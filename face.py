#!/usr/bin/python

import mechanize
from bs4 import BeautifulSoup
import cookielib
import re

#browser handlers
browser = mechanize.Browser()
browser.addheaders  = [ ( 'User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0' ) ]
browser.set_handle_equiv( True )
browser.set_handle_gzip( True )
browser.set_handle_redirect( True )
browser.set_handle_referer( True )
browser.set_handle_robots( False )

#cookie
cookiejar = cookielib.LWPCookieJar()
browser.set_cookiejar(cookiejar)

#authenticate
browser.open('http://m.facebook.com/login.php')
browser.select_form(nr=0)
browser["email"] = 'uukaran1@gmail.com'
browser["pass"] = 'Chr0n!cl3'
response = browser.submit()

#scrapping
home = browser.open("https://m.facebook.com/messages/read/?tid=id.616722851766788&refid=11#fua").read()
soup = BeautifulSoup(home , 'lxml')
#print soup.prettify()
#for element in soup.(string=re.compile("sharma")):
#print soup.find(string=re.compile("dinkar") , 'a')

#spamming
while True:
    browser.select_form(nr=1)
    browser["body"]='FUCK\nFUCK\nFUCK'
    browser.submit()
