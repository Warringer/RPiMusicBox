'''
Created on Mar 21, 2015

@author: warringer
'''

import pygame, time
from Controls.ControlBase import ControlBase

class Touchscreen(ControlBase):
    '''
    classdocs
    '''


    def __init__(self, buttonlayout):
        '''
        Constructor
        '''
        self.buttonlayout = buttonlayout
        