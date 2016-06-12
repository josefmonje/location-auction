from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

from auction.views import Home, Contact, Rentalyields, Capitalgains, Totalgains
from auction.views import Search, AuctionDetail
from auction.views import auction_data, sold_data

partial_patterns = patterns('',
    url(r'^search.html$', TemplateView.as_view(template_name='search.html'), name='search'),
    url(r'^search_router.html$', TemplateView.as_view(template_name='search_router.html'), name='search_router'),
    url(r'^detail.html$', TemplateView.as_view(template_name='detail.html'), name='detail'),
    url(r'^detail_router.html$', TemplateView.as_view(template_name='detail_router.html'), name='detail_router'),
    url(r'^list.html$', TemplateView.as_view(template_name='list.html'), name='list'),
    url(r'^home.html$', TemplateView.as_view(template_name='contact.html'), name='home'),
)

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^$', Home.as_view(), name='home'),
    url(r'^partial/', include(partial_patterns, namespace='partials')),
    url(r'^search/$', TemplateView.as_view(template_name='search_router.html'), name='search'),
    url(r'^detail/(?P<id>\d+)/$', AuctionDetail.as_view(), name='detail'),
    url(r'^mapapi/auction-data/$', auction_data, name='auction_data'),
    url(r'^mapapi/sold-data/$', sold_data, name='sold_data'),

    url(r'^contact/$', Contact.as_view(), name='contact'),
    url(r'^rentalyields/$', Rentalyields.as_view(), name='rentalyields'),
    url(r'^capitalgains/$', Capitalgains.as_view(), name='capitalgains'),
    url(r'^totalgains/$', Totalgains.as_view(), name='totalgains'),
)
