# -*- coding: utf-8 -*-
"""
Created on Thu Apr 09 22:29:38 2015

@author: Eric
"""

from pymongo import MongoClient
from Tkinter import *

#TODO: scalable canvas

class Classifier(Frame):        
    ### app methods    \
    def count_update(self):
        if 'id' in self.curr_tweet:
            x = self.var.get()
            x += 1
            self.var.set(x)
        return
        
    def positive(self):
        self.curr_tweet['class'] = 1.0
        if 'id' in self.curr_tweet:
            self.p.update({'id': self.curr_tweet['id']}, {"$set": self.curr_tweet}, upsert = False)
        self.count_update()
        self.clear_and_load()
        return
    
    def negative(self):
        self.curr_tweet['class'] = -1.0
        if 'id' in self.curr_tweet:
            self.p.update({'id': self.curr_tweet['id']}, {"$set": self.curr_tweet}, upsert = False)
        self.count_update()
        self.clear_and_load()
        return
    
    def clear_and_load(self):
        self.secret.delete(1.0, END)
        self.get_next_unclassified()
        self.secret.insert(INSERT, self.curr_tweet['text'])
        return
        
    def next_tweet(self):
        self.position +=1
        if self.position < self.p.count():
            self.curr_tweet = self.tweets[self.position]
        else: return False
        return True
        
    def get_next_unclassified(self):
        while 'class' in self.curr_tweet:
            if not self.next_tweet():
                self.curr_tweet = {'text': "No tweets remaining."}
            else:
                self.tvar.set(self.position+1)
        return

    def createWidgets(self):
        self.wh = '15'
        self.ww = '60'
        
        
        self.left = Frame(self, bg = "#4A245E")
        
        self.tcl = Label(self.left, text="Number of tweets classified this session: ", bg = "#4A245E")
        self.tcl.grid(row=0, column=0, padx=3)        
        self.tcount = Entry(self.left, textvariable=self.var, width=8)
        self.tcount.grid(row=1, column=0, padx=3)
        
        if self.position >= self.p.count():
            self.tvar.set(self.position)
        else: self.tvar.set(self.position+1)
        
        self.tn = Label(self.left, text="Number of tweets classified this session: ", bg = "#4A245E")
        self.tn.grid(row=2, column=0, padx=3)
        self.tnum = Entry(self.left, textvariable=self.tvar, width=8)
        self.tnum.grid(row=3, column=0, padx=3)
        self.left.grid(row=0, column=0, rowspan=2)
        ##### Secret #####
        self.secret = Text(self, height=self.wh, width=self.ww, bg = "#E0AA0F", borderwidth = 2, wrap="word")
        self.secret.grid(row = 0, column = 1, rowspan = 2, sticky ='N', padx = 10, pady = 3)
        #self.get_next_unclassified()
        self.secret.insert(INSERT, self.curr_tweet['text'])
        
        ## Area 6        
        self.classify_yes = Button(self, text="Positive", command=self.positive)
        self.classify_yes.grid(row = 0, column = 3, sticky='S'+'W'+'E', pady=10, padx=5)
        
        self.classify_no = Button(self, text="Negative", command=self.negative)
        self.classify_no.grid(row = 1, column = 3, sticky='N', pady=10, padx=5)
        
    def __init__(self, master=None):
        Frame.__init__(self, master, bg = "#4A245E")
        self.client = MongoClient()
        ## hardcode database name 'test_database
        self.db = self.client.test_database
        ## hardcode collection name 'posts'
        self.p = self.db.posts
        self.position = 0
        self.tweets = self.p.find()
        self.curr_tweet = self.tweets[0]
        self.tvar = IntVar(0)
        self.var = IntVar(0)
        self.get_next_unclassified()
        self.pack()
        self.createWidgets()
        
def main():
    root = Tk()
    app = Classifier(master=root)
    app.mainloop()
    
if __name__ == '__main__':
    main()