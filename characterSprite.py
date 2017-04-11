import basicSprite
import pygame
from pygame.locals import *
import basicMonster
SUPER_STATE_START = pygame.USEREVENT + 1
SUPER_STATE_OVER = SUPER_STATE_START + 1
SNAKE_EATEN = SUPER_STATE_OVER + 1

class Character(basicSprite.Sprite):
    def __init__(self, centerPoint, image):
        basicSprite.Sprite.__init__(self, centerPoint, image)
        #Initialize the number of pellets eaten
        self.pellets = 0
        # set the number of pixels to move each set_repeat
        self.dist=3
        # Initialize how much the character moves
        self.x_move = 0
        self.y_move = 0
        self.direction = 0
        self.nextdir = 0
        self.xdir = [0,-self.dist,self.dist,0,0]
        self.ydir=[0,0,0,-self.dist,self.dist]

    def MoveKeyDown(self, key):
        '''This function sets the x_move or y_move variables
        that will then move the snake when update() function
        is called. The x_move and y_move values will be returned
        to normal when this MoveKeyUp function is called'''

        self.direction=self.nextdir

        if (key == K_RIGHT):
            self.nextdir=2
        elif (key == K_LEFT):
            self.nextdir=1
        elif (key == K_UP):
            self.nextdir=3
        elif (key == K_DOWN):
            self.nextdir=4



    def MoveKeyUp(self, key):
        '''This function resets the x_move or y_move variables'''
        if key == K_RIGHT:
          self.x_move += -self.x_dist
        elif key == K_LEFT:
          self.x_move += self.x_dist
        elif key == K_UP:
          self.y_move += self.y_dist
        elif key == K_DOWN:
          self.y_move += -self.y_dist


    def update(self, brick_group,pellet_group,monster_group,big_pellet_group):
        '''called when the Character spirit should update itself'''
        self.xMove=self.xdir[self.nextdir]
        self.yMove=self.ydir[self.nextdir]

        self.rect.move_ip(self.xMove,self.yMove)

        """IF we hit a block, don't move - reverse the movement"""
        if pygame.sprite.spritecollide(self, brick_group, False):
            self.rect.move_ip(-self.xMove,-self.yMove)
            """IF we can't move in the new direction... continue in old direction"""
            self.xMove=self.xdir[self.direction]
            self.yMove=self.ydir[self.direction]
            self.rect.move_ip(self.xMove,self.yMove)
            if pygame.sprite.spritecollide(self, brick_group, False):
                self.rect.move_ip(-self.xMove,-self.yMove)
                self.yMove=0
                self.xMove=0
                self.direction=0
                self.nextdir=0
        else:
                self.direction=0




        lst_monsters = pygame.sprite.spritecollide(self,monster_group,False)
        # Monster, Character collision check
        if len(lst_monsters)>0:
            # Collide with a monster
            self.MonsterCollide(lst_monsters)
        else:
            # Character, Pellets collision check
            lst_pellet = pygame.sprite.spritecollide(self,pellet_group,True)
            if len(lst_pellet)>0:
                # Collide with normal pellets
                self.pellets += len(lst_pellet)
            elif len(pygame.sprite.spritecollide(self, big_pellet_group, True))>0:
                # Collide with super pellets
                self.superState = True
                pygame.event.post(pygame.event.Event(SUPER_STATE_START,{}))
                pygame.time.set_timer(SUPER_STATE_OVER,0)
                pygame.time.set_timer(SUPER_STATE_OVER,3000)

    def MonsterCollide(self,lst):
        '''This function is used when there is a collision between monster
        and character.

        Parameters
        self = Character class itself
        lst = list of monsters has been hit by the character'''
        if len(lst)<=0:
            #list is empty, did not hit anything
            return
        for monster in lst:
            if monster.weak:
                monster.M_dead()
            else:
                pygame.event.post(pygame.event.Event(SNAKE_EATEN,{}))
