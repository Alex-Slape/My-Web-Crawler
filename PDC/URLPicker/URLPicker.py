# -*- coding: utf-8 -*-
'''
URL Picker takes in a set number of urls, picks the five most optimal ones and
feeds them back into NAPI

author: Alex Slape

'''
from sys import path, stdout
path.append("../Messenging/")
path.append("../procname/")
import procname
try:
    from Messenger import Messenger
except:
    print "Messenger not found"
    raise ImportError

MAX_LISTS = 10
SEND_LISTS = 10

BAD_DOMAIN = "bad"

class URLPicker():
    
    def __init__(self):
        print "Initializing URL Picker"
        self.urls = list()
        self.prev_domain = list()
        self.msg = Messenger()
        self.handleInput()
        
    def handleInput(self):
        self.msg.registerForMessage(self.callback, 'found_url')
            
    def callback(self, ch, method, properties, body):
        stdout.flush()
        self.urls.append(str(body))       
        if len(self.urls) > MAX_LISTS:
            self.pickURLs()
            self.urls = list()
            
    def pickURLs(self):
        
        domains_sent = 0        
        for url in self.urls:
            curr_domain = url
            if not curr_domain in self.prev_domain:
                self.msg.writeMessage(url, 'url')
                print "New Domain: " + str(url)
                self.prev_domain.append(curr_domain)
                domains_sent += 1
            else:
                print "Same as last Domain"
            #if domains_sent >= SEND_LISTS:
                #print "Done with URLS"
                #return
        if domains_sent == 0:
            self.msg.writeMessage(self.urls[-1], 'url')
    
    def getDomain(self, address):
        sep_str = address.split(".")
        if len(sep_str) < 2:
            return BAD_DOMAIN
        elif len(sep_str) == 2:
            return BAD_DOMAIN
        return sep_str[1]
    
if __name__ == "__main__":
    procname.setprocname('URLPicker')
    UP = URLPicker()

