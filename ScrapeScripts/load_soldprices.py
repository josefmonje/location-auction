import os
import sys

from django.core.wsgi import get_wsgi_application

os.environ['DJANGO_SETTINGS_MODULE'] = 'auction.settings'

from django.utils import timezone

from auction.models import SoldPrice



from django.core.wsgi import get_wsgi_application
from django.conf import settings



import django

django.setup()

import csv
import requests
from datetime import datetime
import pytz

reader = csv.reader(open(os.path.expanduser("~/Google Drive/auction/pricepaiddata/singleyearlyfiles/pp-2013.csv")))

#reader = csv.reader(open('Users/afrakhan/Google Drive/auction/pricepaiddata/singleyearlyfiles/pp-2013.csv'))

# filename = str(datetime.now()).split()[0] + '.csv'

# with open(filename, 'w') as outputfile:
    # output = csv.writer(outputfile)
count = 0
for row in reader:

    print count
    count += 1
    if row:
        LR_ID = row[0].strip()
        paid_price = float(row[1].strip())
        date = datetime.strptime(row[2], '%Y-%m-%d %H:%M').date()
        postcode = row[3].strip()
        property_type = row[4].strip()
        old_new = row[5].strip()
        tenure = row[6].strip()
        PAON = row[7].strip()
        SAON = row[8].strip()
        street = row[9].strip()
        locality = row[10].strip()
        town = row[11].strip()
        district = row[12].strip()
        county = row[13].strip()
        record = row[14].strip()

        # exists = SoldPrice.objects.filter(LR_ID=LR_ID)
        # if not exists:

        SP = SoldPrice(
            LR_ID=LR_ID,
            paid_price=paid_price,
            date=date,
            postcode=postcode,
            property_type=property_type,
            old_new=old_new,
            tenure=tenure,
            PAON=PAON,
            SAON=SAON,
            street=street,
            locality=locality,
            town=town,
            district=district,
            county=county,
            record=record,
        )
        SP.save()

                # output.writerow(row)
 # outputfile.close()