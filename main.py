# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
import numpy as np
import pandas as pd
import re

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
    
    temp_url = {}#grab category as well
    i = 1
    
    for container in containers:
        for link in container.find_all('a'):
            temp_url[link.get('href')] = i
            i = i +1 
            
    temp_url = {k: ((v // 2) - 1) // 3  for k, v in temp_url.items()} #


    return(temp_url)

#generate lists of list of URL per category

def list_urls(MoreGFMclicks = 5):
    GFM_urls = []
    for url in categories_urls:
        GFM_urls.append(extract_urls_from_categories(url, MoreGFMclicks = 5))
    print("All done!")
    return(GFM_urls)

GFM_urls = list_urls()

mydf = pd.DataFrame(columns = ["Url", "Position"])
for cat in GFM_urls:
    temp_val = np.array(list(cat.values()))
    temp_key = np.array(list(cat.keys()))
    temp_df = pd.DataFrame(columns = ["Url", "Position"])
    temp_df["Position"] = temp_val
    temp_df["Url"] = temp_key
    mydf = mydf.append(temp_df)

#flatten list

mydf.to_csv('GFM_scrape.csv', sep='\t')

#need to scrape a single url now

url = 'https://www.gofundme.com/rickmuchow'
category = mydf #extract category from mydf

driver = webdriver.Chrome('C:/webdriver/chromedriver.exe')
driver.get(url)

source = driver.page_source

driver.close()

soup = BeautifulSoup(source, 'lxml')
#contains amount raised - goal amount - # of donators - length of fundraising
container = soup.find_all("div",{"class":"layer-white hide-for-large mb10"})
info_string = container[0].text
info_string = info_string.splitlines()
info_string = list(filter(None, info_string))

amount_raised = int(info_string[0][1:].replace(',',''))

goal = re.findall('\$(.*?) goal', info_string[1])[0]

NumDonators = re.findall('by (.*?) people', info_string[2])[0]

timeFundraised = re.findall("in (.*)$", info_string[2])[0]

title_container = soup.find_all("h1",{"class":"campaign-title"})#<h1 class="campaign-title">Help Rick Muchow Beat Cancer</h1>
title = title_container[0].text

text_container = soup.find_all("div",{"class":"co-story truncate-text truncate-text--description js-truncate"})
all_text = text_container[0].text
all_text = list(filter(None,all_text.splitlines()))[0]

FB_shares_container = soup.find_all("strong", {"class":"js-share-count-text"})
FB_shares = FB_shares_container[0].text.splitlines()
FB_shares = FB_shares[1].replace(" ", "").replace("\xa0", "")

hearts_container = soup.find_all("div", {"class":"campaign-sp campaign-sp--heart fave-num"})
hearts = hearts_container[0].text

location_container = soup.find_all("div", {"class":"pills-contain"})
location = location_container[0].text.splitlines()[-1]
location = location.replace('\xa0', '').strip()

