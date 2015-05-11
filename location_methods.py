# -*- coding: utf-8 -*-
"""
Created on Thu Apr 02 15:10:42 2015

@author: Eric
"""
import json
from LocationResolver import LocationResolver

def execute(range):
    for tweet in s_coll.find(range[0]:range[1]):
        try:
            ##   IDEA:  GUI to choose different locations
            ##          -> Just put locations into list
            ##          -> GUI button chooses which location (list index)
            ##          --> i.e. locations = [in_USA, in_CANADA, in_XYZ]
            ##          ---> maybe get complete listing of locations from carmen?
            if 'mental_illness' not in tweet:
                tweet['mental_illness'] = 0
            if 'physical_illness' not in tweet:
                tweet['physical_illness'] = 0
            loc = resolver.resolveLocationFromTweet(tweet)
            if getBool(loc, location):
                if not list(t_coll.find({ 'id': tweet['id'] })):
                    if not t_coll.insert(tweet):
                        return False
        except:
            pass

# Returns True if successful, false otherwise
def location_filter(location, db, s_coll, t_coll):
    from multiprocessing import Pool
    ## list of tweets
    resolver = LocationResolver.getLocationResolver()
    count = s_coll.find().count()
    p = Pool(10)
    start_index = 0
    end_index = 0
    for i in xrange(0, 10, 1):
        end_index += count / 10.0
        p.map(execute, [start_index, end_index])
        start_index = end_index
    return True

## Determines whether the tweet_loc tweet location matches any contained
##      in the q_loqs location list.
def getBool(tweet_loc, q_locs):
    ## Trivially matches
    if not q_locs:
        return true

    for item in q_locs:
        if str(item).lower() == str(tweet_loc.getCountry().strip('\n').lower()):
            return True
    return False
