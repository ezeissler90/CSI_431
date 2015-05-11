# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 21:18:23 2015

@author: Eric
"""

import json, sys, string
import numpy as np
from sklearn import svm
from sklearn.grid_search import GridSearchCV
from datetime import datetime
from pymongo import MongoClient
import pickle

def readFromFile(filename):
    tweets = []
    for line in open(filename, 'r').readlines():
        tweet = json.loads(line)
        tweets.append(tweet)
    return tweets
    
def get_freq(astr):
    stopwords = ["a", "about", "above", "above", "across", "after", "afterwards", "again", "against", "all", "almost", "alone", "along", "already", "also","although","always","am","among", "amongst", "amoungst", "amount",  "an", "and", "another", "any","anyhow","anyone","anything","anyway", "anywhere", "are", "around", "as",  "at", "back","be","became", "because","become","becomes", "becoming", "been", "before", "beforehand", "behind", "being", "below", "beside", "besides", "between", "beyond", "bill", "both", "bottom","but", "by", "call", "can", "cannot", "cant", "co", "con", "could", "couldnt", "cry", "de", "describe", "detail", "do", "done", "down", "due", "during", "each", "eg", "eight", "either", "eleven","else", "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except", "few", "fifteen", "fify", "fill", "find", "fire", "first", "five", "for", "former", "formerly", "forty", "found", "four", "from", "front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his", "how", "however", "hundred", "ie", "if", "in", "inc", "indeed", "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter", "latterly", "least", "less", "ltd", "made", "many", "may", "me", "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", "much", "must", "my", "myself", "name", "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own","part", "per", "perhaps", "please", "put", "rather", "re", "same", "see", "seem", "seemed", "seeming", "seems", "serious", "several", "she", "should", "show", "side", "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "such", "system", "take", "ten", "than", "that", "the", "their", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they", "thickv", "thin", "third", "this", "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards", "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", "were", "what", "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "with", "within", "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves", "the"]
    
    freq = dict()
    for term in astr.split(" "):
        term.encode("utf8")
        #table = string.maketrans("","")
        term = term.translate({ord(k): u"" for k in string.punctuation})
        term = string.lower(term)
        while term.find(u""):
            a = term.find(u"")
            t1 = term[:a]
            t2 = term[a:]
            term = t1 + t2
            
            print term
        if len(term) > 2 and term not in stopwords:
            if term in freq:
                freq[term] += 1
            else:
                freq[term] = 1
    
    return freq
    
def set_freq(freq):
    
    pass
    
def getDataFromCollection(db, coll, min_freq):
    f = open('training_data.txt', 'w')
    tweets = []
    for tweet in coll.find():
        if tweet.has_key('mental_illness'):
            if int(tweet['mental_illness']) == 1:
                t_id = long(tweet['id'])
                
                tweet['freq'] = get_freq(tweet['text'])
                ## freq assumes tweet['freq'] is a dict() object
                #t_freq = clean(min_freq, tweet['freq'])
                t_freq = tweet['freq']
                
                t_class = float(tweet['mental_illness'])
                #_class = float(tweet['physical_illness'])
                
                tweetline = [t_id, t_freq, t_class]
                f.write(json.dumps(tweetline) + '\n')
                tweets.append(tweetline)
                if len(tweets) == 38:
                    break
        
    num_pos = len(tweets)
    print num_pos, "positive tweets"
    sys.stdout.flush()
                
    for tweet in coll.find():
        if tweet.has_key('mental_illness'):
            if int(tweet['mental_illness']) == -1:
                t_id = long(tweet['id'])
                
                tweet['freq'] = get_freq(tweet['text'])
                ## freq assumes tweet['freq'] is a dict() object
                #t_freq = clean(min_freq, tweet['freq'])
                t_freq = tweet['freq']
                
                t_class = float(tweet['mental_illness'])
                #_class = float(tweet['physical_illness'])
                
                tweetline = [t_id, t_freq, t_class]
                f.write(json.dumps(tweetline) + '\n')
                tweets.append(tweetline)
                if len(tweets) >= (3 * num_pos):
                    f.close()
                    print len(tweets), "all tweets"
                    sys.stdout.flush()
                    return tweets
    
    f.close()
    print "Should not have made it here. Uh Oh"
    sys.stdout.flush()
    return tweets
    
def add_freq_to_tweets(db, coll, freq):
    pass
    

def set_train_data(pfile, nfile):
    p_t_d = readFromFile(pfile)
    n_t_d = readFromFile(nfile)
    
    t_d = p_t_d + n_t_d
    
    clss = [1.0 for i in range(len(p_t_d))] + [-1.0 for i in range(len(n_t_d))]

    return t_d, clss

def get_vocab_freq(tweets):
    vocab = dict()
    for tweet in tweets:
        for term in tweet[1]:
            term = string.lower(term)

            if vocab.has_key(term):
                vocab[term] += tweet[1][term]
            else:
                vocab[term] = tweet[1][term]
    return vocab
    
        
def clean(min_clean, vocab):
    pop = []
    for key in vocab:
        if vocab[key] < min_clean:
            pop.append(key)
            
    for item in pop:
        del vocab[item]
    '''
    counter = 0
    for key in vocab:
        a = []
        a.append(counter)
        a.append(vocab[key])
        vocab[key] = a
        counter += 1
    '''
    #vocab = {term: freq for term, freq in vocab.items() if min_clean > 15}    
    return vocab

def predict(astr, vocab, svmm):
        astr_freq = get_freq(astr)
        x = [0] * len(vocab)
        for term in astr_freq:
            if vocab.has_key(term):
                #print vocab[term]
                x[vocab[term]] += 1
        y = svmm.predict(x)

        return y
    
def main():
    
    startTime = datetime.now()

    min_freq = 0
    
    client = MongoClient('52.5.211.193', 27017)
    db = client.corpus
    tcoll = db.testing_tweets
    
    print "Here 1"
    sys.stdout.flush()
    ## returns list of lists [_id, _freq, _class]
    ## _freq is dictionary { 'term':numTimes }
    
    # getDataFromCollection commented out because it takes an enormous amount
    # of time to run (iterate through collection)
    # Instead, 38 positive tweets and 76 negative tweets are store in 'training_data.txt'
    #training_data = getDataFromCollection(db, tcoll, min_freq)
    # training_data = []
    # for line in open('training_data.txt'):
    #     training_data.append(json.loads(line))
    # print "Here 2"
    # sys.stdout.flush()
    #
    # # All terms in all tweet texts combined
    # vocab = get_vocab_freq(training_data)
    # print len(vocab)
    #
    # # Scrub terms from vocab with less than min_freq
    # vocab = clean(min_freq, vocab)
    # print len(vocab)
    
    '''  A means of trouble shooting
    print "started vocab.txt"
    sys.stdout.flush()
    f = open ('vocab.txt', 'w')
    for item in vocab:
        astr = item + " " + str(vocab[item]) + '\n'
        f.write(astr.encode("utf8"))
    f.close()
    '''
    
    ### This code is commented out when pickle files are used
    '''
    X = []
    vocab_list = [key for key in vocab]
    print len(vocab)
    for tweet in training_data:
        x = [0] * len(vocab)
        #terms = [term for term in tweet.split() if len(term) > 2]
        
        for term in tweet[1]:
            
            if vocab.has_key(term):
                print term, vocab[term], len(x)
                #i = vocab_list.index(term)
                x[vocab_list.index(term)] += 1
        X.append(x)
    print len(X[0]), "# Features"
    classes = [item[2] for item in training_data]
    
    
    linsvm = svm.LinearSVC()
    Cs = range(1, 20)
    ssvm = GridSearchCV(estimator = linsvm, param_grid = dict(C=Cs), cv = 10)
    print len(X), len(X[0]), len(classes)
    ssvm.fit(X, classes)
    svmm = ssvm.best_estimator_
    
    f = open('svmm_model.pkl', 'w')
    f.write(pickle.dumps(svmm))
    f.close()
    f = open('svmm_vocab.pkl', 'w')
    f.write(pickle.dumps(vocab))
    f.close()
    '''
    ### End commented out code
    

    
    svmm = pickle.loads(open('svmm_model.pkl').read())
    vocab = pickle.loads(open('svmm_vocab.pkl').read())
    
    
    predictions = []
    counter = 0
    for tweet in tcoll.find():
        a = predict(tweet['text'], vocab, svmm)
        # if (a[0] == 1):
        #     tcoll.update( {"_id" : tweet["_id"] }, {"$set":{"ment_pred": 1}})
        # else:
        #     tcoll.update( {"_id" : tweet["_id"] }, {"$set":{"ment_pred": 1}})
        tcoll.update( {"_id" : tweet["_id"] }, {"$set":{"ment_pred": a[0]}})
        predictions.append(a)
        counter += 1
        if counter >= 1000:
            break
        
    f = open('preds.txt', 'w')
    for item in predictions:
        f.write(str(item) + '\n')
    f.close()
    
    
    print datetime.now() - startTime
    
if __name__ == '__main__':
    main()