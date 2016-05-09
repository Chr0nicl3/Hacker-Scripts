#!/usr/bin/python

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import time

driver = webdriver.Firefox()
driver.get('http://site21.way2sms.com/content/index.html')

username = driver.find_element_by_name("username")
password = driver.find_element_by_name("password")

username.send_keys('8962411778')
password.send_keys('karan0912')

driver.find_element_by_id("loginBTN").click()
driver.find_element_by_css_selector('input.button.br3').click()
driver.find_element_by_id("sendSMS").click()
mobile = driver.find_element_by_name("mobile").click()
message = driver.find_element_by_name("message").click()

while True:
    os.system('clear')
    print "***Message should not be more than 140 characters***"
    msg = str(raw_input("Enter The Message:\n"))
    if len(msg)>140:
        print "Message is too long allowed limit is 140 characters and your message have %d characters"%(len(msg))
    else:
        mobile.send_keys('9425115245')
        message.send_keys('%s')%(msg)
        driver.find_element_by_id('Send').click()
