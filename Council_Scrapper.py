import requests 
from bs4 import BeautifulSoup 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import os
import re
import sys
''' 
Downloads pdf from city of Phoenix meetings
Shoudl be lauched weekly
Nameing convetion is YYYYMMDD Meeting type Document type
	exampel 20190503 Formal Agenda

TODO refine naming convention
'''
#Changes to streamline code
# specify the URL of the archive here 
archive_url = "https://www.phoenix.gov/cityclerk/publicmeetings/city-council-meetings#"
driver = webdriver.Firefox()

"""
insert FrameSwitch
"""
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
	
	print(pager.text) #prints current page
	for x in pdfs:
		"""
		Creates naming conventions for files
		"""
		toparse=str(x.get('title')) #Turns titles into string to be maniuplated
		toparse=toparse.replace('Meeting ','')
		toparse=toparse.replace('PDF','')
		toparse=toparse.replace('Session ','')
		toparse=toparse.replace('AM','')
		toparse=toparse.replace('PM','')
		date_extract=re.search(r'\d{1,2}''/''\d{1,2}''/''\d{4}',toparse) # extracts date
		time_extract=re.search(r'(1[0-2]|0?[1-9]):([0-5]?[0-9])(:[0-5]?[0-9])?  ',toparse) #extracts time from title
		toparse=toparse.replace(date_extract.group(),'') #Removes date form string
		docs=str(x.get('href')) #Turns links into strings
		date=date_extract.group()#assisngs date to dariable to ve formated
		if time_extract!=None: # Checks of Title has time or not
			toparse=toparse.replace(time_extract.group(),'')
			formated_date=datetime.strptime(date, '%m/%d/%Y').strftime('%Y%m%d') #converts date to yyyymmdd format
			filename=formated_date+toparse
		else: #if title has no 
			toparse=toparse.replace('10:00:00 ','') #Removes the time of 10:00:00 from Avation meetings
			toparse=toparse.replace('9:00:00 ','') #Removes the time of 9:00:00 from Avation meetings
			formated_date=datetime.strptime(date, '%m/%d/%Y').strftime('%Y%m%d') #converts date to yyyymmdd format
			filename=formated_date+toparse
		filename=filename.strip()
		if filename[8]!=' ':
			K=filename.split(filename[8])
			filename=K[0]+' '+filename[8]+K[1]

		downloadfiles=requests.get('https://www.phoenix.gov'+docs)	#creates the pdfs to be documented
		alreadyexist=0
		if os.path.exists('/Users/michael/Google Drive/CityCouncil/'+filename+'.pdf'): #Checks if file has already been downloaded
			print(filename+'.pdf already exist')
			"""
			TODO do a check that ends program
			"""
		else:
			with open('/Users/michael/Google Drive/CityCouncil/'+filename+'.pdf', 'wb') as f:
	   			f.write(downloadfiles.content)
			print(filename+ ' has been downloaded')
	xpath='/html/body/form/div[4]/div[2]/div[3]/span/div[1]/div/div/div/div/div[3]/div/div/div/div/div/div[2]/div[1]/a[2]'
	btn=driver.find_element_by_xpath(xpath)
	btn.click()

print('Download(s) complete')
driver.close()
"""


"""
