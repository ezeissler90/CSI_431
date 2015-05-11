__author__ = 'Anthony'

import pymongo
from pymongo import MongoClient


def main():
    client = MongoClient('52.5.211.193', 27017)
    db = client['corpus']
    collection = db['user_tweets']

    for tweet in collection.find({"mental_illness": 1}):
        vocab = dict()
        text = tweet["text"]
        #print "original: ", text
        for word in text.split():
            try:
                word = word.decode('ascii')
                if ( (not ("http" in word)) and (not ("@" in word) ) and (not any(char.isdigit() for char in word)) ):
                    word = word.strip(".@#!&()[]{}\":?\\\/-_|<>,'")
                    word = word.lower()
                    # print word
                    if (word != 'rt'):
                        if word in vocab:
                            vocab[word] += 1
                        else:
                            vocab[word] = 1
            except:
                print "skipped: ", word
        #print vocab
        #print

        collection.update( {"_id" : tweet["_id"] }, {"$set":{"vocab": vocab}})


if __name__ == '__main__':
    main()