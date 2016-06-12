import requests
import json

postcode="SE228QB"
r = requests.get("http://maps.googleapis.com/maps/api/geocode/json?address="+postcode+",+UK&sensor=false")
if r.status_code == 200:
    loc = r.json()['results'][0]['geometry']['location']
    print loc['lat'], loc['lng']