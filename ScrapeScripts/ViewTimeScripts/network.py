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



csv_file = 'network.csv'
csv_file = open(csv_file, "w")


base_url = "https://dms.eigroup.co.uk/data/script/auction/444/"
details_script_url = "https://dms.eigroup.co.uk/data/script/lot/"

auctions = []

def scrape_list(url):
    try:
        global auctions
        
        homepage = urllib2.urlopen(url)
        page_data=homepage.read()
        data="".join([i.replace('document.write("' , '').replace('");', '').replace('\\"', '"').replace("\\'", "'").rstrip() for i in page_data.split('\n')])
        soup = bs4.BeautifulSoup(data, 'html.parser')
        
        for lot in soup.findAll('h2', {"class" : "lotnum"}):
            lot_num=lot.string.split(" ")[1].strip()
            address=lot.parent.parent.findAll('p', {"class" : "address"})[0].string.replace(u'\xa0', ' ').strip()
            lid=lot.parent.parent.findAll('a', {"class" : "button"})[0]['href'].split("&")[0].split("=")[1]
            auction = {
                    'lot_num': lot_num,
                    'address':address,
                    'url': details_script_url + lid+"/37/"
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
        homepage = urllib2.urlopen(auction['url'])
        page_data=homepage.read()
        data="".join([i.replace('document.write("' , '').replace('");', '').replace('\\"', '"').replace("\\'", "'").rstrip() for i in page_data.split('\n')])
        soup = bs4.BeautifulSoup(data, 'html.parser')
 
        timings = []
        try:
            timing_ps = soup.find_all('div', text=re.compile('To View'))[0].find_next_sibling('p').string.strip()
            timings.append(timing_ps)
        except:
            pass
         
        auction['timings'] = timings
         
        writer = csv.writer(csv_file)
        writer.writerow([ auction['lot_num'], auction['address'] ] + auction['timings'])
        csv_file.flush()
    except:
        pass

