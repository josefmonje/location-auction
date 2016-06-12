"""This module contains spider for http://www.auction.co.uk/residential/onlineCatalogue.asp"""
from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from AUCTION.util import Formatter
from AUCTION.auction_item import AuctionItem
import urlparse
import re

class Auction(Spider):
    """Class for scrapy spider"""
    name = "auction"
    start_urls = ["http://www.auction.co.uk/residential/onlinecatalogue.asp"]
    base_url = 'http://www.auction.co.uk/residential/'
    def parse(self, response):
        """default parsing function of spider"""
        sel = Selector(response)
        yield Request('http://www.auction.co.uk/residential/onlinecatalogue.asp', self.parse_again, dont_filter=True)
    def parse_again(self, response):
        """parsing the page again because at first time its not rendering the lots grid"""
        sel = Selector(response)
        page_urls = []
        page_urls.append(response.url)
        urls = sel.xpath("//table[@id='Table5']/tr/td[3]/a/@href").extract()
        for url in urls:
            page_urls.append(urlparse.urljoin(self.base_url, url))
        for page_url in page_urls:
            yield Request(page_url, self.parse_page)
    def parse_page(self, response):
        """parsing each pagination link"""
        sel = Selector(response)
        
        table = sel.xpath("//table[@class='Main']").extract()
        if len(table) > 0:
            links = sel.xpath("//table[@class='Main']/tr/td[1]/a/@href").extract()
            for link in links:
                yield Request(urlparse.urljoin(self.base_url, link), self.parse_lot)
    def parse_lot(self, response):
        """parsing each lot's detail page"""
        sel = Selector(response)
        num = Formatter.remove_spaces(sel.xpath("//div[@class='lotNum']/text()").extract()[0])
        adr = Formatter.remove_spaces(sel.xpath("//div[@class='address']/text()").extract()[0])
        view = sel.xpath("//div[@style='padding-right:10px;']").extract()[0]

        if 'To View' in view:
            info = view[view.index('To View'):].split('<h3')[0]
            info = Formatter.remove_tags(info)
            info = info.split('To View')[0] + ' To View ' + info.split('To View')[1]
            info = info.replace("To View ", "")
            info = info.replace("The property will be open for viewing ", "").replace("These are open viewing times with no need to register. ","")
            info = info.strip()
        else:
            info = 'No Viewings'
        item = AuctionItem()
        item['lot_num'] = num
        item['allsop_address'] = adr
        item['view_info'] = info
        yield item