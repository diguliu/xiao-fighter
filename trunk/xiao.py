# -*- coding: utf-8 -*-
from pygame.locals import *
import pygame
from constants import *
from evManager import *
from model import *
from view import *
from control import *

def main():
    """..."""
    evManager = EventManager()

    spinner = CPUSpinnerController(evManager)
    pygameView = PygameView(evManager)
    game = Game(evManager)
    keybd = KeyboardController(evManager, game)
    
    spinner.Run()

if __name__ == '__main__':
    main()
