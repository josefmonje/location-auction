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



csv_file = 'brendons.csv'
csv_file = open(csv_file, "w")


base_url = "http://www.brendonsauctioneers.co.uk/search_gallery.php?current=1&auctionid=43&page="
details_script_url = "http://www.brendonsauctioneers.co.uk/"

auctions = []

def scrape_list(url):
    try:
        global auctions
        
        homepage = urllib2.urlopen(url)
        soup = bs4.BeautifulSoup(homepage, 'html.parser')
        all_exist=True
        for elem in soup.findAll('div', { "class" : "propertyListing" }):
            lot_num = elem.findAll('div', {'class':'description'})[0].h3.contents[0].strip().split('|')[0].split(' ')[1].strip()
            address=elem.findAll('div', {'class':'description'})[0].h2.string.strip()
            link=elem.findAll('a', {'class' : 'button'})[0]['href'].strip()
            auction = {
                    'lot_num': lot_num,
                    'address':address,
                    'url': details_script_url + link
            }
            
            try:
                [x['lot_num'] for x in auctions].index(auction['lot_num'])
            except:
                # means this lot number has not been indexed
                all_exist=False
                auctions += [ auction ]
        if all_exist:
            return False
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

#load the auction page, get the timings and print the result
for auction in auctions:
    try:
        homepage = urllib2.urlopen(auction['url'])
        soup = bs4.BeautifulSoup(homepage, 'html.parser')
        timings = []
        try:
            for elem in soup(text=re.compile(r'VIEWING')):
                timings.append(elem.parent.span.string.strip())
        except Exception as e:
            print e
            pass
     
        auction['timings'] = timings
         
        writer = csv.writer(csv_file)
        writer.writerow([ auction['lot_num'], auction['address'] ] + auction['timings'])
        csv_file.flush()
    except:
        pass

