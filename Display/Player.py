'''
Created on Mar 20, 2015

@author: warringer
'''

import sys, pygame, os, time
import Hardware.PlayerControls
import Clients.MPDClient

class Player(object):
    '''
    classdocs
    '''
    BLACK = 0, 0, 0
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    
    # Volume Bar
    VOLBAR_HEIGHT = 208
    VOLBAR_WIDTH = 5
    VOLBAR_LEFT = 308
    VOLBAR_BOTTOM = 233

    # Progressbar
    PROGBAR_HEIGHT = 5
    PROGBAR_TOP = 135
    PROGBAR_LEFT = 6

    if pygame.font:
        pygame.font.init()
        FONT_TEXT = pygame.font.SysFont("Droid Sans Mono" , 12)
        FONT_SYM = pygame.font.SysFont("DejaVu Sans Mono" , 36)
        
    SYMBOLS = {'play': [u'\u25b6', u'\u25b7'], 'pause': [u'\u25ae\u25ae', u'\u25af\u25af'], 'prev': [u'\u25c0\u25c0', u'\u25c1\u25c1'], 'next': [u'\u25b6\u25b6', u'\u25b7\u25b7'], 'stop': [u'\u25a0', u'\u25a1'], 'mode': [u'\u2731', u'\u2732']}
    

    def __init__(self, screen, playerskin, controls, client):
        '''
        Constructor
        '''
        
        self.screen = screen
        self.keysymbols = {'play': self.SYMBOLS['play'][0], 'prev': self.SYMBOLS['prev'][0], 'next': self.SYMBOLS['next'][0], 'stop': self.SYMBOLS['stop'][0], 'mode': self.SYMBOLS['mode'][0]}
        self.background = pygame.image.load(playerskin).convert()
        self.controls = controls
        self.client = client
        self.status = None
        self.currentSong = None
        
    def drawVolume(self):
        vol = int(self.controls.getRotary() * 2.08)
        volbar_top = self.VOLBAR_BOTTOM - vol
        pygame.draw.rect(self.screen, self.GREEN, pygame.Rect(self.VOLBAR_LEFT, volbar_top, self.VOLBAR_WIDTH, vol))
        
    def getClientData(self):
        self.status = self.client.status()
        self.currentSong = self.client.currentsong()
        
    def drawProgress(self):
        if self.status['state'] != 'stop':
            time_pos = self.status['time'].split(':')
            position = int(time_pos[0])
            length = int(time_pos[1])
            progress = int((float(position) / float(length)) * 296)
            pos = time.strftime('%M:%S', time.gmtime(position))
            leng = time.strftime('%M:%S', time.gmtime(length))
            timer = "%s/%s" % (pos, leng)
            pygame.draw.rect(self.screen, self.GREEN, pygame.Rect(self.PROGBAR_LEFT, self.PROGBAR_TOP, progress, self.PROGBAR_HEIGHT))
        else:
            timer = "00:00/00:00"
        text_timer = self.FONT_TEXT.render(timer, 1, self.GREEN)
        self.screen.blit(text_timer, (225, 144))
        
    def drawSongData(self):
        if self.currentSong != {}:
            album = "%s - %s" % (self.currentSong['albumartist'], self.currentSong['album'])
            track = "CD %s, Track %s" % (self.currentSong['disc'], self.currentSong['track'])
            song = "%s - %s" % (self.currentSong['artist'], self.currentSong['title'])
        else:
            album = ""
            track = ""
            song = "Currently not playing"
        text_album = self.FONT_TEXT.render(album, 1, self.WHITE)
        text_track = self.FONT_TEXT.render(track, 1, self.WHITE)
        text_song = self.FONT_TEXT.render(song, 1, self.WHITE)
        self.screen.blit(text_album, (4, 4))
        self.screen.blit(text_track, (4, 18))
        self.screen.blit(text_song, (4, 30))
        
    def drawControls(self):       
        if self.controls.isPressed('play'):
            if self.status['state'] == 'play':
                self.keysymbols['play'] = self.SYMBOLS['pause'][1]
            else:
                self.keysymbols['play'] = self.SYMBOLS['play'][1]
        if self.controls.isReleased('play'):
            if self.status['state'] == 'play':
                self.keysymbols['play'] = self.SYMBOLS['pause'][0]
            else:
                self.keysymbols['play'] = self.SYMBOLS['play'][0]
                     
        if self.controls.isPressed('prev'):
            self.keysymbols['prev'] = self.SYMBOLS['prev'][1]
        if self.controls.isReleased('prev'):
            self.keysymbols['prev'] = self.SYMBOLS['prev'][0]
            
        if self.controls.isPressed('next'):
            self.keysymbols['next'] = self.SYMBOLS['next'][1]
        if self.controls.isReleased('next'):
            self.keysymbols['next'] = self.SYMBOLS['next'][0]
            
        if self.controls.isPressed('stop'):
            self.keysymbols['stop'] = self.SYMBOLS['stop'][1]
        if self.controls.isReleased('stop'):
            self.keysymbols['stop'] = self.SYMBOLS['stop'][0]
            
        if self.controls.isPressed('mode'):
            self.keysymbols['mode'] = self.SYMBOLS['mode'][1]
        if self.controls.isReleased('mode'):
            self.keysymbols['mode'] = self.SYMBOLS['mode'][0]
            
        self.screen.blit(self.FONT_SYM.render(self.keysymbols['prev'], 1, self.GREEN), (13, 181))
        if self.keysymbols['play'] in self.SYMBOLS['play']:
            self.screen.blit(self.FONT_SYM.render(self.keysymbols['play'], 1, self.GREEN), (84, 181))
        else:
            self.screen.blit(self.FONT_SYM.render(self.keysymbols['play'], 1, self.GREEN), (73, 181))
        self.screen.blit(self.FONT_SYM.render(self.keysymbols['stop'], 1, self.GREEN), (144, 181))
        self.screen.blit(self.FONT_SYM.render(self.keysymbols['next'], 1, self.GREEN), (193, 181))
        self.screen.blit(self.FONT_SYM.render(self.keysymbols['mode'], 1, self.GREEN), (264, 181))
        
    def doControl(self):
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
        
    def drawPlayer(self):
        self.getClientData()
        self.controls.doKeys()
        self.screen.blit(self.background, [0, 0])
        self.drawVolume()
        self.drawProgress()
        self.drawSongData()
        self.drawControls()
        self.doControl()
        
