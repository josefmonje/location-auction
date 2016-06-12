import os
import sys

from django.core.wsgi import get_wsgi_application
from django.conf import settings

os.environ['DJANGO_SETTINGS_MODULE'] = 'auction.settings'


import os, django

django.setup()

from auction.models import Auction
from datetime import datetime
import csv

reader = csv.reader(open('data.csv'))

reader.next()
count = 0

for row in reader:
    print count
    count += 1
    if row:
        lot = row[0].strip()
        image_src = row[1].strip()
        address = row[2].strip()
        town = row[3].strip()
        postcode = row[4].strip()
        description = row[5].strip()
        guide_price = row[6].strip()
        try:
            price = float(row[7].strip())
        except:
            price = None
        auctioneer = row[8].strip()
        auction_date = datetime.strptime(row[9], '%d %B %Y')
        lease_details = row[10].strip()
        vendor = row[11].strip()

        # exists = Geocode.objects.filter(postcode=postcode)
        # if not exists:
        A = Auction(
            lot=lot,
            image_src=image_src,
            address=address,
            town=town,
            postcode=postcode,
            description=description,
            guide_price=guide_price,
            price=price,
            auctioneer=auctioneer,
            auction_date=auction_date,
            lease_details=lease_details,
            vendor=vendor
        )
        A.save()
