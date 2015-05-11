__author__ = 'Anthony'

import pymongo
from pymongo import MongoClient

def main():
    client = MongoClient('52.5.211.193', 27017)
    db = client['corpus']
    user_tweets = db['user_tweets']
    filtered_tweets = db['filtered_tweets']

    for tweet in filtered_tweets.find():
        user = tweet["user"]
        id = user["id"]

        temp = user_tweets.find_one({"_id" : id })

        if ("mental_illness" not in temp) or (temp["mental_illness"] == 0 and tweet["mental_illness"] != 0):
            user_tweets.update( {"_id" : id }, {"$set":{"mental_illness": tweet["mental_illness"], "physical_illness": tweet["physical_illness"]}})
            print "updated: ", id
        else:
            print "skipped: ", id

if __name__ == '__main__':
    main()