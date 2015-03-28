'''
Created on Mar 21, 2015

@author: warringer
'''

import Controls.Hardware
import Clients.MPDClient
from Controls import ControlBase

class Player(ControlBase):
    '''
    classdocs
    '''


    def __init__(self, client):
        '''
        Constructor
        '''
        self.sceme  = []
        self.client = client
        self.status = None
        
    def addControlSceme(self, sceme):
        self.sceme.append(sceme)
        
    def doControls(self, status):
        self.status = status
        for sceme in self.sceme:
            self.doControl(sceme)
        
    def doControl(self, controls):
        controls.doControls()
        if controls.getToggle('play') == 1:
            if self.status == 'play':
                self.client.pause()
            elif self.status == 'pause':
                self.client.pause()
            elif self.status == 'stop':
                self.client.play()
            else:
                pass
            controls.unsetToggle('play')
        
        if controls.getToggle('prev') == 1:
            self.client.prev()
            controls.unsetToggle('prev')
                    
        if controls.getToggle('next') == 1:
            self.client.next()
            controls.unsetToggle('next')
        
        if controls.getToggle('stop') == 1:
            self.client.stop()
            controls.unsetToggle('stop')
        
        if controls.getToggle('mode') == 1:
            controls.unsetToggle('mode')
        
        if controls.getToggle('enter') == 1:
            controls.unsetToggle('enter')
        
        rotary = controls.getRotary()
        if rotary != None:
            self.client.setVolume(rotary)
            
    def isPressed(self, index):
        status = False
        for sceme in self.scemes:
            status = status or sceme.isPressed(index)
        return status
        
    def isRelease(self, index):
        status = False
        for sceme in self.scemes:
            status = status or sceme.isReleased(index)
        return status
        
    def getToggle(self, index):
        status = False
        for sceme in self.scemes:
            status = status or sceme.getToggle(index)
        return status
    
    def unsetToggle(self, index):
        for sceme in self.scemes:
            sceme.unsetToggle(index)
        
    def getRotary(self):
        rotary = 0
        for sceme in self.scemes:
            rotary = sceme.getRotary()
        return rotary
    
    def doKeys(self, index):
        for sceme in self.scemes:
            sceme.dioKeys(index)