from django.contrib import admin

from .models import Auction, Geocode, SoldPrice


class AuctionAdmin(admin.ModelAdmin):
    pass


class GeocodeAdmin(admin.ModelAdmin):
    pass


class SoldPriceAdmin(admin.ModelAdmin):
    pass

admin.site.register(Auction, AuctionAdmin)
admin.site.register(Geocode, GeocodeAdmin)
admin.site.register(SoldPrice, SoldPriceAdmin)
