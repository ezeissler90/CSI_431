# -*- coding: utf-8 -*-
"""
Created on Thu Apr 02 15:10:42 2015

@author: Eric
"""
import json
from LocationResolver import LocationResolver

# Returns True if successful, false otherwise
def location_filter(location, db, s_coll, t_coll):
    ## list of tweets
    tweets = list(s_coll.find())
    
    resolver = LocationResolver.getLocationResolver()
    for tweet in tweets:
        try:
        ##   IDEA:  GUI to choose different locations
        ##          -> Just put locations into list
        ##          -> GUI button chooses which location (list index)
        ##          --> i.e. locations = [in_USA, in_CANADA, in_XYZ]
        ##          ---> maybe get complete listing of locations from carmen?
            #tweet = json.loads(tweet)
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
            ##print "No Place key"
            pass
    #successful if made it here        
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