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

f = open('ViewTimeScripts/strettons.csv')

reader = csv.reader(f)

x = {}
for row in reader:
    print row

    viewing_time = ''
    for i in range(2, len(row)):
        item = row[i].strip()
        if item:
            viewing_time = viewing_time + item + " " + "\n"
            #viewing_time = viewing_time.strip()
    print viewing_time

    x[row[0]] = viewing_time


for i, k in x.iteritems():
    print i, k
    try:
        item=Auction.objects.get(auctioneer='Strettons', lot = i )

        item.viewing_time = k

        item.save()
    except:
        pass
