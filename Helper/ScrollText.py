'''
Created on Mar 21, 2015

@author: warringer
'''

import time

class ScrollText():
    '''
    classdocs
    '''

    TICK_LENGTH  = 0.1
    TICK_INITIAL = 0.5

    def __init__(self, text, width):
        '''
        Constructor
        '''
        self.text           = text
        self.tick           = 0
        self.text_length    = len(self.text)
        self.width          = width
        self.timer          = time.clock()
        self.init_tick      = True 
        
    def doTick(self):
        if self.init_tick:
            tick = self.TICK_INITIAL
        else:
            tick = self.TICK_LENGTH
        if (time.clock() - self.timer) > tick:
            self.tick += 1
            self.timer = time.clock()
        if self.tick > (self.text_length - self.width):
            self.tick = 0
            self.timer = time.clock()
            
    def getScrolledText(self):
        start   = self.tick
        end     = start + self.width
        if (start == 0) or (end == self.text_length):
            self.init_tick = True
        else:
            self.init_tick = False
        return self.text[start:end]
    
    def setScrolledText(self, text):
        if text != self.text:
            self.text           = text
            self.tick           = 0
            self.text_length    = len(self.text)
            self.timer          = time.clock()
            self.init_tick      = True
