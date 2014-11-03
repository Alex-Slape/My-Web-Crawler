# -*- coding: utf-8 -*-
'''
Organizer takes in raw html input and organizes it into messages representing
links, header, body, and etc.

author: Alex Slape

'''
from HTMLParser import HTMLParser
from sys import path, stdout
from random import Random
path.append("../Messenging/")
path.append("../procname/")
import procname
try:
    from Messenger import Messenger
except:
    print "Messenger not found"
    raise ImportError

MANY_TO_SEARCH = 2

class Organizer(HTMLParser):
    
    def __init__(self):
        HTMLParser.__init__(self)
        print "Initializing Organizer"
        self.data = dict() #form of (tag, list of data)
        self.tag_list = ['title', 'meta','a']
        self.msg = Messenger()
        self.rand = Random()
        self.rand.seed()
        self.sent_urls = 0
        self.url = None
        self.handleInput()

    def handleInput(self):
        self.msg.registerForMessage(self.callback, 'html_code')
        
    def sendData(self):
        print "Got Data"

        sent = 0
        #nums = self.getRandomNums(self.data)
        if "meta" in self.data:
            for attr in self.data["meta"]:
                print attr
                content = "meta" + "|divider|" + str(attr) + "|divider|" + str(self.url)
                self.msg.writeMessage(content, 'keywords')
                sent += 1
        if "href" in self.data:
            for attr in self.data["href"]:
                self.checkForUrl(attr)
            
        '''for tag in self.data:
            if self.tagIsImportant(tag):
                #for x in nums:
                    #attr = self.data[tag][x]
                for attr in self.data[tag]:
                    #self.checkForUrl(attr)    
                    content = str(tag) + "|divider|" + str(attr) + "|divider|" + str(self.url)
                    self.msg.writeMessage(content, 'tagged_content')
                    sent += 1'''
        print "Sent " + str(sent) + " messages"              
        
    
    def checkForUrl(self, obj):
       
        if isinstance(obj, basestring):
            strobj = str(obj)
            if strobj.find("http") != -1:
                self.msg.writeMessage(strobj, 'found_url')
                print "Found URL"
                return True
        elif isinstance (obj, (list, tuple)):
            for child in obj:
                if str(child).find("http") != -1:
                    return self.checkForUrl(child)
                return False
        else:
            print "Weird Behavior"
            return False
        print "Did not find"
        return False
    
    def callback(self, ch, method, properties, body):
        stdout.flush()
        print "Got HTML"
        body = body.split("|divider|")
        html = body[0]
        self.url = body[1]
        self.sent_urls = 0
        #self.sendURLs(body)
        try :
            self.feed(html)
            print "Feeding done"
            self.sendData()
        except:
            print "Unicode Error"

        
    def handle_starttag(self, tag, attrs):
        
        if not tag in self.data:        
            self.data[tag] = attrs
        else:
            self.data[tag].append(attrs)
        if tag == "a" and self.sent_urls < 15 and self.rand.randint(0, 100) > 95:
           # Check the list of defined attributes.
           for name, value in attrs:
               # If href is defined, print it.
               if name == "href":
                   self.msg.writeMessage(value, 'found_url')
                   self.sent_urls += 1
               if self.sent_urls >= 15:
                   print "BREAKING"
                   break
              
                   
               
            
    def tagIsImportant(self, tag):
        if tag in self.tag_list:
            return True
        else:
            return False
            
    def getRandomNums(self, passedlist):
        numlist = list()
        if len(passedlist) < 2:
            return [0]
        for x in range(0, MANY_TO_SEARCH):        
            numlist.append(self.rand.randint(1, len(passedlist) - 1))
        if len(passedlist) < MANY_TO_SEARCH:
            return range(0, len(passedlist) - 1)
        return numlist
    
if __name__ == "__main__":
    procname.setprocname('Organizer')
    ORG = Organizer()