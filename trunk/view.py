import pygame
from pygame.locals import *
from evManager import *
from constants import *

class CharactorSprite(pygame.sprite.Sprite):
    def __init__(self, group=None):
        pygame.sprite.Sprite.__init__(self, group)
        
        self.image = pygame.image.load("xiao.png")
        self.rect  = self.image.get_rect()

        self.moveTo = None
        self.image_sleep = 40
        self.flag_switch = 0
    #----------------------------------------------------------------------
    def update(self):
        if self.moveTo:
            self.rect.center = self.moveTo
            self.moveTo = None

#------------------------------------------------------------------------------
class PygameView:
    """..."""
    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.RegisterListener(self)

        pygame.init()
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Xiao fighter')
        self.background = pygame.Surface(self.window.get_size())
        self.background.fill((255, 255, 255))

        self.backSprites = pygame.sprite.RenderUpdates()
        self.frontSprites = pygame.sprite.RenderUpdates()

        self.window.blit(self.background, (0,0))
        pygame.display.flip()

    #----------------------------------------------------------------------
#Wrote by Rodrigo    
    def ShowCharactor(self, charactor):
        charactorSprite = CharactorSprite(self.frontSprites)
#        sector = charactor.sector
#        sectorSprite = self.GetSectorSprite(sector)
        charactor.sprite = charactorSprite
        charactorSprite.rect.center = charactor.rect.center

    #----------------------------------------------------------------------
#Wrote by Rodrigo
    def MoveCharactor(self, charactor):
        charactor.sprite.moveTo = charactor.rect.center
        charactorSprite = charactor.sprite
        if charactorSprite.flag_switch == 0:
            charactorSprite.image_sleep -= 1
        else:
            charactorSprite.image_sleep += 1
        if charactor.eyeDirection == 3:
            if charactorSprite.image_sleep== 0:
                charactorSprite.image = pygame.image.load("xiao2.png")
                charactorSprite.flag_switch = 1
            if charactorSprite.image_sleep== 40:
                charactorSprite.image = pygame.image.load("xiao.png")
                charactorSprite.flag_switch = 0
            if charactorSprite.image_sleep == 20:
                charactorSprite.image = pygame.image.load("xiao3.png")
        else:
            if charactorSprite.image_sleep== 0:
                charactorSprite.image = pygame.image.load("xiao2.png")
                charactorSprite.image = pygame.transform.flip(charactorSprite.image,1,0)
                charactorSprite.flag_switch = 1
            if charactorSprite.image_sleep== 40:
                charactorSprite.image = pygame.image.load("xiao.png")
                charactorSprite.image = pygame.transform.flip(charactorSprite.image,1,0)
                charactorSprite.flag_switch = 0
            if charactorSprite.image_sleep == 20:
                charactorSprite.image = pygame.image.load("xiao3.png")
                charactorSprite.image = pygame.transform.flip(charactorSprite.image,1,0)

    #----------------------------------------------------------------------
    def Notify(self, event):
        if isinstance(event, TickEvent):
            #Draw Everything
            self.backSprites.clear( self.window, self.background)
            self.frontSprites.clear( self.window, self.background)

            self.backSprites.update()
            self.frontSprites.update()

            dirtyRects1 = self.backSprites.draw(self.window)
            dirtyRects2 = self.frontSprites.draw(self.window)
            
            dirtyRects = dirtyRects1 + dirtyRects2
            pygame.display.update(dirtyRects)


        elif isinstance(event, MapBuiltEvent):
            map = event.map
            self.ShowMap(map)

        elif isinstance(event, CharactorPlaceEvent):
            self.ShowCharactor(event.charactor)

        elif isinstance(event, CharactorMoveEvent):
            self.MoveCharactor(event.charactor)



