#!/usr/bin/python

import sys, pygame, os
import gaugette.rotary_encoder
import gaugette.switch
import time
from mpd import MPDClient
import types
from socket import error as SocketError
import wiringpi2 as wiringpi
import threading
import Controls.Hardware
import Clients.MPDClient
import Display.Player

global TEST_MPD_HOST, TEST_MPD_PORT, TEST_MPD_PASSWORD

TEST_MPD_HOST     = "localhost"
TEST_MPD_PORT     = "6600"
TEST_MPD_PASSWORD = None

os.putenv('SDL_VIDEODRIVER', 'fbcon')
os.putenv("SDL_FBDEV", "/dev/fb1")
os.putenv("SDL_MOUSEDRV", "TSLIB")
os.putenv("SDL_MOUSEDEV", "/dev/input/event0")

# WiringPi pins for LED Charlieplexing
LED_A = 29
LED_B = 25

# WiringPi pins for Key Charlieplexing
KEY_A = 28
KEY_B = 27
KEY_C = 26

# WiringPi pins for Rotary Encoder
ROT_A = 23
ROT_B = 24

pinlayout = {'LED_A': LED_A, 'LED_B' : LED_B, 'KEY_A': KEY_A, 'KEY_B': KEY_B, 'KEY_C': KEY_C, 'ROT_A': ROT_A, 'ROT_B': ROT_B}

keys = {'play': 2, 'prev': 0, 'next': 3, 'stop': 5, 'mode': 4, 'enter': 1}

keystates = [None,None,None,None,None,None]

playerskin = "/home/pi/RPiMusicBox/playerskin.png"

size = width, height = 320, 240

# Initializing

pygame.init()
screen = pygame.display.set_mode(size)

pygame.mouse.set_visible(False)

#controls = Controls.Controls.PlayerControls.Worker(pinlayout, keystates, keys, 80)
controls = Controls.Hardware.Hardware(pinlayout, keystates, keys, 80)

client = Clients.MPDClient.MDPClient(TEST_MPD_HOST, TEST_MPD_PORT)

player = Display.Hardware.Hardware(screen=screen, controls=controls, client=client, playerskin=playerskin)

while True:
    player.drawPlayer()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    
    pygame.display.update()
