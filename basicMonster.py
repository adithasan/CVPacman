import basicSprite
import pygame
import random

'''A class for Monsters.
Loads the '''
class Monster(basicSprite.Sprite):
    def __init__(self,centerPoint,image,weakMon_image = None):
        basicSprite.Sprite.__init__(self,centerPoint,image)
        # Store the original rect information
        self.original_rect = pygame.Rect(self.rect)
        self.normal_image = image
        if weakMon_image != None:
            self.weakMon_image = weakMon_image
        else:
            self.weakMon_image = image
        self.weak = False
        #When the variable movecount matches the random number self.moves,
        #the next direction will be randomly chosen
        #Here is the initialization of each variables
        self.direction = random.randint(1,4)
        self.dist = 1
        self.moves = random.randint(100,200)
        self.moveCount = 0;
    def update(self,brick_group):
        '''This function updates the movement of the Monster'''
        x_move,y_move = 0,0
        if self.direction==1:
            #Move left
            x_move = -self.dist
        elif self.direction==2:
            #Move up
            y_move = -self.dist
        elif self.direction==3:
            #Move right
            x_move = self.dist
        elif self.direction==4:
            #Move down
            y_move = self.dist
        self.rect.move_ip(x_move,y_move)
        self.moveCount += 1

        if pygame.sprite.spritecollideany(self, brick_group):
            #in case the monster hits the brick, it should reverse the movement
            self.rect.move_ip(-x_move,-y_move)
            self.direction = random.randint(1,4)
        elif self.moves == self.moveCount:
            # at a certain time, the monster will change its direction
            self.direction = random.randint(1,4)
            self.moves = random.randint(100,200)
            self.moveCount = 0;
    def M_dead(self):
        '''When the monster is dead, they will be regenerated at their original position
        This function used the previouly stored rect information to regenerate the monster

        Parameter:
        self = Monster: a class itself
        '''
        self.weak = False
        self.rect = self.original_rect
        self.image = self.normal_image

    def weakMon(self,weak):

        '''This functino checked whether the monster should be in weak stage
        When the monster is in weak stage, change the image to weakMon_image.
        Else it is normal_image

        Parameters:
        self = Monster: a class itself
        weak = a bool stage: if weak is True it is in weak stage
                else it is not.

        '''
        if self.weak != weak:
            self.weak = weak
            if weak:
                self.image = self.weakMon_image
            else:
                self.image = self.normal_image
