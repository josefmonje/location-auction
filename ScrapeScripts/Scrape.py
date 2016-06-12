# -*- coding: utf-8 -*-
"""
Created on Mon Oct 27 17:34:51 2014

@author: rs538
"""

############################################
#Web scraping property auction
###########################################

#import os
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "auction.settings")

#from models import EIG


import mechanize
import cookielib
from bs4 import BeautifulSoup
import csv
import re
import sys, logging




# Columns for the data extraction
columns=['Lot Number', 'Image', 'Address', 'Town', 'Postcode', 'Description',  'Guide Price', 'Price', 'Auctioneer', 'Auction Date', 'Lease Details', 'Vendor']
# Final output csv filename
filename='data.csv'


##############################################
#Function to extract the listing data from html
##############################################
def extractData(html):
    mainData=[]
    #Convert the html file into soup for extraction: BUG Does not cpytonvert the whole html into soup?
    soup=BeautifulSoup(html)
    #Find the tables which contain the data (using width as an unique identfier?)
    tables=soup.findAll('table', width="100%")
    #Iterate over each table 
    for table in tables:
        data = {}
        #Get the address of the listing which is the header of the table
        data['Address']=[table.findAll('th')[0].string]
        data['Postcode']=[table.findAll('th')[0].string.split(",")[-1]]
        try:
            data['Town']=[table.findAll('th')[0].string.split(",")[-2]]
        except Exception, e:
            pass

        #Iterate over each row and each column and extract the data
        for row in table.findAll('tr'):
            for cell in row.findAll('td'):
                cellValues=cell.findAll(text=True)
                links=[]
                for x in cell.findAll('img', width = 150):
                    link = x['src']
                    links.append(link)
                    data['Image']= links

                # For each column find the respective data values and store in a dict
                for i, s in enumerate(cellValues):
                    if 'Description' in s:
                        data['Description']=[cellValues[i+1].strip()] if (i + 1) < len(cellValues) else [None]
                    if 'Guide Price' in s:
                        data['Guide Price']= [cellValues[i+1].strip().encode('utf-8', 'ignore').replace("Â", "")] if (i + 1) < len(cellValues) else [None]
                        for j in data['Guide Price']:
                            ls = []
                            j = j.split("to")[0]
                            k = re.sub(r'\D', "", j)
                            ls.append(k)
                        data['Price'] = ls
                    if 'Lot Number' in s:
                        data['Lot Number']= [cellValues[i+1].strip()] if (i + 1) < len(cellValues) else [None]
                    if 'Auctioneer' in s:
                        data['Auctioneer']=[cellValues[i+2].strip()] if (i + 2) < len(cellValues) else [None]
                    if 'Auction Date' in s:                                  
                        data['Auction Date']=[cellValues[i+2].strip()] if (i + 2) < len(cellValues) else [None]
                    if 'Lease Details' in s:
                        data['Lease Details']=[cellValues[i+1].strip().encode('utf-8', 'ignore')] if (i + 1) < len(cellValues) else [None]
                    if 'Vendor' in s:
                        data['Vendor']=[cellValues[i+1].strip()] if (i + 1) < len(cellValues) else [None]

        print data


        #Add that to the main data dataframe to be returned


        mainData.append(data)
        #print mainData    
        
    return mainData                

###########################################################################################

#User name and password for login

username= '762136'
password= '788683'

# Create browser
br= mechanize.Browser(factory=mechanize.RobustFactory())

# Create a cookie jar to handle the cookies from the website
cj= cookielib.LWPCookieJar()
# Assign cookie handling capabilities to the browser
br.set_cookiejar(cj)

# Set Browser options
br.set_handle_equiv(True)
#br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
# Follows refresh 0 but not hangs on refresh > 0
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
# Log information about HTTP redirects and Refreshes.
#br.set_debug_redirects(True)
# Log HTTP response bodies (ie. the HTML, most of the time).
#br.set_debug_responses(True)
# Print HTTP headers.
#br.set_debug_http(True)


# # To make sure you're seeing all debug output:
#logger = logging.getLogger("mechanize")
#logger.addHandler(logging.StreamHandler(sys.stdout))
#logger.setLevel(logging.INFO)

# Open the website for login
br.open('https://www.eigroup.co.uk/clients/auctions/future.aspx')
#br.open('https://www.eigroup.co.uk/Login.aspx?ReturnUrl=%2fclients%2f')

# Select the form (form does not have name?)
br.form=list(br.forms())[0]

# Set the user name and password for the selected form
for control in br.form.controls:
    if control.type=="text":
        br[control.name]=username
    if control.type=="password":
        br[control.name]=password
    
#Submit the user name and password to login
resp=br.submit()

#Create dataframes to hold the data 1. for each auctioneer 2. for all auctioneer
allData=[]

#Find all the links for auctions 
allauctionlinks=[l for l in br.links(url_regex='auctionid')]

# Iterate over all links (Only the first five)
for link in allauctionlinks[0:50]:
    print link.url
    #Click the link
    request=br.follow_link(link)
    #link=br.find_link(url_regex='fulldetails')

    # Find the link for full details and click the link (iterate for all )
    try:
        respond=br.follow_link(url_regex='fulldetails')
    except:
        pass
    html=respond.read()
    
    
    myData=extractData(html)
    
    respond=br.back()
    respond=br.back()

    allData.append(myData)
    #Rearramge the columns 
    html=''


#print allData
#Write the output dataframe into a csv file
with open(filename,'wb') as f:
    csvwriter = csv.writer(f, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csvwriter.writerow(columns)
    for data in allData:
        for row in data:
            ordered_row = []
            for item in columns:
                ordered_row.append(row[item][0] if item in row else None)
            csvwriter.writerow(ordered_row)

# #Print the final table
# print allData



################################################
#Writing the data into SQL file
################################################

#Create a SQL connection

#con=mysql.connector.connect(user='LendInvest', password='1234', host='local', database='Auction Listings')
#allData.to_sql(name='Auction_Listing', con=con, flavor='mysql', if_exists='replace')
################################################

###############################################
#SQL QUERY TO FIND AVERAGE GUIDE PRICE ACROSS ALL THE LOTS
###############################################
#Convert string to number
# SELECT TO_NUMBER(REGEXP_REPLACE(Guide Price,'[^[:digit:]]')) FROM Auction_Listing
#Find the average
#SELECT AVG(Guide Price) FROM Auction_Listing

