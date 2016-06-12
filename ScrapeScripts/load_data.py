import os
import sys

from django.core.wsgi import get_wsgi_application

os.environ['DJANGO_SETTINGS_MODULE'] = 'auction.settings'

application = get_wsgi_application()

from django.utils import timezone

from auction.models import Auction

from datetime import datetime

import csv
import requests
import json


count = 0

def load_csv(file):

    with open(file) as f:
        reader = csv.reader(f)
        first_line = True
        count = 1
        for row in reader:
            if first_line:
                first_line = False
                continue
            print count
            count += 1
            try:
                lot=row[0].strip()
                image_src = row[1].strip()
#                 if '.' in image_src:
#                     extension = '.' + image_src.split('.')[-1].lower()
#                 else:
#                     extension = ".jpg"
#                 img_temp = NamedTemporaryFile(suffix=extension, delete=True)
#                 img_temp.write(urllib2.urlopen(image_src).read())
#                 img_temp.flush()
#                 image = File(img_temp)

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
                try:
                    auction_date = datetime.strptime(row[9], '%d %B %Y')
                except:
                    auction_date = None
                lease_details = row[10].strip()
                vendor = row[11].strip()

                # now retrieve the lat and long location based on zip code

                # try:
                #     r = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address=" + postcode + "UK&sensor=false&key=AIzaSyAnfBmJtJWYu5qynm_pnFVe775CG8LNBxY")
                #     if r.status_code == 200:
                #         loc = r.json()['results'][0]['geometry']['location']

                #         lat = float(loc['lat'])
                #         lng = float(loc['lng'])
                #         print 'success', lat, lng
                # except:
                #     lat = None
                #     lng = None
                #     print 'error'


                # print image_src, address, town, postcode, guide_price, price, auctioneer, auction_date, lease_details, vendor

                auction, created = Auction.objects.get_or_create(address=address)
                auction.lot=lot
                auction.image_src = image_src
#                 auction.image = image
                auction.town = town
                auction.postcode = postcode
                auction.description = description
                auction.guide_price = guide_price
                auction.price = price
                auction.auctioneer = auctioneer
                auction.auction_date = timezone.make_aware(auction_date, timezone.get_current_timezone())
                auction.lease_details = lease_details
                auction.vendor = vendor
                # if lat is not None:
                #     auction.geom = {'type': 'Point', 'coordinates': [lng, lat]}

                auction.save()

            except Exception as e:
                print e






datafile = 'data.csv'


##################################################
########## UNCOMMENT TO LOAD DATA ################
##################################################

load_csv(datafile)


#load_time(path)
