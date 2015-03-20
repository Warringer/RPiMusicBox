'''
Created on Mar 20, 2015

@author: warringer
'''

import time
from mpd import MPDClient
import types
from socket import error as SocketError

class MDPClient(object):
    '''
    classdocs
    '''


    def __init__(self, host, port, password = None):
        '''
        Constructor
        '''
        client = MPDClient()
        connected = False
        while connected == False:
            connected = True
            try:
                client.connect(host, port)

                # self.commands = self.client.commands()
            except SocketError as e:
                connected = False

            if connected == True and password != None:
                try:
                    client.password(password)

                except mpd.CommandError as e:
                    connected = False

            if connected == False:
                print "Couldn't connect. Retrying"
                time.sleep(5)
            
        print("Connected to MPD Client")
        self.client = client
        
    def status(self):
        return self.client.status()
    
    def currentsong(self):
        return self.client.currentsong()
    
    def play(self, id = 1):
        self.client.play(id)
        
    def pause(self):
        self.client.pause()
        
    def stop(self):
        self.client.stop()
        
    def prev(self):
        self.client.prev()
        
    def next(self):
        self.client.next()
        
    def setVolume(self, volume):
        self.client.setvol(volume)