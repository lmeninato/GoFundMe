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

start = 700
end = len(df)
for i in range(start, end):
    try:
        print("Getting latitude %s" %(i+1))
        
        location_geocode = geolocator.geocode(df['Location'][i])
        
        latitude = location_geocode.latitude
        
        print("Getting longitude %s" %(i+1))
        longitude = location_geocode.longitude
        
    except:
        
        print("Error: retrying in 60 seconds...")
        
        sleep(60)
        
        try:
            
            location_geocode = geolocator.geocode(df['Location'][i])
            print("Getting latitude (attempt two) %s" %(i+1))

            latitude = location_geocode.latitude
            
            print("Getting longitude (attempt two) %s" %(i+1))
            longitude = location_geocode.longitude
            
        except:
            latitude = np.nan
            longitude = np.nan

    print("Latitude: %s" % latitude)
    latitudes = np.append(latitudes, latitude)
    print("Longitude: %s" % longitude)
    longitudes = np.append(longitudes, longitude)
    
#np.savez("array_dump1", latitudes, longitudes)
#np.savez("array_dump2", latitudes, longitudes)

temp_data = np.load("array_dump1.npz")

temp_lats = temp_data['arr_0']
temp_lats = temp_lats[temp_lats != '']

temp_long = temp_data['arr_1']
temp_long = temp_long[temp_long != '']

temp_data2 = np.load("array_dump2.npz")
temp_lats2 = temp_data2['arr_0']
temp_lats2 = temp_lats2[temp_lats2 != '']

temp_long2 = temp_data2['arr_1']
temp_long2 = temp_long2[temp_long2 != '']

all_lats = temp_lats.tolist() + temp_lats2.tolist()
all_longs = temp_long.tolist() + temp_long2.tolist()

df['Latitude'] = all_lats
df['Longitude'] = all_longs

df.to_csv('GFM_data.csv', sep = '\t')



