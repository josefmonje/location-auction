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
    string = ''.join([ text for text in element.stripped_strings ])

    return string.encode('utf8')



csv_file = 'strettons.csv'
csv_file = open(csv_file, "w")

base_url = "http://auctions.strettons.co.uk/CurrentAuction.aspx"

homepage = urllib2.urlopen(base_url)
soup = bs4.BeautifulSoup(homepage)

# there are multiple scripts that render the auction pages
# first, main_script is loaded, which in turn loads auction_script
main_script_element = soup.find('script')
main_script_url = main_script_element.get('src')
main_script = urllib2.urlopen(main_script_url)
main_script_content = main_script.read().decode('utf8')

# auction_script generates the actual list of actions on the home page
auction_script_url_matches = re.search("http.*auction/[0-9]+/", main_script_content)
auction_script_url = auction_script_url_matches.group()
auction_script = urllib2.urlopen(auction_script_url)
auction_script_content = auction_script.read().decode('utf8')
auction_script_content = decode_document_writes(auction_script_content)

# details_script contains all the details of an auction
details_script_url_matches = re.search("http.*/lot/", main_script_content)
details_script_url = details_script_url_matches.group()

soup = bs4.BeautifulSoup(auction_script_content)

# all the auction information. it is not really required,
# but can be helpful if the script needs to be extended
auctions = []
for tr in soup.find_all('tr'):
    tds = tr.find_all('td')
    if (len(tds) != 3):
        continue

    lot_td, link_td, _ = tds

    # lot num is easier to get here
    lot_num = get_stripped_string(lot_td)

    # link to the particular auction page
    link_a = link_td.find('a')
    link = link_a.get('href')

    # extra parameters that may be pased
    lid = re.sub('.*lid=([0-9]+).*', '\\1', link)
    tid = re.sub('.*tid=([^&]*).*', '\\1', link)

    # logic copied from the javascript
    if tid == link:
        tid = '9'

    # last part of the URL
    urlpart = lid + "/" + tid

    auction = {
            'lot_num': lot_num,
            'url': details_script_url + urlpart + '?src=null'
    }

    auctions += [ auction ]

writer = csv.writer(csv_file)

# load the auction page, get the timings and print the result
for auction in auctions:
    url = auction['url']
    auction_page = urllib2.urlopen(url)
    auction_content = auction_page.read().decode('utf8')
    auction_content = decode_document_writes(auction_content)

    soup = bs4.BeautifulSoup(auction_content)
    lot_address_div = soup.find(class_ = 'lotaddress')
    lot_address = get_stripped_string(lot_address_div)

    timing_ps = soup.find_all(class_ = 'red')

    timings = []
    for timing_p in timing_ps:
        timings += [ get_stripped_string(timing_p) ]

    auction['address'] = lot_address
    auction['timings'] = timings

    writer.writerow([ auction['lot_num'], auction['address'] ] + auction['timings'])
    csv_file.flush()

