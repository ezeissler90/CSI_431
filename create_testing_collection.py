__author__ = 'Anthony'


import pymongo
from pymongo import MongoClient

def main():
    client = MongoClient('52.5.211.193', 27017)
    db = client['corpus']
    user_tweets = db['user_tweets']
    testing_tweets = db['testing_tweets']

    #pos_tweets = user_tweets.find({"mental_illness" : 1}).count()
    #neg_tweets = user_tweets.find({"mental_illness" : 1}).count()

    for tweet in user_tweets.find({"mental_illness" : 1}):
        testing_tweets.insert_one(tweet)
    for tweet in user_tweets.find({"mental_illness" : -1}):
        testing_tweets.insert_one(tweet)


if __name__ == '__main__':
    main()