# -*- coding: utf-8 -*-
"""
Created on Thu Aug 23 23:40:56 2018

@author: loren
"""

from geopy.geocoders import Nominatim
import pandas as pd
import numpy as np

headers = ["Url", "Category","Position", "Title", "Location","Amount_Raised", "Goal", "Number_of_Donators", "Length_of_Fundraising", "FB_Shares", "GFM_hearts", "Text"]

df = pd.read_csv('GFM_data.csv', sep = '\t')

df = df.drop_duplicates()
df = df.drop(df.columns[0], axis=1)
df.columns = headers
df = df.reset_index(drop=True)

geolocator = Nominatim(user_agent="test")

latitudes = np.array([])
longitudes = np.array([])

for i in range(len(df)):
    try:
        latitude = geolocator.geocode(df['Location'][i]).latitude
        longitude = geolocator.geocode(df['Location'][i]).longitude
    except:
        latitude = np.nan
        longitude = np.nan
    print("Getting latitude %s" %(i+1))
    latitudes = np.append(latitudes, latitude)
    print("Getting longitude %s" %(i+1))
    longitudes = np.append(longitudes, longitude)
    
df['Latitude'] = latitudes
df['Longitude'] = longitudes

df.to_csv('GFM_data.csv', sep = '\t')
