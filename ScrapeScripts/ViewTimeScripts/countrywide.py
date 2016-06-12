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



csv_file = 'countrywide.csv'
csv_file = open(csv_file, "w")


base_url = "http://www.countrywidepropertyauctions.co.uk/search.php?current=1&page="
details_script_url = "http://www.countrywidepropertyauctions.co.uk/"

auctions = []

def scrape_list(url):
    try:
        global auctions
        
        homepage = urllib2.urlopen(url)
        soup = bs4.BeautifulSoup(homepage, 'html.parser')
        all_exist=True
        for elem in soup.findAll('div', { "class" : "propertyListing" }):
            lot_num_string = elem.findAll('div', {'class':'description'})[0].h2.contents[0].strip()
            if '|' in lot_num_string:
                lot_num=lot_num_string.split('|')[0].split(' ')[1].strip()
            else:
                lot_num=''
            address=elem.findAll('div', {'class':'description'})[0].h3.string.strip()
            link=elem.findAll('a')[0]['href'].strip()
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
            view_time=soup.findAll('div', {'id':'propertyLinks'})[0](text=re.compile(r'Viewings'))[0].parent.find_next_sibling('p').string.strip()
            timings.append(view_time) 
        except Exception as e:
            print e
            pass
     
        auction['timings'] = timings
         
        writer = csv.writer(csv_file)
        writer.writerow([ auction['lot_num'], auction['address'] ] + auction['timings'])
        csv_file.flush()
        
    except:
        pass

