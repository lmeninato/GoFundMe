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
#make url_categories
categories_urls = list(map(lambda x:{x:'https://www.gofundme.com/discover/{}-fundraiser'.format(x.lower())}, all_cats))

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

mydf.to_csv('GFM_scrape.csv', sep='\t')

headers = ["Url", "Category","Position", "Title", "Location","Amount_Raised", "Goal", "Number_of_Donators", "Length_of_Fundraising", "FB_Shares", "GFM_hearts", "Text"]
mydf = mydf.reindex(columns = headers)


full_df = pd.DataFrame(columns = headers)
#need to scrape a single url now

def scrape_url(row_index):
    single_row = mydf.iloc[row_index]
    url = single_row["Url"]
    category = single_row["Category"]
    position = single_row["Position"]
    
    driver = webdriver.Chrome('C:/webdriver/chromedriver.exe')
    driver.get(url)
    
    source = driver.page_source
    
    driver.close()
    
    soup = BeautifulSoup(source, 'lxml')
    #contains amount raised - goal amount - # of donators - length of fundraising
    try:
        container = soup.find_all("div",{"class":"layer-white hide-for-large mb10"})
        info_string = container[0].text
        info_string = info_string.splitlines()
        info_string = list(filter(None, info_string))
        
        amount_raised = int(info_string[0][1:].replace(',',''))
        
        goal = re.findall('\$(.*?) goal', info_string[1])[0]
        
        NumDonators = re.findall('by (.*?) people', info_string[2])[0]
        
        timeFundraised = re.findall("in (.*)$", info_string[2])[0]
    except:
        amount_raised = np.nan
        goal = np.nan
        NumDonators = np.nan
        timeFundraised = np.nan
        
    
    title_container = soup.find_all("h1",{"class":"campaign-title"})#<h1 class="campaign-title">Help Rick Muchow Beat Cancer</h1>
    
    try:
        title = title_container[0].text
    except:
        title = np.nan
    
    text_container = soup.find_all("div",{"class":"co-story truncate-text--description js-truncate"})
    
    try:
        all_text = text_container[0].text
        all_text = list(filter(None,all_text.splitlines()))[0]
    except:
        all_text = np.nan
    
    try:
        FB_shares_container = soup.find_all("strong", {"class":"js-share-count-text"})
        FB_shares = FB_shares_container[0].text.splitlines()
        FB_shares = FB_shares[1].replace(" ", "").replace("\xa0", "")
    except:
        FB_shares = np.nan
        
    try:
        hearts_container = soup.find_all("div", {"class":"campaign-sp campaign-sp--heart fave-num"})
        hearts = hearts_container[0].text
    except:
        hearts = np.nan
    
    try:
        location_container = soup.find_all("div", {"class":"pills-contain"})
        location = location_container[0].text.splitlines()[-1]
        location = location.replace('\xa0', '').strip()
    except:
        location = np.nan
        
    temp_row = np.array([[url, category, position, title, location, amount_raised, goal, NumDonators, timeFundraised, FB_shares, hearts, all_text]])
    temp_df = pd.DataFrame(temp_row, columns = headers)
    
    return(temp_df)
    
#full_df = full_df.append(scrape_url(0), ignore_index = True)

def scrape_all_urls():
    full_df = pd.DataFrame(columns = headers)
    for i in range(len(mydf)):
        full_df = full_df.append(scrape_url(i), ignore_index = True)
    return(full_df)

full_df = scrape_all_urls()
