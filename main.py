# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
import csv


url = 'https://www.gofundme.com/discover'
driver = webdriver.Chrome('C:/webdriver/chromedriver.exe')
driver.get(url)
for elem in driver.find_elements_by_link_text('Show all categories'):
        try:
            elem.click()
            print('Succesful click')
        except:
            print('Unsuccesful click')
            
source = driver.page_source

driver.close()

soup = BeautifulSoup(source, 'lxml')
cat_containers = soup.findAll("div", {"class": "section-categories grid-x small-up-2 medium-up-3 large-up-6"})
categories = cat_containers[0].text #contains category names for this section
categories = categories.splitlines()
categories = list(filter(None, categories))

more_containers = soup.findAll("div", {"class": "section-categories grid-x small-up-2 medium-up-3 large-up-6 js-more-categories"})
more_cats = more_containers[0].text
more_cats = more_cats.splitlines()
more_cats = list(filter(None, more_cats))

all_cats = categories + more_cats # should be len(all_cats) == 18
lower_cats = list(map(lambda x: x.lower(), all_cats))

#make url_categories
categories_urls = list(map(lambda x:'https://www.gofundme.com/discover/{}-fundraiser'.format(x), lower_cats))





#process to extract individual gofundme urls from an individual category
#----------------------------repeat for all categories-------------------

def extract_urls_from_categories(url, MoreGFMclicks = 5):
    
    # eg. url = 'https://www.gofundme.com/discover/medical-fundraiser'
    driver = webdriver.Chrome('C:/webdriver/chromedriver.exe')
    driver.get(url)
    
    for i in range(MoreGFMclicks):
        for elem in driver.find_elements_by_link_text('Show More'):
            try:
                elem.click()
                print('Succesful click %s' %(i+1))#make this more useful- say what category it is e.g. url.get_category()
            except:
                print('Unsuccesful click %s' %(i+1))
                
            sleep(0.8) #longer delay - more succesful
            
    source = driver.page_source
        
    driver.close()
    
    soup = BeautifulSoup(source, 'lxml')
    
    
    containers = soup.findAll("div", {"class": "cell grid-item small-6 medium-4 js-fund-tile"})
    container = containers[0]
    temp_url = []
    for container in containers:
        for link in container.find_all('a'):
            temp_url.append(link.get('href'))

    return(temp_url)
#--------------------------repeat for all categories----------------------
GFM_urls = []
for url in categories_urls:
    GFM_urls.append(extract_urls_from_categories(url, MoreGFMclicks = 5))
print("All done!")

GFM_urls_list = [item for sublist in GFM_urls for item in sublist]
GFM_urls_list = list(set(GFM_urls_list))

csv_file = open('cms_scrape.csv', 'w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(GFM_urls_list)
csv_file.close()

#need to scrape a single url now





