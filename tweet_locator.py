# -*- coding: utf-8 -*-
"""
Created on Wed Apr 01 18:21:30 2015

@author: Eric
"""

from pymongo import MongoClient
from location_method import location_filter

client = MongoClient()
# hardcode database 'test_database'
db = client.test_database

# hardcode collection names 'posts' 'usaers'
s_coll = db.posts   #source
t_coll = db.usaers  #target

## Names of Countries to find tweets for
locs = ["united states"]

success = location_filter(locs, db, s_coll, t_coll)

print success, "<-- True?!?!"
