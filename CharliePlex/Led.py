'''
Created on Mar 20, 2015

@author: warringer
'''
import time
import wiringpi2 as wiringpi
import threading

class Led:

    #----------------------------------------------------------------------
    # Pass the wiring pin numbers here. See:
    # https://projects.drogon.net/raspberry-pi/wiringpi2/pins/
    #----------------------------------------------------------------------
    def __init__(self, led1pin, led2pin):
        self.pin1 = led1pin
        self.pin2 = led2pin
        
        self.led = [None,None]

        # Sets the LED pins to output
        wiringpi.pinMode(self.pin1, 1)
        wiringpi.pinMode(self.pin2, 1)

    def setLed(self, index):
        self.led[index] = 1

    def unsetLed(self, index):
        self.led[index] = 0

    def getLed(self, index):
        return self.led[index]

    def executeDisplay(self):

        for i, n in enumerate(self.led):
            
            wiringpi.digitalWrite(self.pin1, 0)
            wiringpi.digitalWrite(self.pin2, 0)
        
            if i == 0:
                wiringpi.digitalWrite(self.pin1, n)
            elif i == 1:
                wiringpi.digitalWrite(self.pin2, n)
            else:
                pass
                

    class Worker(threading.Thread):
        def __init__(self, led1pin, led2pin):
            threading.Thread.__init__(self)
            self.lock = threading.Lock()
            self.led = Led(led1pin, led2pin)

        def run(self):
            while True:
                with self.lock:
                    self.led.executeDisplay()
                time.sleep(0.0005)

        def setLed(self, index):
            with self.lock:
                self.led.setLed(index)

        def unsetLed(self, index):
            with self.lock:
                self.led.unsetLed(index)

        def getLed(self, index):
            with self.lock:
                return self.led.getLed(index)
