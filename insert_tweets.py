# -*- coding: utf-8 -*-
"""
Created on Wed Apr 01 18:21:30 2015

@author: Eric
"""

from LocationResolver import *
from pymongo import MongoClient

client = MongoClient()
db = client.test_database
posts = db.posts

tk = {}
tk1 = {}
tk2 = {}
for line in open('CrimeReport.txt').readlines():
    tweet = json.loads(line)
    
    ## Can't change the size (add/delete) of dictionaries
    ## while in a loop
    tk = tweet.copy()
    for key in tweet:
        new_key = key
        if key.find('.'):
            new_key = key.replace(".", "_")
            tk[new_key] = tk.pop(key)

        
        t = tk[new_key]
        if isinstance(t, dict):
            ## create copy
            tk1 = t.copy()
            for ke in t:
                new_key_2 = ke
                if ke.find('.'):
                    new_key_2 = ke.replace(".", "_")
                    tk1[new_key_2] = tk1.pop(ke)
                    tk[new_key] = tk1
                

                tt = tk1[new_key_2]
                if isinstance(tt, dict):
                    ## create copy
                    tk2 = tt.copy()
                    for k in tt:
                        if k.find('.'):
                            new_key_3 = k.replace(".", "_")
                            tk2[new_key_3] = tk2.pop(k)
                            tk1[new_key_2] = tk2
                            tk[new_key] = tk1
    
    try:
        post_id = posts.insert(tk)
    except:
        raise
        print "Insert did not work"
    print '------------------------------'
