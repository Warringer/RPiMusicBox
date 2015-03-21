'''
Created on Mar 21, 2015

@author: warringer
'''

import Controls.Hardware
import Clients.MPDClient

class Player:
    '''
    classdocs
    '''


    def __init__(self, controls, client):
        '''
        Constructor
        '''
        self.controls   = controls
        self.client     = client
        
    def doControls(self):
        if self.controls.getToggle('play') == 1:
            if self.status['state'] == 'play':
                self.client.pause()
            elif self.status['state'] == 'pause':
                self.client.pause()
            elif self.status['state'] == 'stop':
                self.client.play()
            else:
                pass
            self.controls.unsetToggle('play')
        
        if self.controls.getToggle('prev') == 1:
            self.client.prev()
            self.controls.unsetToggle('prev')
                    
        if self.controls.getToggle('next') == 1:
            self.client.next()
            self.controls.unsetToggle('next')
        
        if self.controls.getToggle('stop') == 1:
            self.client.stop()
            self.controls.unsetToggle('stop')
        
        if self.controls.getToggle('mode') == 1:
            self.controls.unsetToggle('mode')
        
        if self.controls.getToggle('enter') == 1:
            self.controls.unsetToggle('enter')

        self.client.setVolume(self.controls.getRotary())