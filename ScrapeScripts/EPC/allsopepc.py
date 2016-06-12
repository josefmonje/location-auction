import requests


import scraperwiki

import urllib2, lxml.etree, mechanize, cookielib


username= 'afrakhan'
password= 'password123'

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
br.open('http://www.auction.co.uk/residential/Epc.asp')
#br.open('https://www.eigroup.co.uk/Login.aspx?ReturnUrl=%2fclients%2f')

# Select the form (form does not have name?)
br.form=list(br.forms())[1]



# Set the user name and password for the selected form
for control in br.form.controls:
    if control.type=="text":
        br[control.name]=username
    if control.type=="password":
        br[control.name]=password

#Submit the user name and password to login
resp=br.submit()


r = br.open('http://www.auction.co.uk/residential/Epcpdf.asp?Lot=1&ID=931000001&A=931')

html = r.read()
print html

url = 'http://legals.auction.co.uk/residential//mar2015/1/energy'

pdfdata = urllib2.urlopen(url).read()
print pdfdata


# xmldata = scraperwiki.pdftoxml(pdfdata)
# root = lxml.etree.fromstring(xmldata)


