'''
Created on Mar 20, 2015

@author: warringer
'''
# -*- coding: utf-8 -*-
import time
import wiringpi2 as wiringpi
import threading

class Button:

    #----------------------------------------------------------------------
    # Pass the wiring pin numbers here. See:
    # https://projects.drogon.net/raspberry-pi/wiringpi2/pins/
    #----------------------------------------------------------------------
    def __init__(self, buttonList):
        self.buttonList     = buttonList               # Pin IDs via WiringIDs in List
        self.button_states  = []

    def getButtonLine(self, active):                # active List ID of wiringID Pin
        states = []
        
        for i, n in enumerate(self.buttonList):
            if i == active:
                wiringpi.pinMode(n, 1)
            else:
                wiringpi.pinMode(n, 0)

        wiringpi.digitalWrite(self.buttonList[active], 1)   # sets active pin to 1 (3V3, on)
    
        for i, n in enumerate(self.buttonList):
            if i != active:
                states.append(wiringpi.digitalRead(n))
    
        wiringpi.digitalWrite(self.buttonList[active], 0)

        return states

    def executeButtonPress(self):
        self.button_states = []

        for i, n in enumerate(self.buttonList):
            self.button_states = self.button_states + self.getButtonLine(i)


    def getButtons(self):
        self.executeButtonPress()

        return self.button_states


    class Worker(threading.Thread):
        def __init__(self, buttonList):
            threading.Thread.__init__(self)
            self.lock = threading.Lock()
            self.buttons = Button(buttonList)

        def run(self):
            while True:
                with self.lock:
                    self.buttons.executeButtonPress()        
                time.sleep(0.001)

        def getButtons(self):
            with self.lock:
                buttons = self.buttons.getButtons()
            return buttons
