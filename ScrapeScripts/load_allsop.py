import os
import sys

from django.core.wsgi import get_wsgi_application

os.environ['DJANGO_SETTINGS_MODULE'] = 'auction.settings'
application = get_wsgi_application()



import csv
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
import urllib2
from auction.models import Auction
from datetime import datetime
import requests
import json
import time
import glob
import difflib




##################################################
########## UNCOMMENT TO LOAD DATA ################
##################################################

f = open('AUCTION/AUCTION/spiders/auctionsoutput.csv')

reader = csv.reader(f)

x = {}
for row in reader:
   x[row[2]] = row[0]


for i, k in x.iteritems():
    print i, k
    try:
        item=Auction.objects.get(auctioneer='Allsop Residential', lot = i )

        item.viewing_time = k

        item.save()
    except:
        pass
