import pygame
from pygame.locals import *

##CONSTANTS##
#Directions
DIRECTION_UP = 0
DIRECTION_DOWN = 1
DIRECTION_LEFT = 2
DIRECTION_RIGHT = 3

#The lesser speed is faster. In fact, speed is actually a "sleep".  xD
RUN_SPEED = 3
WALK_SPEED = 5
VERT_SPEED = 1

#Xiao Image Size
XIAO_WIDTH = 30
XIAO_HEIGHT = 70

#Screen Size
WIDTH = 800
HEIGHT = 600

#Top limit inside de screen
TOP_LIMIT = HEIGHT*40/100

#Jump Control
MAX_JUMPS = 80
MAX_STAY_RUN = 10
MAX_STAY_WALK = 10
ACC = 3

#Start Rect Player 1
START_RECT1 = pygame.Rect(0,TOP_LIMIT+1,XIAO_WIDTH,XIAO_HEIGHT)

#Start Rect Player 2
START_RECT2 = pygame.Rect(WIDTH-XIAO_WIDTH,HEIGHT-XIAO_HEIGHT,XIAO_WIDTH,XIAO_HEIGHT)

#Player 1
P1_UP = K_w
P1_DOWN = K_s
P1_LEFT = K_a
P1_RIGHT = K_d
P1_ATK = K_h
P1_JMP = K_j
P1_BLK = K_k

#Player 2
P2_UP = K_KP8
P2_DOWN = K_KP5
P2_LEFT = K_KP4
P2_RIGHT = K_KP6
P2_ATK = K_INSERT
P2_JMP = K_HOME
P2_BLK = K_PAGEUP

CONTROL_P1 = [P1_UP,P1_DOWN,P1_LEFT,P1_RIGHT,P1_ATK,P1_JMP,P1_BLK]
CONTROL_P2 = [P2_UP,P2_DOWN,P2_LEFT,P2_RIGHT,P2_ATK,P2_JMP,P2_BLK]

#Sleeps
COMBO_SLEEP = 500
CRITICAL_SLEEP = 1000
DAMAGED_SLEEP = 500
FALLING_SLEEP = 1000

##CONSTANTS##
#Directions
DIRECTION_UP = 0
DIRECTION_DOWN = 1
DIRECTION_LEFT = 2
DIRECTION_RIGHT = 3

#The lesser speed is faster. In fact, speed is actually a "sleep".  xD
RUN_SPEED = 3
WALK_SPEED = 5
VERT_SPEED = 1

#Xiao Image Size
XIAO_WIDTH = 30
XIAO_HEIGHT = 70

#Screen Size
WIDTH = 800
HEIGHT = 600

#Top limit inside de screen
TOP_LIMIT = HEIGHT*40/100

#Jump Control
MAX_JUMPS = 80
MAX_STAY_RUN = 10
MAX_STAY_WALK = 10
ACC = 3

#Start Rect Player 1
START_RECT1 = pygame.Rect(0,TOP_LIMIT+1,XIAO_WIDTH,XIAO_HEIGHT)

#Start Rect Player 2
START_RECT2 = pygame.Rect(WIDTH-XIAO_WIDTH,HEIGHT-XIAO_HEIGHT,XIAO_WIDTH,XIAO_HEIGHT)

#Player 1
P1_UP = K_w
P1_DOWN = K_s
P1_LEFT = K_a
P1_RIGHT = K_d
P1_ATK = K_h
P1_JMP = K_j
P1_BLK = K_k

#Player 2
P2_UP = K_KP8
P2_DOWN = K_KP5
P2_LEFT = K_KP4
P2_RIGHT = K_KP6
P2_ATK = K_INSERT
P2_JMP = K_HOME
P2_BLK = K_PAGEUP

CONTROL_P1 = [P1_UP,P1_DOWN,P1_LEFT,P1_RIGHT,P1_ATK,P1_JMP,P1_BLK]
CONTROL_P2 = [P2_UP,P2_DOWN,P2_LEFT,P2_RIGHT,P2_ATK,P2_JMP,P2_BLK]

#Sleeps
COMBO_SLEEP = 500
CRITICAL_SLEEP = 1000
DAMAGED_SLEEP = 500
FALLING_SLEEP = 1000

