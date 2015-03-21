'''
Created on Mar 20, 2015

@author: warringer
'''

import gaugette.rotary_encoder
import gaugette.switch
import wiringpi2 as wiringpi
import threading, time
import CharliePlex.Led
import CharliePlex.Button

class Hardware:
    '''
    classdocs
    '''

    def __init__(self, pinlayout, keystate, keylayout, rotary):
        '''
        Constructor
        '''
        wiringpi.wiringPiSetup()
        
        self.button         = CharliePlex.Button.Button.Worker((pinlayout['KEY_A'], pinlayout['KEY_B'], pinlayout['KEY_C']))
        self.encoder        = gaugette.rotary_encoder.RotaryEncoder.Worker(pinlayout['ROT_A'], pinlayout['ROT_B'])
        self.encoder.start()
        
        self.keystate       = keystate
        self.keylayout      = keylayout
        self.toggle         = self.keylayout.copy()
        for key in self.toggle:
            self.toggle[key] = 0
        self.states         = self.button.getButtons()
        
        self.rotary         = rotary
        self.rotary_state   = 0
    
    def doKey(self, index):
        if (self.states[self.keylayout[index]] == 1) & (self.toggle[index] == 0):
            self.toggle[index] = -1
        if (self.states[self.keylayout[index]] == 0) & (self.toggle[index] == -1):
            self.toggle[index] = 1
    
    def doKeys(self):
        self.states     = self.button.getButtons()
        for key in self.keylayout:
            self.doKey(key)
            
    def isPressed(self, index):	
        if (self.states[self.keylayout[index]] == 1) & (self.toggle[index] <= 0):
            return True
        else:
            return False
        
    def isReleased(self, index):
        if (self.states[self.keylayout[index]] == 0) & (self.toggle[index] > 0):
            return True
        else:
            return False
        
    def getKeystate(self):
        return self.keystate
    
    def getToggle(self, index):
        return self.toggle[index]
    
    def unsetToggle(self, index):
        self.toggle[index] = 0
    
    def doRotary(self):
        delta = self.encoder.get_delta()
        if delta!=0:
            self.rotary_state = self.rotary_state + 1
            if self.rotary_state == 4:
                if (self.rotary == 0) & (delta < 0) :
                    self.rotary = 0
                elif (self.rotary == 99) & (delta > 0):
                    self.rotary = 99
                else:
                    self.rotary = self.rotary + delta
                    if self.rotary > 99:
                        self.rotary = 99
                    if self.rotary < 0:
                        self.rotary = 0
                    self.rotary_state = 0
                    
    def getRotary(self):
        self.doRotary()
        return self.rotary
                    
    class Worker(threading.Thread):
        def __init__(self, pinlayout, keystate, keylayout, rotary):
            threading.Thread.__init__(self)
            self.lock       = threading.Lock()
            self.controls   = Hardware(pinlayout, keystate, keylayout, rotary)
            self.running    = True

        def run(self):
            while self.running:
                with self.lock:
                    self.controls.doKeys()
                    self.controls.doRotary()
                time.sleep(0.0005)

        def getKeystate(self):
            with self.lock:
                return self.controls.getKeystate()
                
        def getToggle(self, index):
            with self.lock:
                return self.controls.getToggle(index)
        
        def isPressed(self, index):
            with self.lock:
                return self.controls.isPressed(index)
        
        def isReleased(self, index):
            with self.lock:
                return self.controls.isReleased(index)
                
        def getRotary(self):
            with self.lock:
                return self.controls.getRotary()
            
        def unsetToggle(self, index):
            with self.lock:
                self.controls.unsetToggle(index)
