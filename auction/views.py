from django.core.paginator import Paginator
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView, DetailView

from auction.models import Auction, SoldPrice
from auction.utils import Geocodeutil

# from forms import FilterForm

from djgeojson.serializers import Serializer as gs

from geopy.distance import VincentyDistance as vd

from datetime import datetime

# from ScrapeScripts.load_data import load_csv

import json
import requests


class Search(TemplateView):
    template_name = 'search.html'
    # form_class = FilterForm

    def get_context_data(self, **kwargs):
        context = super(Search, self).get_context_data(**kwargs)
        auctioneers = Auction.objects.values_list(
            'auctioneer', flat=True).distinct()
        context['auctioneers'] = auctioneers.order_by('auctioneer')
        return context


class Home(TemplateView):
    template_name = 'index.html'


class Contact(TemplateView):
    template_name = 'contact.html'


class Rentalyields(TemplateView):
    template_name = 'rentalyields.html'


class Capitalgains(TemplateView):
    template_name = 'capitalgains.html'


class Totalgains(TemplateView):
    template_name = 'totalgains.html'


class AuctionDetail(DetailView):
    model = Auction
    pk_url_kwarg = 'id'
    template_name = 'detail_router.html'


def auction_data(request):
    latitude = request.REQUEST.get('latitude', None)
    longitude = request.REQUEST.get('longitude', None)
    radius = request.REQUEST.get('radius', 3)
    minprice = request.REQUEST.get('minprice', None)
    maxprice = request.REQUEST.get('maxprice', None)
    auctioneer = request.REQUEST.get('auctioneer', None)
    object_id = request.REQUEST.get('id', None)
    point = Point(float(longitude), float(latitude))

    result = Auction.objects.filter(auction_date__gt=datetime.today())
    result = result.filter(point__distance_lte=(point, D(mi=radius)))

    if minprice:
        result = result.filter(price__gte=float(minprice))
    if maxprice:
        result = result.filter(price__lte=float(maxprice))
    if auctioneer:
        result = result.filter(auctioneer=auctioneer)
    if object_id:
        result = result.filter(id=object_id)[:1]

    data = [r.to_json() for r in result]
    data = json.dumps(data)
    return HttpResponse(data)


def sold_data(request):
    radius = request.REQUEST.get('radius', 3)
    object_id = request.GET['id']
    obj = Auction.objects.filter(id=object_id)
    if obj:
        obj = obj[0]
        item = obj.to_json()
        item['icon'] = '../../static/auction/images/green-pin.png'

    data = SoldPrice.objects.filter(
        point__distance_lte=(obj.point, D(mi=radius)))
    data = [d.to_json() for d in data]
    data.append(item)

    data = json.dumps(data)
    return HttpResponse(data)
