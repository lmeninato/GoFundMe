# -*- coding: utf-8 -*-
"""
Created on Thu Aug 23 23:40:56 2018

@author: loren
"""

from geopy.geocoders import Nominatim
import pandas as pd

df = pd.read_csv('GFM_data.csv', sep = '\t')

df = df.drop_duplicates()

geolocator = Nominatim(user_agent="test")
location = geolocator.geocode("Mapleton, UT")

latitude, longitude = location.latitude, location.longitude