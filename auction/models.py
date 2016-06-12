from django.db import models
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.core.files.storage import FileSystemStorage

from auction.utils import Geocodeutil

import hashlib
import random
import os
import settings
import requests
import json

dbfs = FileSystemStorage(location=settings.STATIC_ROOT, base_url='/static/')
md5_constructor = hashlib.md5
md5_hmac = md5_constructor
sha_constructor = hashlib.sha1
sha_hmac = sha_constructor


def generate_sha1(string, salt=None):
    """
    Generates a sha1 hash for supplied string. Doesn't need to be very secure
    because it's not used for password checking. We got Django for that.

    :param string:
        The string that needs to be encrypted.

    :param salt:
        Optionally define your own salt. If none is supplied, will use a random
        string of 5 characters.

    :return: Tuple containing the salt and hash.

    """
    if not salt:
        salt = sha_constructor(str(random.random())).hexdigest()[:5]
    hash = sha_constructor(salt + str(string)).hexdigest()
    return (salt, hash)


def upload_to_db(subpath='images'):
    def upload_to(instance, filename):
        """
        Store the flat image
        """
        extension = filename.split('.')[-1].lower()
        salt, hash = generate_sha1(instance.pk)
        name = '%(hash)s.%(extension)s' % {'hash': hash[:10],
                                           'extension': extension}
        return os.path.join(subpath, name)
    return upload_to_db


class Geocode(models.Model):
    postcode = models.CharField(max_length=10, unique=True)
    latitude = models.FloatField()
    longitude = models.FloatField()


class Auction(models.Model):
    lot = models.CharField(max_length=20, null=True, blank=True)
    image = models.ImageField(storage=dbfs, upload_to=upload_to_db('images'),
                              null=True, blank=True)
    image_src = models.CharField(max_length=150, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    town = models.CharField(max_length=30, blank=True, null=True)
    postcode = models.CharField(max_length=20, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    guide_price = models.CharField(max_length=30, blank=True, null=True)
    price = models.FloatField(null=True)
    auctioneer = models.CharField(max_length=50, blank=True, null=True)
    auction_date = models.DateField(auto_now=False, auto_now_add=False,
                                    blank=True, null=True, editable=True)
    lease_details = models.TextField(null=True, blank=True)
    vendor = models.CharField(max_length=50, blank=True, null=True)
    viewing_time = models.TextField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    # https://docs.djangoproject.com/en/1.7/ref/contrib/gis/model-api/
    point = models.PointField(null=True, blank=True)

    objects = models.GeoManager()

    def save(self, *args, **kwargs):
        g = Geocodeutil(self.postcode)
        if g:
            self.latitude, self.longitude = g
        if self.latitude and self.longitude:
            self.geom = Point(self.longitude, self.latitude)
        super(Auction, self).save(*args, **kwargs)

    def to_json(self):
        return {
            'image_src': self.image_src,
            'id': self.id,
            'address': self.address,
            'price': self.price,
            'description': self.description,
            'lease_details': self.lease_details,
            'auctioneer': self.auctioneer,
            'lot': self.lot,
            'auction_date': str(self.auction_date),
            'viewing_time': self.viewing_time,
            # 'town': self.town,
            # 'guide_price': self, guide_price,
            # 'postcode': self.postcode,
            # 'vendor': self.vendor,
            'qs': '?id=' + str(self.id),
            'coordinates': {'latitude': self.latitude,
                            'longitude': self.longitude},
        }

    def coordinates(self):
        return (self.longitude, self.latitude)


class SoldPrice(models.Model):
    LR_ID = models.CharField(max_length=38, null=True, blank=True)
    paid_price = models.FloatField(null=True, blank=True)
    date = models.DateField(auto_now=False, auto_now_add=False,
                            blank=True, null=True, editable=True)
    postcode = models.CharField(max_length=8, blank=True, null=True)
    property_type = models.CharField(max_length=1, null=True, blank=True)
    old_new = models.CharField(max_length=1, null=True, blank=True)
    tenure = models.CharField(max_length=1, null=True, blank=True)
    PAON = models.CharField(max_length=100, null=True, blank=True)
    SAON = models.CharField(max_length=100, null=True, blank=True)
    street = models.CharField(max_length=100, null=True, blank=True)
    locality = models.CharField(max_length=50, null=True, blank=True)
    town = models.CharField(max_length=50, null=True, blank=True)
    district = models.CharField(max_length=50, null=True, blank=True)
    county = models.CharField(max_length=50, null=True, blank=True)
    record = models.CharField(max_length=1, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    point = models.PointField(null=True, blank=True)

    objects = models.GeoManager()

    def save(self, *args, **kwargs):
        g = Geocodeutil(self.postcode)
        if g:
            self.latitude, self.longitude = g
        if self.latitude and self.longitude:
            self.geom = Point(self.longitude, self.latitude)
        super(SoldPrice, self).save(*args, **kwargs)

    def address(self):
        address = ''
        if self.street:
            address = address + self.street.title() + ', '
        if self.locality:
            address = address + self.locality.title() + ', '
        if self.town:
            address = address + self.town.title() + ', '
        if self.district:
            address = address + self.district.title() + ', '
        if self.county:
            address = address + self.county.title() + ', '
        if self.postcode:
            address = address + self.postcode
        return address

    def to_json(self):
        return {
            'id': self.id,
            'LR_ID': self.LR_ID,
            'date': str(self.date),
            'paid_price': self.paid_price,
            'postcode': self.postcode,
            'address': self.address(),
            # 'property_type': self.property_type,
            # 'old_new': self.old_new,
            # 'tenure': self.tenure,
            # 'PAON': self.PAON,
            # 'SAON': self.SAON,
            # 'record': self.record,
            'coordinates': {'latitude': self.latitude,
                            'longitude': self.longitude}
        }

    def coordinates(self):
        return (self.longitude, self.latitude)
