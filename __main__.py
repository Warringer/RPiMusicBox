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
from Controls import *
import Clients.MPDClient
import Display.Player
import Controls

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

player_touchbuttons = {'prev': [7, 178, 53, 53], 'play': [67, 178, 53, 53], 'stop': [127, 178, 53, 53], 'next': [187, 178, 53, 53], 'mode': [247, 178, 53, 53]}

keys = {'play': 2, 'prev': 0, 'next': 3, 'stop': 5, 'mode': 4, 'enter': 1}

playerskin = "/home/pi/RPiMusicBox/playerskin.png"

size = width, height = 320, 240

# Initializing

pygame.init()
screen = pygame.display.set_mode(size)

pygame.mouse.set_visible(False)

#player_hardwarecontrols = Controls.Controls.PlayerControls.Worker(pinlayout, keystates, keys, 80)
player_hardwarebuttons   = Controls.Hardware.Hardware(pinlayout, keys, 70)
player_touchscreen      = Controls.Touchscreen.Touchscreen(player_touchbuttons)

client = Clients.MPDClient.MDPClient(TEST_MPD_HOST, TEST_MPD_PORT)

player = Display.Player.Player(screen=screen, controls=player_hardwarebuttons, client=client, playerskin=playerskin)

player_controls = Controls.Player.Player(client)
player_controls.addControlSceme(player_hardwarebuttons)
player_controls.addControlSceme(player_touchscreen)

while True:
    player.drawPlayer()
    player_controls.doControls(player.getPlayerStatus())
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    
    pygame.display.update()