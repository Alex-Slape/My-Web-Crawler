# -*- coding: utf-8 -*-
'''
Web Reader is a class that takes in a list of web addresses, grabs the web data,
and then sends it to Organizer.

author: Alex Slape

'''
import urllib
from sys import path, stdout
path.append("../Messenging/")
path.append("../procname/")
import procname
try:
    from Messenger import Messenger
except:
    print "Messenger not found"
    raise ImportError
    


class WebReader():
    
    def __init__(self):
        print "Initializing"
        self.msg = Messenger()
        self.url = None
        self.handleInput()        
        
    def handleInput(self):
        self.msg.registerForMessage( self.callback, 'url')
    
    def grabData(self, url):
        if url != None and self.isUrl(url):
            print "Grabbing: " + url
            self.url = url
            sock = urllib.urlopen(url) 
            htmlSource = sock.read()                            
            sock.close()   
            self.sendData(htmlSource)
        else:
            print "Got None Type"
    
    def isUrl(self, url):
        if str(url).find('http') != -1:
            return True
        else:
            return False
    
    def sendData(self, raw_data):
        self.msg.writeMessage(raw_data + "|divider|" + str(self.url), 'html_code')
        print "Message Sent"
    
    def callback(self, ch, method, properties, body):
        stdout.flush()
        print "Message Recieved"            
        self.grabData(str(body))

if __name__ == "__main__":
    procname.setprocname('WebReader')
    WR = WebReader()
    