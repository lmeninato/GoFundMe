# -*- coding: utf-8 -*-
"""
Created on Sat Sep  1 18:49:45 2018

@author: Pablo
"""

import pandas as pd
import numpy as np

headers = ["Url", "Category","Position", "Title", "Location","Amount_Raised", "Goal", "Number_of_Donators",
           "Length_of_Fundraising", "FB_Shares", "GFM_hearts", "Text", "Latitude", "Longitude"]

df = pd.read_csv('GFM_data.csv', sep = '\t', encoding = 'latin1')

