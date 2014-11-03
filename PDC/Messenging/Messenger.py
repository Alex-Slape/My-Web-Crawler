# -*- coding: utf-8 -*-
"""
Created on Sat May 31 14:00:13 2014

@author: alex
"""

import pika
import logging
logging.basicConfig()

class Messenger():
    '''Messenger provides a simple framework
    for all classes to send messages to queues
    and read messages from queues'''    
    
    def writeMessage(self, messageContent, stream):
        
        
        connection = pika.BlockingConnection(pika.ConnectionParameters(
               host ='localhost'))
        
        channel = connection.channel()

        channel.queue_declare(queue = stream)

        channel.basic_publish(exchange='',
                      routing_key =stream,
                      body=messageContent)
                      
        connection.close()
        
    def registerForMessage(self, callback, stream):

        connection = pika.BlockingConnection(pika.ConnectionParameters(
               host='localhost'))
        channel = connection.channel()

        channel.queue_declare(queue = stream)
        
        channel.basic_consume(callback,
                      queue=stream,
                      no_ack=False)

        channel.start_consuming()
    
    
    

        
        