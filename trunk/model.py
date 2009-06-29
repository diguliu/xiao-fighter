from pygame.locals import *
import pygame
from constants import *
from evManager import *

#------------------------------------------------------------------------------
class Game:
    """..."""

    STATE_PREPARING = 0
    STATE_RUNNING = 1
    STATE_PAUSED = 2

    #----------------------------------------------------------------------
    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.RegisterListener(self)

        self.state = Game.STATE_PREPARING
        
        self.players = [Player(evManager,CONTROL_P1,START_RECT1),Player(evManager,CONTROL_P2,START_RECT2)]
#        self.map = Map(evManager)

    #----------------------------------------------------------------------
    def Start(self):
#        self.map.Build()
        self.state = Game.STATE_RUNNING
        ev = GameStartedEvent(self)
        self.evManager.Post(ev)

    #----------------------------------------------------------------------
    def Notify(self, event):
        if isinstance(event, TickEvent):
            if self.state == Game.STATE_PREPARING:
                self.Start()

#------------------------------------------------------------------------------
class Player:
    """..."""
    def __init__(self, evManager, controls, start_rect):
        self.evManager = evManager
        #self.evManager.RegisterListener(self)

        self.charactor = Charactor(evManager,controls,start_rect)

#------------------------------------------------------------------------------
class Charactor:
    """..."""
    def __init__(self, evManager, controls, start_rect):
        self.evManager = evManager
        self.evManager.RegisterListener(self)
        self.controls = controls
        self.combo = [-1,-1,-1]
        self.combo_sleep = -1
        self.hp = 500
        self.mp = 100
        self.speed = -1
        self.status = ""
        self.eyeDirection = DIRECTION_RIGHT
        self.up = False
        self.up_sleep = -1
        self.down = False
        self.down_sleep = -1
        self.left = False
        self.right = False
        self.jump_times = -1
        self.jump_dir = 0
        self.jump_sleep = -1
        self.jump_sleeph = -1
        self.jump_directions = [False,False,False,False]
        self.block_sleep = -1
        self.critical_sleep = -1
        self.damarea = pygame.Rect(0,0,0,0)
        self.damage_sim = 10
        self.damage_critical = 20
        self.falling_direction = -1
        self.start_rect = start_rect
        self.sprite = None
    #----------------------------------------------------------------------
#Wrote by Rodrigo
    def Move(self,direction):
        if direction == DIRECTION_UP and self.rect.top-1>=TOP_LIMIT:
            self.rect = self.rect.move([0,-1])
            ev = CharactorMoveEvent(self)
            self.evManager.Post(ev)
        elif direction == DIRECTION_DOWN and self.rect.bottom+1<=600:
            self.rect = self.rect.move([0,1])
            ev = CharactorMoveEvent(self)
            self.evManager.Post(ev)
        elif direction == DIRECTION_LEFT and self.rect.left-1>=0:
            self.rect = self.rect.move([-1,0])
            self.eyeDirection = DIRECTION_LEFT
            ev = CharactorMoveEvent(self)
            self.evManager.Post(ev)
        elif direction == DIRECTION_RIGHT and self.rect.right+1<=800:
            self.rect = self.rect.move([1,0])
            self.eyeDirection = DIRECTION_RIGHT
            ev = CharactorMoveEvent(self)
            self.evManager.Post(ev)
    #----------------------------------------------------------------------
#Wrote by Rodrigo
    def Walk(self, direction):
        if not self.status == "jumping" and not self.status == "dead" and not self.status == "damaged" and not self.status == "standby" and not self.status == "falling":
            if not self.status == "running":
                self.speed = 0
                self.status = "walking"
            
            if direction == DIRECTION_UP:
                self.up = True
                self.up_sleep = 0
            elif direction == DIRECTION_DOWN:
                self.down = True
                self.down_sleep = 0
            elif direction == DIRECTION_LEFT:
                self.left = True
            elif direction == DIRECTION_RIGHT:
                self.right = True
    #----------------------------------------------------------------------
#Wrote by Rodrigo
    def Walking(self):
        if self.speed == 0:
            self.speed = WALK_SPEED
            if self.up:
                if self.up_sleep == 0:
                    self.up_sleep = VERT_SPEED
                    self.Move(DIRECTION_UP)
                elif self.up_sleep > 0:
                    self.up_sleep -= 1
            if self.down:
                if self.down_sleep == 0:
                    self.down_sleep = VERT_SPEED
                    self.Move(DIRECTION_DOWN)
                elif self.down_sleep > 0:
                    self.down_sleep -= 1
            if self.left:
                self.Move(DIRECTION_LEFT)
            if self.right:
                self.Move(DIRECTION_RIGHT)
        elif self.speed > 0:
            self.speed -= 1

    #----------------------------------------------------------------------
#Wrote by Rodrigo
    def StopWalk(self, direction):
        if direction == DIRECTION_UP:
            self.up = False
            self.up_sleep = -1
        elif direction == DIRECTION_DOWN:
            self.down = False
            self.down_sleep = -1
        elif direction == DIRECTION_LEFT:
            self.left = False
        elif direction == DIRECTION_RIGHT:
            self.right = False

        if self.status == "walking" and not self.up and not self.down and not self.left and not self.right:
                self.speed = -1
                self.status = ""
    #----------------------------------------------------------------------
#Wrote by Rodrigo

#Loro, Criar frames diferenstes para a corrida.

    def Run(self):
        if not self.status == "jumping" and not self.status == "dead" and not self.status == "damaged" and not self.status == "standby" and not self.status == "falling":
            self.speed = 0
            self.status = "running"
    #----------------------------------------------------------------------
#Wrote by Rodrigo
    def Running(self):
        if self.speed == 0:
            self.speed = RUN_SPEED
            self.Move(self.eyeDirection)
            if self.up:
                if self.up_sleep == 0:
                    self.up_sleep = VERT_SPEED
                    self.Move(DIRECTION_UP)
                elif self.up_sleep > 0:
                    self.up_sleep -= 1
            if self.down:
                if self.down_sleep == 0:
                    self.down_sleep = VERT_SPEED
                    self.Move(DIRECTION_DOWN)
                elif self.down_sleep > 0:
                    self.down_sleep -= 1
        else:
            self.speed -= 1

    #----------------------------------------------------------------------
#Wrote by Rodrigo
    def StopRun(self):
         self.speed = -1
         self.status = ""
    #----------------------------------------------------------------------

#Wrote by Rodrigo

#Loro, criar frames diferentes para o pulo

    def Jump(self):
        if self.status == "walking":
            self.jump_directions[2] = True
            self.jump_sleeph = WALK_SPEED
        elif self.status == "running":
            self.jump_directions[3] = True
            self.jump_sleeph = RUN_SPEED

        if not self.status == "jumping" and not self.status == "damaged" and not self.status == "standby" and not self.status == "falling":
            self.status = "jumping"
            if(self.combo[0]!=-1):                 
                if self.combo[0] == self.controls[0]:
                    self.jump_directions[0] = True
                elif self.combo[0] == self.controls[1]:
                    self.jump_directions[1] = True
            elif self.combo[1]!=-1:                 
                if self.combo[1] == self.controls[0]:
                    self.jump_directions[0] = True
                elif self.combo[1] == self.controls[1]:
                    self.jump_directions[1] = True
            if self.jump_directions[0] == self.jump_directions[1] == True:
                self.jump_directions[0] = self.jump_directions[1] = False

            self.jump_times = 1
            self.jump_dir = 1
            self.jump_sleep = 0
    #----------------------------------------------------------------------
#Wrote by Rodrigo
    def JumpWalking(self):
        if self.jump_sleeph == 0:
            self.jump_sleeph = WALK_SPEED
            if self.eyeDirection == DIRECTION_LEFT:
                self.Move(DIRECTION_LEFT)
            else:
                self.Move(DIRECTION_RIGHT)
        elif self.jump_sleeph > 0:
            self.jump_sleeph -= 1
    #----------------------------------------------------------------------
#Wrote by Rodrigo

#Loro, criar frames diferentes para o pulo com corrida

    def JumpRunning(self):
        if self.jump_sleeph == 0:
            self.jump_sleeph = RUN_SPEED+1
            if self.eyeDirection == DIRECTION_LEFT:
                self.Move(DIRECTION_LEFT)
                self.Move(DIRECTION_LEFT)
            else:
                self.Move(DIRECTION_RIGHT)
                self.Move(DIRECTION_RIGHT)
        elif self.jump_sleeph > 0:
            self.jump_sleeph -= 1
            

    #----------------------------------------------------------------------
#Wrote by Rodrigo
    def SleepCalc(self,min,max):
        if self.jump_times-min <= (max-min)*1/10:
            return 1
        elif self.jump_times-min <= (max-min)*3/10:
            return 2
        elif self.jump_times-min <= (max-min)*6/10:
            return 3
        elif self.jump_times-min <= (max-min)*10/10:
            return 5
    #----------------------------------------------------------------------
#Wrote by Rodrigo
    def JumpGoingUp(self):
        if self.jump_directions[2]:
            self.JumpWalking()  
        elif self.jump_directions[3]:
            self. JumpRunning()

        if self.jump_times == MAX_JUMPS:
            self.jump_dir = 0

        if self.jump_sleep == 0:                
            self.Move(DIRECTION_UP)
            self.jump_sleep = self.SleepCalc(0,MAX_JUMPS)
            self.jump_times += 1;

        elif self.jump_sleep > 0:
            self.jump_sleep -= 1

    #----------------------------------------------------------------------
#Wrote by Rodrigo
    def JumpMaxStay(self):
        print "MAX!!"
        MAX_STAY = -1
        if self.status == "running":
            MAX_STAY = MAX_STAY_RUN
        elif self.status == "walking":
            MAX_STAY = MAX_STAY_WALK

        if self.jump_times <= MAX_JUMPS + MAX_STAY:
                self.jump_times += 1
                if self.jump_directions[2]:
                    self.JumpWalking()  
                elif self.jump_directions[3]:
                    self. JumpRunning()
        else :
            self.jump_times = MAX_JUMPS
            self.jump_dir = -1


    #----------------------------------------------------------------------
#Wrote by Rodrigo
    def JumpGoingDown(self):
        if self.jump_times == MAX_JUMPS:
            self.jump_times -= 1
        
        if self.jump_directions[2]:
            self.JumpWalking()  
        elif self.jump_directions[3]:
            self. JumpRunning()

        if self.jump_sleep == 0:                
            self.Move(DIRECTION_DOWN)
            self.jump_sleep = self.SleepCalc(0,MAX_JUMPS)
            self.jump_times -=1;
            
        elif self.jump_sleep > 0:
            self.jump_sleep -= 1

    #----------------------------------------------------------------------
#Wrote by Rodrigo
    def Jumping(self):
        ev = None
        if self.jump_dir == 1:
            self.JumpGoingUp()

        elif self.jump_dir == 0:
            self.JumpMaxStay()

        elif self.jump_dir == -1 and not self.jump_times == 0:
            self.JumpGoingDown()

        #End of the Jump
        elif self.jump_times == 0:
            ev = CharactorStopJumpEvent(self)
            self.evManager.Post(ev)

    #----------------------------------------------------------------------
#Wrote by Rodrigo
    def StopJump(self):
       self.jump_directions = [False,False,False,False]
       if self.up or self.down or self.left or self.right:
           self.status = "walking"
       else:
           self.status = ""
    #----------------------------------------------------------------------
#Wrote by Dedeu

#Loro, criar frames para o ataque


    def Attack(self,charactor):
        if not self.status == "jumping" and not self.status == "attacking" and not self.status == "dead" and not self.status == "standby" and not self.status == "walking" and not self.status == "damaged" and not self.status == "falling":
            if self.eyeDirection == DIRECTION_RIGHT:
                charactor.sprite.image = pygame.image.load("xiao_atk.png")
                ret = pygame.Rect(self.rect.right, self.rect.top+XIAO_HEIGHT/2, 5, 1) 
            else:
                charactor.sprite.image = pygame.transform.flip(pygame.image.load("xiao_atk.png"))
                ret = pygame.Rect(self.rect.left, self.rect.top+XIAO_HEIGHT/2, 5, 1) 
            self.damarea = ret
            self.status = "attacking"
            self.combo_hit = 1
            ev = CharactorAttackEvent(self)
            self.evManager.Post(ev)
        elif self.status == "attacking":
            if self.combo[0] == self.controls[4]:
                print "CRITICAL HIT!"
                self.critical_sleep = CRITICAL_SLEEP
                self.CleanCombo
                self.combo_hit = 3
                self.status = "standby"
            else:
                self.combo_hit = 2
            ev = CharactorAttackEvent(self)
            self.evManager.Post(ev)

    #------------------------------------------------------------------------
 
#Loro, criar frames para o dano (note que q deve ter um para o dano normal e outro para o dano critico, incluindo a queda)

    def Damaged (self, charactor):
        if self != charactor and self.rect.colliderect(charactor.damarea) and not self.status == "blocking":
            if charactor.combo_hit != 3:
                self.hp -= charactor.damage_sim
                self.status = "damaged"
                self.dam_sleep = DAMAGED_SLEEP
            else:
                print "RECIEVED CRITICAL!"
                self.hp -= charactor.damage_critical
                self.status = "falling"
                self.falling_direction = charactor.eyeDirection
                self.dam_sleep = FALLING_SLEEP
            print(self.hp)
        elif self.status == "blocking":
            if charactor.combo_hit == 3:
                self.status = ""
            print(self.hp)

    #------------------------------------------------------------------------

#Loro, criar frames para a defesa

    def Defend (self):
        if not self.status == "damaged" and not self.status == "jumping" and not self.status == "blocking" and not self.status == "dead" and not self.status == "standby" and not self.status == "falling":
            self.status = "blocking"
            self.block_sleep = 10000   
    #----------------------------------------------------------------------
#Wrote by Rodrigo
    def Place(self):
        self.rect = self.start_rect
        ev = CharactorPlaceEvent(self)
        self.evManager.Post(ev)
    #----------------------------------------------------------------------
#Wrote by Rodrigo    
    def Add2Combo(self, key):
        self.combo_sleep = COMBO_SLEEP        
        if(len(self.combo)<3):
            self.combo.append(key)
        else:
            self.combo.pop(0)
            self.combo.append(key)
        print self.combo
        ev = CharactorAdd2ComboEvent(self)
        self.evManager.Post(ev)
    #----------------------------------------------------------------------
#Wrote by Rodrigo    
    def VerifyCombo(self):
        combo_atual = -1
        if self.combo[2] == self.controls[2]:
            combo_atual = DIRECTION_LEFT
        elif self.combo[2] == self.controls[3]:
            combo_atual = DIRECTION_RIGHT

        if self.combo[1] == self.controls[3] and self.combo[2] == self.controls[3] and not self.status == "running":
            combo_atual = DIRECTION_RIGHT
            ev = CharactorRunEvent(self)
            self.evManager.Post(ev)
        elif self.combo[1] == self.controls[2] and self.combo[2] == self.controls[2] and not self.status == "running":
            combo_atual = DIRECTION_LEFT
            ev = CharactorRunEvent(self)
            self.evManager.Post(ev)
        elif self.status == "running" and self.combo[2] != self.controls[0] and self.combo[2] != self.controls[1]:
            if (self.eyeDirection == DIRECTION_LEFT and combo_atual == DIRECTION_RIGHT) or (self.eyeDirection == DIRECTION_RIGHT and combo_atual == DIRECTION_LEFT):
                ev = CharactorStopRunEvent(self)
                self.evManager.Post(ev)


    #----------------------------------------------------------------------
#Wrote by Rodrigo    
    def CleanCombo(self):
        self.combo_sleep = -1
        self.combo = [-1,-1,-1]
        if self.status == "attacking":
            self.status = ""
            self.combo_hit = 0
            self.damarea = pygame.Rect(0,0,0,0)

    #----------------------------------------------------------------------
#Wrote by Rodrigo    
    def Notify(self, event):
        if isinstance(event, GameStartedEvent):
#            map = event.game.map
            self.Place()

        elif isinstance(event, CharactorMoveRequest):
            self.Move(event.direction)

        elif isinstance(event, CharactorWalkEvent) and event.charactor == self:
            self.Walk(event.direction)

        elif isinstance(event, CharactorStopWalkEvent) and event.charactor == self:
            self.StopWalk(event.direction)

        elif isinstance(event, CharactorRunEvent) and event.charactor == self:
            self.Run()

        elif isinstance(event, CharactorStopRunEvent) and event.charactor == self:
            self.StopRun()

        elif isinstance(event, CharactorJumpRequest) and event.charactor == self:
            self.Jump()

        elif isinstance(event, CharactorStopJumpEvent) and event.charactor == self:
            self.StopJump()
      
        elif isinstance(event, CharactorAttackRequest) and event.charactor == self:
            self.Attack(event.charactor)

        elif isinstance(event, CharactorDefendRequest) and event.charactor == self:
            self.Defend()
    
        elif isinstance(event, CharactorAttackEvent):
            self.Damaged(event.charactor)
  
        elif isinstance(event, CharactorAdd2ComboRequest) and event.charactor == self:
            self.Add2Combo(event.key)

        elif isinstance(event, CharactorAdd2ComboEvent)and event.charactor == self:
            self.VerifyCombo()

        elif isinstance(event, TickEvent):
            if self.hp <= 0:
                self.status == "dead"

            elif self.status == "jumping":
                self.Jumping()   

            elif self.status == "running":
                self.Running()

            elif self.status == "walking":
                self.Walking()

            elif self.status == "blocking":
                if self.block_sleep == 0:
                    self.status = ""
                else:
                    self.block_sleep -= 1

            elif self.status == "standby":
                if self.critical_sleep == 0:
                    self.status = ""
                else:
                   self.critical_sleep -= 1

            elif self.status == "falling":
                if self.dam_sleep == 0:
                    self.status = ""
                    self.falling_direction = -1
                elif self.dam_sleep > 0:
                    if self.dam_sleep%RUN_SPEED == 0 and self.dam_sleep >= 740:      
                        self.Move(self.falling_direction)
                    self.dam_sleep -= 1         
    
            elif self.status == "damaged":
                if self.dam_sleep == 0:
                    self.status = ""
                    self.falling_direction = -1
                else:
                    self.dam_sleep -= 1

            if self.combo_sleep==0:
                self.CleanCombo()
            elif self.combo_sleep>0:
                self.combo_sleep -= 1
              


