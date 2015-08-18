# Created by a human
# when:
#8/15/2015
#11:49 AM
from utilities import *
import random
import math
random.seed()

#---------------------------------------------------------------------------------------------
# This is the Master, so it lords over other subclasses in the entities kingdom
#---------------------------------------------------------------------------------------------
class Master(pygame.sprite.Sprite):
#   -the attributes-
    active = False
    owner = None
    usable = False
    immortal = False

#   -entity health
    hp = 100
#   -the max it can be
    max_hp = 100
#   -amount added when health is added to
    med = 0
#   -dictionary to hold various frame lists
    frames = {}
#   -list to hold various state methods
    states = []
#   -the current state of the entity
    state = None
    image = None
    rect = None
    xvel = 0
    yvel = 0
    speed = (xvel, yvel)
    target = None
    direction = None
    damage = 0
    direction_dictionary = {
        'up' : (0,1),
        'down' : (0,-1),
        'left': (-1,0),
        'right': (1,0)}
    up = direction_dictionary['up']
    down = direction_dictionary['down']
    left = direction_dictionary['left']
    right = direction_dictionary['right']

    opposite_direction = {
        'up':'down',
        'down':'up',
        'left':'right',
        'right':'left'}

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)


    def activate(self):
        self.active = True
        return self.seek()

    def deactivate(self):
        if self.active:
            self.active = False
        self.xvel = 0
        self.yvel = 0
        return

    def die(self):
        if not self.immortal:
            self.kill()

    def set_position(self, (x, y)):
        self.rect.x += x
        self.rect.y += y

    def get_position(self):
        return self.rect.topleft

    def get_hit(self, damage):
        self.hp -= damage
        if self.hp < 1:
            self.die()

    def hitting(self, what):
        damage = self.damage
        what.hp -= damage

    def move(self, (x,y)):
        self.speed = (x,y)

    def speedX(self, x):
        self.xvel = x
    def speedY(self, y):
        self.yvel = y

#   - method to be used for self.state-
    def seek(self):
        self.rect.x += self.xvel
        (sx, sy) = self.get_position()
        (tx, ty) = self.target.get_position()
        if sx > tx:
            self.xvel = -1
            self.direction = "right"
        elif sx < tx:
            self.xvel = 1
            self.direction = "left"
        self.rect.y += self.yvel
        if sy > ty:
            self.yvel = -1
            self.direction = "up"
        elif sy < ty:
            self.yvel = 1
            self.direction = "down"

    def update(self):
        pass

    def display(self, screen):
        pass

    def collisions(self, objects):
        pass
