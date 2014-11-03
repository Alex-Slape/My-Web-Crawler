# -*- coding: utf-8 -*-
'''
Ranker takes in the Appraisers votes, parses the domain of the url, and then
records the results.

author: Alex Slape

'''

from sys import path, stdout
from time import time
path.append("../Messenging/")
path.append("../procname/")
import procname
try:
    from Messenger import Messenger
except:
    print ("Messenger not found")
    raise ImportError



class Ranker():
    
    def __init__(self):
        print ("Initializing Ranker")
        self.map = dict()
        self.last_time = time()
        self.fname = None
        self.url = list()
        self.msg = Messenger()
        self.handleInput()
        
        
    def handleInput(self):
        self.msg.registerForMessage(self.callback, 'keywords')
            
    def callback(self, ch, method, properties, body):
        stdout.flush()
        print body
        tag, keywords, url = self.parseMessage(str(body))
        self.recordSites(url)
        self.updateDict(url, keywords)
        now_time = time()
        if now_time - self.last_time > 120:
            self.recordDict()
            self.last_time = now_time
            
    def parseMessage(self, message):
        #print message
        message = message.split("|divider|")
        if len(message) != 3:
            #print "Abprt"
            #print message
            return "ERROR", "ERROR"
        tag = message[0]
        keywords = message[1]
        url = message[2]
        #print "URL: " + str(url)
        
        return tag, keywords, url
        
    def updateDict(self, url, keywords):
        if not url in self.map:
            self.map[url] = list()
            self.map[url].append(keywords)
        else:
            print "Updating dict"
            self.map[url].append(keywords)
            
    def recordDict(self):
        idx = 0
        if self.fname == None:        
            f = "Engine Results"
            while True:
                self.fname = str(f) + str(idx) + ".txt"
                try:
                    self.myfile = open(self.fname, 'r')
                except:
                    self.myfile = open(self.fname, 'w')
                    break
                idx += 1
        else:
            self.myfile = open(self.fname, 'w')
        print "Writing to File"
        for url in self.map:
            self.myfile.write(str(url) + ": " + str(self.map[url]) + "\n")
        self.myfile.close()
        
    def recordSites(self, site):
        if not site in self.url:
            self.url.append(site)
        if time() - self.last_time > 120:
            urlfile = open("SitesVisited.txt", 'a')
            for site in self.url:
                urlfile.write(str(site) + "\n")
            urlfile.close()
        
if __name__ == "__main__":
    procname.setprocname('Ranker')
    RN = Ranker()
