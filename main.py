# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import requests
import re

mydf = pd.read_csv('GFM_url_list.csv', sep = '\t')

headers = ["Url", "Category","Position", "Title", "Location","Amount_Raised", "Goal", "Number_of_Donators", "Length_of_Fundraising", "FB_Shares", "GFM_hearts", "Text"]
mydf = mydf.reindex(columns = headers)

full_df = pd.DataFrame(columns = headers)
#need to scrape a single url now


def scrape_url(row_index):
    single_row = mydf.iloc[row_index]
    url = single_row["Url"]
    category = single_row["Category"]
    position = single_row["Position"]
    
    page = requests.get(url)
         
    soup = BeautifulSoup(page.text, 'lxml')
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
    
    text_container =  soup.find('meta', attrs={'name': 'description'})
    
    try:
        all_text = text_container['content']
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


def scrape_all_urls(file = 'GFM_data.csv', start = 0, end = len(mydf)):
    for i in range(start, end):
        temp_df = scrape_url(i)
        temp_df.to_csv(file, mode = 'a',sep = '\t', header = False)
        print("Scraping url %s" %(i+1))
        
scrape_all_urls()
