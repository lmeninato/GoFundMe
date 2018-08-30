# -*- coding: utf-8 -*-
"""
Created on Thu Aug 23 23:40:56 2018

@author: loren
"""
from geopy.geocoders import GoogleV3
import pandas as pd
import numpy as np
from time import sleep

headers = ["Url", "Category","Position", "Title", "Location","Amount_Raised", "Goal", "Number_of_Donators",
           "Length_of_Fundraising", "FB_Shares", "GFM_hearts", "Text", "Latitude", "Longitude"]

df = pd.read_csv('GFM_data.csv', sep = '\t', encoding = 'latin1')

df = df.drop_duplicates()
df = df.drop(df.columns[0], axis=1)
df.columns = headers
df = df.reset_index(drop=True)

geolocator = GoogleV3()

latitudes = np.repeat('', len(df))
longitudes = np.repeat('', len(df))

start = 0
for i in range(start,len(df)):
    try:
        print("Getting latitude %s" %(i+1))
        latitude = geolocator.geocode(df['Location'][i]).latitude
        
        print("Getting longitude %s" %(i+1))
        longitude = geolocator.geocode(df['Location'][i]).longitude
        
    except:
            
        sleep(60)
        
        try:
            latitude = geolocator.geocode(df['Location'][i]).latitude
            longitude = geolocator.geocode(df['Location'][i]).longitude
            
        except:
            latitude = ''
            longitude = ''
            sleep(300)
            while latitude == '':
                try:
                    latitude = geolocator.geocode(df['Location'][i]).latitude
                    longitude = geolocator.geocode(df['Location'][i]).longitude
                except:
                    latitude = np.nan
                    longitude = np.nan

    print("Latitude: %s" % latitude)
    latitudes = np.append(latitudes, latitude)
    print("Longitude: %s" % longitude)
    longitudes = np.append(longitudes, longitude)
    

df['Latitude'] = latitudes
df['Longitude'] = longitudes

df.to_csv('GFM_data.csv', sep = '\t')
