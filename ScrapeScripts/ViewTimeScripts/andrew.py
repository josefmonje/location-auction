#!/usr/bin/python

# Scrape http://auctions.strettons.co.uk and store the results
# in a CSV file
#
# Syntax: scrape_auctions.py <csv_file|->
# If the first argument is '-', then the output is printed on the screen

import re
import bs4
import csv
import sys
import urllib2

# most of the documents are generated dynamically through document.write()
# this function extracts the strings out of document.write(), unescapes double quotes
# and converts non-breaking spaces to normal spaces
def decode_document_writes(content):
    content = re.sub('^document.write\("(.*)"\);', '\\1', content, 0, re.MULTILINE)
    content = re.sub('\\\\', '', content, 0, re.MULTILINE)
    # replace &nbsp; with a space
    content = re.sub(u'\u00a0', ' ', content, 0, re.MULTILINE)
    return content

# get the stripped string from a HTML element
def get_stripped_string(element):
    print element
    # string = ''.join([ text for text in element.stripped_strings ])
    return element.string.strip()
    # return string.encode('utf8')



csv_file = 'andrew.csv'
csv_file = open(csv_file, "w")


base_url = "http://www.as-r.co.uk/property-auctions/search-results/auction-properties-for-sale-in-uk/page-"
details_script_url = "http://www.as-r.co.uk"

auctions = []

def scrape_list(url):
    try:
        global auctions
        
        homepage = urllib2.urlopen(url)
        soup = bs4.BeautifulSoup(homepage, 'html.parser')
        
        for tr in soup.findAll("tr", { "class" : "clickable" }):
            tds = tr.find_all('td')
            if (len(tds) != 4):
                continue
        
            lot_td, link_td, loc_td, price_td = tds
        
            # lot num is easier to get here
            lot_num = get_stripped_string(lot_td)
        
            # link to the particular auction page
            link_a = link_td.find('a')
            link = link_a.get('href')
        
            auction = {
                    'lot_num': lot_num,
                    'url': details_script_url + link
            }
            
            try:
                [x['lot_num'] for x in auctions].index(auction['lot_num'])
            except:
                # means this lot number has not been indexed
                print auction
                auctions += [ auction ]
        return True
    except Exception as e:
        print e
        return False

for i in range(1, 20):
    print "scraping page " + str(i)
    if scrape_list(base_url + str(i)):
        continue
    else:
        break

# load the auction page, get the timings and print the result
for auction in auctions:
    try:
        auction_page = urllib2.urlopen(auction['url'])
        soup = bs4.BeautifulSoup(auction_page, 'html.parser')
        lot_address = ""
        try:
            lot_address_div = soup.findAll("div", { "class" : "property-details-header" })[0]
            lot_post_code = get_stripped_string(lot_address_div.div.h1.span.string)
            lot_address = get_stripped_string(lot_address_div.div.h1.contents[2])
        except:
            pass
            
        timings = []
        try:
            timing_ps = soup.find_all('h4', text="Viewing Times")[0].find_next_sibling('ul').find_all('li')
            timings = []
            for timing_p in timing_ps:
                timings += [ get_stripped_string(timing_p.string) ]
        except:
            pass
    
        auction['address'] = lot_address
        auction['timings'] = timings
        
        writer = csv.writer(csv_file)
        writer.writerow([ auction['lot_num'], auction['address'] ] + auction['timings'])
        csv_file.flush()
    except:
        pass

