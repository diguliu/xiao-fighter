import pygame
from pygame.locals import *
from evManager import *
from constants import *

#------------------------------------------------------------------------------
#Wrote by Rodrigo
class KeyboardController:
    def __init__(self, evManager, game):
        self.evManager = evManager
        self.evManager.RegisterListener(self)
        self.game = game


    #----------------------------------------------------------------------
#From here I (Rodrigo) wrote all Key Requests
    def Notify(self, event):
        if isinstance(event, TickEvent):
            # Handle input events.
            for event in pygame.event.get():
                ev1 = None
                ev2 = None
                if event.type == QUIT:
                    ev1 = QuitEvent()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        ev1 = QuitEvent()
                    elif event.key == P1_UP:
                        ev2 = CharactorWalkEvent(DIRECTION_UP,self.game.players[0].charactor)
                        ev1 = CharactorAdd2ComboRequest(P1_UP,self.game.players[0].charactor)
                    elif event.key == P2_UP:
                        ev2 = CharactorWalkEvent(DIRECTION_UP,self.game.players[1].charactor)
                        ev1 = CharactorAdd2ComboRequest(P2_UP,self.game.players[1].charactor)
                    elif event.key == P1_DOWN:
                        ev2 = CharactorWalkEvent(DIRECTION_DOWN,self.game.players[0].charactor)
                        ev1 = CharactorAdd2ComboRequest(P1_DOWN,self.game.players[0].charactor)
                    elif event.key == P2_DOWN:
                        ev2 = CharactorWalkEvent(DIRECTION_DOWN,self.game.players[1].charactor)
                        ev1 = CharactorAdd2ComboRequest(P2_DOWN,self.game.players[1].charactor)
                    elif event.key == P1_LEFT:
                        ev2 = CharactorWalkEvent(DIRECTION_LEFT,self.game.players[0].charactor)
                        ev1 = CharactorAdd2ComboRequest(P1_LEFT,self.game.players[0].charactor)
                    elif event.key == P2_LEFT:
                        ev2 = CharactorWalkEvent(DIRECTION_LEFT,self.game.players[1].charactor)
                        ev1 = CharactorAdd2ComboRequest(P2_LEFT,self.game.players[1].charactor)
                    elif event.key == P1_RIGHT:
                        ev2 = CharactorWalkEvent(DIRECTION_RIGHT,self.game.players[0].charactor)
                        ev1 = CharactorAdd2ComboRequest(P1_RIGHT,self.game.players[0].charactor)
                    elif event.key == P2_RIGHT:
                        ev2 = CharactorWalkEvent(DIRECTION_RIGHT,self.game.players[1].charactor)
                        ev1 = CharactorAdd2ComboRequest(P2_RIGHT,self.game.players[1].charactor)
                    elif event.key == P1_ATK:
                        ev2 = CharactorAttackRequest(self.game.players[0].charactor)
                        ev1 = CharactorAdd2ComboRequest(P1_ATK,self.game.players[0].charactor)
                    elif event.key == P2_ATK:
                        ev2 = CharactorAttackRequest(self.game.players[1].charactor)
                        ev1 = CharactorAdd2ComboRequest(P2_ATK,self.game.players[1].charactor)
                    elif event.key == P1_BLK:
                        ev2 = CharactorDefendRequest(self.game.players[0].charactor)
                        ev1 = CharactorAdd2ComboRequest(P1_BLK,self.game.players[0].charactor)
                    elif event.key == P2_BLK:
                        ev2 = CharactorDefendRequest(self.game.players[1].charactor)
                        ev1 = CharactorAdd2ComboRequest(P2_BLK,self.game.players[1].charactor)
                    elif event.key == P1_JMP:
                        ev2 = CharactorJumpRequest(self.game.players[0].charactor)
                        ev1 = CharactorAdd2ComboRequest(P1_JMP,self.game.players[0].charactor)
                    elif event.key == P2_JMP:
                        ev2 = CharactorJumpRequest(self.game.players[1].charactor)
                        ev1 = CharactorAdd2ComboRequest(P2_JMP,self.game.players[1].charactor)
                        
                elif event.type == KEYUP:
                    if event.key == P1_UP:
                        ev1 = CharactorStopWalkEvent(DIRECTION_UP,self.game.players[0].charactor)
                    elif event.key == P2_UP:
                        ev1 = CharactorStopWalkEvent(DIRECTION_UP,self.game.players[1].charactor)
                    elif event.key == P1_DOWN:
                        ev1 = CharactorStopWalkEvent(DIRECTION_DOWN,self.game.players[0].charactor)
                    elif event.key == P2_DOWN:
                        ev1 = CharactorStopWalkEvent(DIRECTION_DOWN,self.game.players[1].charactor)
                    elif event.key == P1_LEFT:
                        ev1 = CharactorStopWalkEvent(DIRECTION_LEFT,self.game.players[0].charactor)
                    elif event.key == P2_LEFT:
                        ev1 = CharactorStopWalkEvent(DIRECTION_LEFT,self.game.players[1].charactor)
                    elif event.key == P1_RIGHT:
                        ev1 = CharactorStopWalkEvent(DIRECTION_RIGHT,self.game.players[0].charactor)
                    elif event.key == P2_RIGHT:
                        ev1 = CharactorStopWalkEvent(DIRECTION_RIGHT,self.game.players[1].charactor)

                if ev1:
                    self.evManager.Post(ev1)
                if ev2:
                    self.evManager.Post(ev2)

#------------------------------------------------------------------------------
class CPUSpinnerController:
    """..."""
    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.RegisterListener(self)

        self.keepGoing = 1

    #----------------------------------------------------------------------
    def Run(self):
        while self.keepGoing:
            event = TickEvent()
            self.evManager.Post(event)

    #----------------------------------------------------------------------
    def Notify(self, event):
        if isinstance(event, QuitEvent):
            # This will stop the while loop from running.
            self.keepGoing = 0

