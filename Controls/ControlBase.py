'''
Created on Mar 21, 2015

@author: warringer
'''

class ControlBase:
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        raise NotImplementedError()
    
    def isPressed(self, index):
        raise NotImplementedError()
    
    def isReleased(self, index):
        raise NotImplementedError()
    
    def getToggle(self, index):
        raise NotImplementedError()
    
    def unsetToggle(self, index):
        raise NotImplementedError()

    def getRotary(self):
        raise NotImplementedError()

    def doControl(self):
        raise NotImplementedError()
    
    def doKeys(self, index):
        raise NotImplementedError()