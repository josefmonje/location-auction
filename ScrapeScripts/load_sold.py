import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'auction.settings'



import csv
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
import urllib2
from auction.models import SoldPrice
from datetime import datetime
import requests
import json
import time
import glob
import difflib



f = open('C:/Users/afrakhan/Google Drive/auction/pricepaiddata/singleyearlyfiles/pp-2010.csv')

#f = open (os.path.expanduser("~/Downloads/pp-complete.csv"))


reader = csv.reader(f)
count = 0

for row in reader:
    print count
    count += 1

    date_sold = datetime.strptime(row[2], '%Y-%m-%d %H:%M').date()
    postcode_strip = row[3].replace(" ", "")
    try:
        SP = SoldPrice(postcode_strip = postcode_strip , LR_ID = row[0], paid_price = row[1], date = date_sold, postcode = row[3], property_type = row[4], old_new = row[5], tenure = row[6], PAON = row[7], SAON = row[8], street = row[9], locality = row[10], town = row[11], district = row[12], county = row[13], record = row[14])
    except:
        print 'fail', row[0]
        pass

    # try:
    #     r = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address=" + postcode + "UK&sensor=false&key=AIzaSyAnfBmJtJWYu5qynm_pnFVe775CG8LNBxY")
    #     if r.status_code == 200:
    #         loc = r.json()['results'][0]['geometry']['location']
    #         lat = float(loc['lat'])
    #         lng = float(loc['lng'])
    # except:
    #     lat = None
    #     lng = None
    #
    # if lat is not None:
    #     SP.geom = {'type': 'Point', 'coordinates': [lng, lat]}
    SP.save()