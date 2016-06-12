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


def load_time(path):
    auctions=[]
    for file in glob.glob(path + '/*.csv'):
        with open(file) as f:
            print file
            reader = csv.reader(f)
            for row in reader:
                lot_num = row[0]
                address = row[1]
                viewing_time = ''
                for i in range(2, len(row)):
                    item = row[i].strip()
                    if item:
                        viewing_time = viewing_time + item + "\n"
                viewing_time = viewing_time.strip()

                auction = {
                     'lot':lot_num,
                     'address':address,
                     'viewing_time':viewing_time
                }

                auctions.append(auction)

    #now prepare all the address fields
    address_list=Auction.objects.all().values_list('address', flat=True)
    for auction in auctions:
        #ignore those does not have viewing time
        try:
            if auction['viewing_time']!='':
                address=auction['address']
                highest=0
                target=''
                for val in address_list:
                    similarity=difflib.SequenceMatcher(a=address.lower(), b=val.lower()).ratio()
                    if similarity>highest:
                        highest=similarity
                        target=val
                if highest>0.5:
                    #find a match, update the database
                    item=Auction.objects.get(address=target)
                    item.viewing_time=auction['viewing_time']
                    item.save()
                else:
                    print auction
        except Exception as e:
            print e
            pass



path = 'ScrapeScripts/ViewTimeScripts/strettons.csv'



print path
##################################################
########## UNCOMMENT TO LOAD DATA ################
##################################################



load_time(path)