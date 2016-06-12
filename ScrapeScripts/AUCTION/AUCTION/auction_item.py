"""This module contains class for scrapy item for auction spider"""
from scrapy.item import Item, Field
class AuctionItem(Item):
    """The class contains the field that need to be scraped from
    http://www.auction.co.uk/residential/LotDetails.asp?A=930&MP=24&ID=930000010&S=L&O=A"""
    lot_num = Field()
    allsop_address = Field()
    view_info = Field()