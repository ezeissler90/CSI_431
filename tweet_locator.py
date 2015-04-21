# -*- coding: utf-8 -*-
"""
Created on Wed Apr 01 18:21:30 2015

@author: Eric
"""

from pymongo import MongoClient
from location_methods import location_filter

client = MongoClient('52.5.211.193', '27017')

# hardcode database 'corpus'
db = client.corpuse

# hardcode collection names 'twitter' 'filtered_tweets'
s_coll = db.twitter   #source
t_coll = db.filtered_tweets  #target

## Names of Countries to find tweets for
locs = ["united states"]

success = location_filter(locs, db, s_coll, t_coll)

print success, "<-- True?!?!"
