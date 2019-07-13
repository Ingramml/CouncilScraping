import requests 
from bs4 import BeautifulSoup 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import os
import re
import time

''' 
Downloads pdf from city of Phoenix meetings
Shoudl be lauched weekly
Nameing convetion is YYYYMMDD Meeting type Document type
	exampel 20190503 Formal Agenda
TODO refine naming convention
'''
# specify the URL of the archive here 
archive_url = "https://www.phoenix.gov/cityclerk/publicmeetings/city-council-meetings#"
driver = webdriver.Firefox()

pagertext='Page 1 of 12'
while pagertext!='Page 12 of 12':
	
	driver.get(archive_url)
	html = driver.page_source
	#create beautiful-soup object 
	soup = BeautifulSoup(html,'html.parser')
	# find all links on web-page 
	pdfs = soup.findAll('a',attrs={'class': 'ico pdf'})
	pager= soup.find('span',attrs={'class':"ms-promlink-button-inner"})
	#print ('window opened')
	pagertext=pager.text
	#print(pager.text)
	xpath='/html/body/form/div[4]/div[2]/div[3]/span/div[1]/div/div/div/div/div[3]/div/div/div/div/div/div[2]/div[1]/a[2]'
	btn=driver.find_element_by_xpath(xpath)
	btn.click()
	pdfs = soup.findAll('a',attrs={'class': 'ico pdf'})
	
	btn=driver.find_element_by_xpath(xpath)
	btn.click()
	archive_url = driver.current_url

print('complete')

#driver.close()

