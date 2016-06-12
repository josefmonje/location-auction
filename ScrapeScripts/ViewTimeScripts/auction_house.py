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



csv_file = 'auction_house.csv'
csv_file = open(csv_file, "w")


base_url = "http://www.auctionhouse.uk.net/london/auction/lots/4431"
details_script_url = "http://www.auctionhouse.uk.net/auction/details/"

auctions = []

def scrape_list(url):
    try:
        global auctions
        
        homepage = urllib2.urlopen(url)
        soup = bs4.BeautifulSoup(homepage, 'html.parser')
        for div in soup.findAll('a', text="View Full Details"):
            lot_div = div.parent.parent.parent.parent.parent
            
            lot_num = lot_div.find_all('div')[0].find_all('div')[1].h3.contents[2].strip().split(' ')[1]
            address = lot_div.div.find_next_sibling('div').find_all('div')[0].h3.string
            link = div['data-id']
        
            auction = {
                    'lot_num': lot_num,
                    'address': address,
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

scrape_list(base_url)


# load the auction page, get the timings and print the result
for auction in auctions:
    try:
        request = urllib2.Request(auction['url'], headers={"Referer" : base_url, "X-Requested-With":"XMLHttpRequest"})
        soup = bs4.BeautifulSoup(urllib2.urlopen(request).read(), 'html.parser')
        timings = []
        try:
            timing_ps = soup.find_all('h3', text="Viewing Details")[0].find_next_sibling('p').string.strip()
            timings.append(timing_ps)
        except:
            pass

        auction['timings'] = timings         
        writer = csv.writer(csv_file)
        writer.writerow([ auction['lot_num'], auction['address'] ] + auction['timings'])
        csv_file.flush()
    except:
        pass

