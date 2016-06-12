from django.db.models import get_model

import requests


def Geocodeutil(postcode):
    Geocode = get_model('auction.Geocode')
    g = Geocode.objects.filter(postcode=postcode)
    if g:
        g = g[0]
        latitude = g.latitude
        longitude = g.longitude
    elif not g:
        try:
            r = requests.get(
                "https://maps.googleapis.com/maps/api/geocode/json?address="
                + postcode + ",UK&sensor=false")
            if r.status_code == 200:
                loc = r.json()['results'][0]['geometry']['location']
                latitude = float(loc['lat'])
                longitude = float(loc['lng'])

                g = Geocode(
                    postcode=postcode,
                    latitude=latitude,
                    longitude=longitude
                )
                g.save()
            else:
                print 'Tried getting coordinates got error', r.status_code
        except Exception:
            print 'Error getting coordinates:', postcode
    if 'latitude' in locals() and 'longitude' in locals():
        return latitude, longitude
