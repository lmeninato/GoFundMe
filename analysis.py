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

geolocator = Nominatim(user_agent="test")
location = geolocator.geocode("Mapleton, UT")

latitude, longitude = location.latitude, location.longitude

df['Latitude'] = Nominatim(user_agent="test").geocode(df.Location.astype(str)).latitude

df.apply(lambda row: Nominatim(user_agent="test").geocode(row.Location.astype(str)).latitude)

latitudes = np.array([])
longitudes = np.array([])

for i in range(len(df)):
    latitude = geolocator.geocode(df['Location'][i]).latitude
    longitude = geolocator.geocode(df['Location'][i]).longitude
    latitudes = np.append(latitudes, latitude)
    longitudes = np.append(longitudes, longitude)