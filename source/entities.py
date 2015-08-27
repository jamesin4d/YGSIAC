# Created by a human
# when:
#8/22/2015
#4:46 AM
#
# Rewriting entities/player/nearly everything to be less of a mess
# and hopefully be better to read and work with
#--------------------------------------------------------------------
from utilities import *
import math
import random
random.seed()

#-----------------------------------------------------------------
# the special bullet class that doesn't inherit from the Base sprite
#-----------------------------------------------------------------
class Bullet(pygame.sprite.Sprite):
    def __init__(self, loc, angle):
        pygame.sprite.Sprite.__init__(self)
        image = pygame.image.load("img/bullet2.png")
        self.original_image = image
        self.angle = -math.radians(angle-136)
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect(center=loc)
        self.move = [self.rect.x, self.rect.y]
        self.speed_mod = 10
        self.speed = (self.speed_mod*math.cos(self.angle),
                      self.speed_mod*math.sin(self.angle))
        self.done = False

    def update(self):
        self.move[0] += self.speed[0]
        self.move[1] += self.speed[1]
        self.rect.topleft = self.move

    def remove(self, screen_rect):
        if not self.rect.colliderect(screen_rect):
            self.kill()

# ------------------------------------------------------------
# Base sprite parent class, holds attributes to inherit
# as well as some commonly used methods
#-------------------------------------------------------------
class Base(pygame.sprite.Sprite):
    direction = None # used for determining which frame is shown
    dead = False     # self
    canShoot = False # explanatory
    health = 0       # variables
    max_health = 0.0 # here

    image = None
    rect = None
    xvelocity = 0
    yvelocity = 0
    angle = None

    walking_frames_left = [] # lists to hold walking frames
    walking_frames_right = [] # pulled from a spritesheet
    walking_frames_down = []
    walking_frames_up = []
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

    def get_frames(self, spritesheet):
        self.walking_frames_down = []
        self.walking_frames_up = []
        self.walking_frames_right = []
        self.walking_frames_left = []
        sheet = spritesheet
        s = SpriteSheet(sheet)

        # left walking frames
        i = s.get_image(0,32,32,32)
        self.walking_frames_left.append(i)
        i = s.get_image(32,32,32,32)
        self.walking_frames_left.append(i)
        i = s.get_image(64,32,32,32)
        self.walking_frames_left.append(i)

        # right walking frames
        i = s.get_image(0,64,32,32)
        self.walking_frames_right.append(i)
        i = s.get_image(32,64,32,32)
        self.walking_frames_right.append(i)
        i = s.get_image(64,64,32,32)
        self.walking_frames_right.append(i)

        # down walking frames
        i = s.get_image(0,0,32,32)
        self.walking_frames_down.append(i)
        i = s.get_image(32,0,32,32)
        self.walking_frames_down.append(i)
        i = s.get_image(64,0,32,32)
        self.walking_frames_down.append(i)
        # up walking frames

        i = s.get_image(0,96,32,32)
        self.walking_frames_up.append(i)
        i = s.get_image(32,96,32,32)
        self.walking_frames_up.append(i)
        i = s.get_image(64,96,32,32)
        self.walking_frames_up.append(i)

        self.image = self.walking_frames_down[0]
        self.rect = self.image.get_rect()

    def set_position(self, x, y):
        # position setter method
        self.rect.x = x
        self.rect.y = y

    def get_position(self):
        #position get method, returns (x,y)
        return self.rect.topleft

    def take_damage(self, quanta):
        self.health -= quanta
        if self.health < 1:
            self.kill()
            self.dead = True

    def give_pain(self, what):
        damage = self.damage
        what.health -= damage

    def move_x(self, x):
        self.xvelocity = x


    def move_y(self, y):
        self.yvelocity = y

    def check_collisions(self, objects):
        pass

    def update(self):
        pass

class Tile(Base):
    def __init__(self):
        Base.__init__(self)


class Solid(Base):
    health = 1000
    max_health = 1000.0
    def __init__(self):
        Base.__init__(self)


class Exit(Base):
    def __init__(self):
        Base.__init__(self)




