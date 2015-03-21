'''
Created on Mar 21, 2015

@author: warringer
'''

import pygame, time
from pygame.locals import *
from Controls.ControlBase import ControlBase

class Touchscreen(ControlBase):
    '''
    classdocs
    
    buttonlayout = {'button': [x,y,h,w], 'button': [x,y,h,w], ... }
    '''


    def __init__(self, buttonlayout):
        '''
        Constructor
        '''
        self.buttonlayout   = buttonlayout
        self.toggle         = {}
        for key in self.buttonlayout:
            self.toggle[key]        = 0

    def doControls(self):
        self.doButtons()
        
    def doButtons(self):
        for event in pygame.event.get():
            if (event.type in [MOUSEBUTTONDOWN, MOUSEBUTTONUP]):
                pos = pygame.mouse.get_pos()
                for button, bpos in self.buttonlayout.iteritems():
                    self.doButton(button, pos, event.type, bpos[0], bpos[1], bpos[2], bpos[3])
                
    def doButton(self, button, pos, event, x, y, h, w):
        px, py = pos
        if (px >= x) and (px <= x + h):
            if (py >= y) and (py <= y + w):
                if (event == MOUSEBUTTONDOWN):
                    self.toggle[button] = -1
                elif (event == MOUSEBUTTONUP):
                    self.toggle[button] = 1
                else:
                    pass
    
    def isPressed(self, index):
        if self.toggle[index] == -1:
            return True
        else:
            return False
        
    def isrReleased(self, index):
        if self.toggle[index] == 1:
            return True
        else:
            return False
        
    def getToggle(self, index):
        return self.toggle[index]
    
    def unsetToggle(self, index):
        self.toggle[index] = 0
        
    def getRotary(self):
        return None
