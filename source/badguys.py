# Created by a human
# when:
# 8/14/2015
# 10:38 AM
from entities import *
from utilities import SpriteSheet
import pygame
import random
import math
import time
random.seed()


# mapper class produces a variable equal to: sort_data(return)
def sort_enemy_data(x, y, id_k, image):
    return x, y, id_k, image

# sort_data is then passed as the 'what' argument here
def sort_by_type(what):
    id_key = what[2] #the id_key is unique for every tile
    if id_key == 28: #just assign which id_key you want for
        enemy = Walker()#each type of enemy
        enemy.image = what[3] #Mapper.all_tiles[id_key]
        enemy.rect = pygame.Rect(what[0], what[1], 32, 32)
        return enemy
    if id_key == 117:
        enemy = Turret()
        enemy.image = what[3]
        enemy.rect = pygame.Rect(what[0], what[1], 32, 32)
        return enemy


class TurretBullet(Master):
    def __init__(self, owner):
        self.image = pygame.image.load('img/bullet2.png')
        self.rect = self.image.get_rect()
        self.owner = owner
        self.target = owner.target
        self.vector = None
        self.speed = 10
        self.damage = 5
        self.exact_pos = list(self.rect.topleft)

        Master.__init__(self)

    def getVector(self):
        targ = self.target
        own = self.owner
        x = targ.rect.centerx-own.rect.centerx
        y = targ.rect.centery-own.rect.centery
        m = math.hypot(x,y)
        vec_x = self.speed*(x/m)
        vec_y = self.speed*(y/m)
        return (vec_x, vec_y)

    def update(self):
        self.old_pos = self.exact_pos[:]
        if not self.vector:
            self.vector = self.getVector()
        self.exact_pos[0] += self.vector[0]
        self.exact_pos[1] += self.vector[1]
        self.rect.topleft = self.exact_pos

# Turret enemy class
# enemy_id: 117
class Turret(Master):
    def __init__(self):
        Master.__init__(self)
        self.hp = random.randint(50, 80)
        self.bullets = pygame.sprite.Group()
        self.active = False
        self.screen = pygame.display.get_surface()
        self.canShoot = False

    def activate(self):
        self.active = True
        return
    def deactivate(self):
        im = pygame.image.load('img/turret2.png')
        self.image = im
        self.active = False
        return
    def set_target(self):
        return self.target.get_position()

    def display(self, screen):
        self.bullets.draw(screen)

#----------------------------------------------------------------------------------
# Generic walking enemy
# enemy_id: 28
#----------------------------------------------------------------------------------
class Walker(Master):
    WFL = []
    WFR = []
    WFD = []
    WFU = []
    sheets = ['img/greymen.png',
              'img/br_bluemen.png',
              'img/brownmen.png',
              'img/greenmen.png',
              'img/br_greenmen.png',
              'img/yellowmen.png'
              ]
    sprite_sheet = random.choice(sheets)
    def __init__(self, ):
        # - ask the Master class first...
        Master.__init__(self)
        self.active = True
        #set up a small amount of hp, weak enemies
        self.hp = random.randint(10, 40)
        # this chooses a random sprite sheet from the list ^above^
        s = SpriteSheet(self.sprite_sheet)
#-------------------------get some images, fill some lists----------
#-------- right images
        image = s.get_image(0, 32, 32, 32)
        self.WFL.append(image)
        image = s.get_image(32, 32, 32, 32)
        self.WFL.append(image)
        image = s.get_image(64, 32, 32, 32)
        self.WFL.append(image)
#--------- left images
        image = s.get_image(0, 64, 32, 32)
        self.WFR.append(image)
        image = s.get_image(32, 64, 32, 32)
        self.WFR.append(image)
        image = s.get_image(64, 64, 32, 32)
        self.WFR.append(image)
#------- down images
        image = s.get_image(0, 0, 32, 32)
        self.WFD.append(image)
        image = s.get_image(32, 0, 32, 32)
        self.WFD.append(image)
        image = s.get_image(64, 0, 32, 32)
        self.WFD.append(image)
#------- up images
        image = s.get_image(0, 96, 32, 32)
        self.WFU.append(image)
        image = s.get_image(32, 96, 32, 32)
        self.WFU.append(image)
        image = s.get_image(64, 96, 32, 32)
        self.WFU.append(image)
        self.image = self.WFD[0]
        self.rect = pygame.Rect(32, 32, 32, 22)

    def update(self):
        if self.active:
            if self.direction == "left":
                frame = (self.rect.x // 30) % len(self.WFL)
                self.image = self.WFL[frame]
            elif self.direction == "right":
                frame = (self.rect.x // 30) % len(self.WFR)
                self.image = self.WFR[frame]
            elif self.direction == "up":
                frame = (self.rect.y // 30) % len (self.WFU)
                self.image = self.WFU[frame]
            elif self.direction == "down":
                frame = (self.rect.y // 30) % len (self.WFD)
                self.image = self.WFD[frame]
            else:
                self.image = self.WFD[0]
        else:
            self.xvel = 0
            self.yvel = 0


