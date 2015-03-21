'''
Created on Mar 21, 2015

@author: warringer
'''

import time

class ScrollText():
    '''
    classdocs
    '''

    TICK_LENGTH = 0.5

    def __init__(self, text, width):
        '''
        Constructor
        '''
        self.text           = text
        self.tick           = 0
        self.text_length    = self.text.len()
        self.width          = width
        self.timer          = time.time()
        
    def doTick(self):
        if (self.timer + self.TICK_LENGTH) > time.time():
            self.tick += 1
        if self.tick > (self.text_length - self.width):
            self.tick = 0
        self.timer = time.time()
            
    def getScrolledText(self):
        start   = self.tick
        end     = start + self.width
        return self.text[start:end]
    
    def setScrolledText(self, text):
        if text != self.text:
            self.text           = text
            self.tick           = 0
            self.text_length    = self.text.len()
            self.timer          = time.time()