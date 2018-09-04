# -*- coding: utf-8 -*-
"""
Created on Thu Aug 23 21:48:43 2018

@author: loren
"""
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
import numpy as np
import pandas as pd

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
#make url_categories
categories_urls = list(map(lambda x:{x:'https://www.gofundme.com/discover/{}-fundraiser'.format(x.lower())}, all_cats))

#process to extract individual gofundme urls from an individual category



mydf = pd.read_csv('GFM_url_list.csv', sep = '\t')

headers = ["Url", "Category","Position", "Title", "Location","Amount_Raised", "Goal", "Number_of_Donators", "Length_of_Fundraising", "FB_Shares", "GFM_hearts", "Text"]
mydf = mydf.reindex(columns = headers)

full_df = pd.DataFrame(columns = headers)

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
    
    temp_url = {}
    i = 1
    
    for container in containers:
        for link in container.find_all('a'):
            temp_url[link.get('href')] = i
            i = i + 1 

    temp_url = {k: ((v // 2) - 1) // 3  for k, v in temp_url.items()} #


    return(temp_url)

#generate lists of list of URL per category

def list_urls(MoreGFMclicks = 5):
    GFM_urls = []
    for url_pair in categories_urls:
        category = list(url_pair.keys())[0]
        url = list(url_pair.values())[0]
        GFM_urls.append([extract_urls_from_categories(url, MoreGFMclicks = 5), category])#get category from categories_urls
    print("All done!")
    return(GFM_urls)

GFM_urls = list_urls()

mydf = pd.DataFrame(columns = ["Url", "Category","Position"])
for cat in GFM_urls:
    
    temp_val = np.array(list(cat[0].values()))
    temp_key = np.array(list(cat[0].keys()))
    temp_category = np.repeat(cat[1], len(cat[0]))
    
    temp_df = pd.DataFrame(columns = ["Url", "Category", "Position"])
    temp_df["Position"] = temp_val
    temp_df["Category"] = temp_category
    temp_df["Url"] = temp_key
    
    mydf = mydf.append(temp_df, ignore_index = True)

#flatten list

mydf.to_csv('GFM_url_list.csv', sep='\t')