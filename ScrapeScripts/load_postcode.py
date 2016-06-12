import os
import sys

from django.core.wsgi import get_wsgi_application

os.environ['DJANGO_SETTINGS_MODULE'] = 'auction.settings'

from auction.models import Geocode

import csv

reader = csv.reader(open('postcodes.csv'))

reader.next()

count = 0
for row in reader:

    print count
    count += 1

    if row:
        postcode = row[0]
        latitude = row[1]
        longitude = row[2]

        # exists = Geocode.objects.filter(postcode=postcode)
        # if not exists:
        PC = Geocode(
            postcode = postcode,
            latitude = latitude,
            longitude = longitude
        )
        PC.save()
