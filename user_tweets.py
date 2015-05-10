__author__ = 'Anthony'

import pymongo
from pymongo import MongoClient

def combine_tweets(user_tweets):
    print len(user_tweets)
    if len(user_tweets) == 0:
        print "Error: no tweets for user"
        return

    combined = user_tweets[0]

    if len(user_tweets) > 1:
        for tweet in user_tweets[1:]:
            text = combined["text"] + " " + tweet["text"]
            combined["text"] = text

    return combined

def insert_all(collection, user_collect, id):
    user_tweets = []
    for tweet in collection.find({"user.id" :  id}):
        user_tweets.append(tweet)

    # print "All tweets:"
    # for tweet in user_tweets:
    #     print tweet

    combined = combine_tweets(user_tweets)

    # print "Combined Record:"
    # print combined

    u = combined["user"]

    combined["_id"] = u["id"]

    user_collect.insert_one(combined)

def main():
    client = MongoClient('52.5.211.193', 27017)
    db = client['corpus']
    collection = db['filtered_tweets']
    user_collect = db['user_tweets']

    count_user = 0
    count_checked = 0

    for tweet in collection.find():
        count_checked += 1

        user = tweet["user"]

        #test if the user is already in the user collection
        if user_collect.find({"_id" :  user["id"]}).count() == 0:
            count_user += 1
            print "Adding user: ", user["id"]
            insert_all(collection, user_collect, user["id"])

    print "checked: ", count_checked
    print "num users added: ", count_user

if __name__ == '__main__':
    main()