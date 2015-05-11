__author__ = 'Anthony'

import pymongo
from pymongo import MongoClient

def main():
    client = MongoClient('52.5.211.193', 27017)
    db = client['corpus']
    collection = db['filtered_tweets']

    print "pos: ", collection.find({"mental_illness" :  1}).count()
    print "neg: ", collection.find({"mental_illness" :  -1}).count()
    print "undef: ", collection.find({"mental_illness" :  0}).count()


if __name__ == '__main__':
    main()