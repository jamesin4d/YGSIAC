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

class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

#-----------------------------------------------------------------
# the special bullet class that doesn't inherit from the Base sprite
#-----------------------------------------------------------------
class Bullet(Entity):
    def __init__(self, loc, angle):
        Entity.__init__(self)
        self.frames = SpriteSheet.strip_sheet('img/b_sheet.png',96,16,16,16)
        self.original_image = self.frames[0]
        self.angle = -math.radians(angle-136)
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect(center=loc)
        self.move = [self.rect.x, self.rect.y]
        self.speed_mod = 10
        self.speed = (self.speed_mod*math.cos(self.angle),
                      self.speed_mod*math.sin(self.angle))

        # remember when you were like, 'wtf does @staticmethod mean' well see this shit below, it means you don't need to
        # create an active instance of SpriteSheet() to use that method, it just works like so:

    def check_collisions(self, objects):
        for o in objects:
            if pygame.sprite.collide_rect(self, o):
                self.kill()

# a brief explainer on the animation method here
    def anim(self):
        # if the x-axis has speed applied to it
        if self.speed[0] != 0:
            # essentially:
            # frame = the currently displayed frame
            #  (x // y)- returns (floored) quotient of x and y
            # the ' % ' is called a modulus in python, it returns the remainder of something.
            # so what this line does is as the x-axis moves, itterate over the length(self.frames) I think
            frame = (self.rect.x//40) % len(self.frames) # how this equation actually works is something of a black box for me.
            #this is just one of those things that wasn't clearly explained wherever I learned it from, but works so I don't ask any questions.
            # https://docs.python.org/2/library/stdtypes.html <-- head there for *some* further help.
            self.image = pygame.transform.rotate(self.frames[frame], self.angle)
        elif self.speed[1] != 0:
            frame = (self.rect.y//40) % len(self.frames)
            self.image = pygame.transform.rotate(self.frames[frame], self.angle)

    def update(self, objects):
        self.check_collisions(objects)
        self.move[0] += self.speed[0]
        self.move[1] += self.speed[1]
        self.rect.topleft = self.move
        self.anim()
    def remove(self, screen_rect):
        if not self.rect.colliderect(screen_rect):
            self.kill()

class EnemyBullet(Entity):
    def __init__(self, loc, angle):
        Entity.__init__(self)
        self.original_image = pygame.image.load("img/badbullet.png")
        self.angle = -math.radians(angle-136)
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect(center=loc)
        self.move = [self.rect.x, self.rect.y]
        self.speed_mod = 10
        self.speed = (self.speed_mod*math.cos(self.angle),
                      self.speed_mod*math.sin(self.angle))

    def check_collisions(self, objects):
        for o in objects:
            if pygame.sprite.collide_rect(self, o):
                self.kill()

    def update(self, objects):
        self.check_collisions(objects)
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
class Base(Entity):
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
    movement_rate = 0 # every entity should get a movement_rate to determine how fast they're allowed to move

    walking_frames_left = [] # lists to hold walking frames
    walking_frames_right = [] # pulled from a spritesheet
    walking_frames_down = []
    walking_frames_up = []

    def __init__(self):
        Entity.__init__(self)

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
        self.rect = pygame.Rect((0,0,32,20))

    def set_position(self, x, y):
        # position setter method
        self.rect.x = x
        self.rect.y = y

    def acquire_location(self):
        r = self.rect
        left = r.left
        right = r.right
        top = r.top
        bottom = r.bottom
        midleft = r.midleft
        midright = r.midright
        midtop = r.midtop
        midbottom = r.midbottom
        rectangle = (left, right, top, bottom)
        rectangle_two = (midleft,midright,midtop,midbottom)
        #print rectangle
        #print rectangle_two
        return rectangle

    def aim(self, target):
        offset = (target.rect.centery - self.rect.centery, target.rect.centerx - self.rect.centerx)
        self.angle = 135 - math.degrees(math.atan2(*offset))
        return self.angle

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

# below are the various movement methods used to manuever entities around
    def move_x(self, x):
        self.xvelocity = x
    def move_y(self, y):
        self.yvelocity = y
    def move(self, x,y):
        return self.move_x(x), self.move_y(y)

    def check_collisions(self, objects):
        pass

    def animate(self):
        if self.xvelocity < 0:
            self.direction = 'left'
        if self.xvelocity > 0:
            self.direction = 'right'
        if self.yvelocity < 0:
            self.direction = 'up'
        if self.yvelocity > 0:
            self.direction = 'down'
        if self.direction == 'left':
            frame = (self.rect.x//25) % len(self.walking_frames_left)
            self.image = self.walking_frames_left[frame]
        if self.direction == 'right':
            frame = (self.rect.x//25) % len(self.walking_frames_right)
            self.image = self.walking_frames_right[frame]
        if self.direction == 'up':
            frame = (self.rect.y//20) % len(self.walking_frames_up)
            self.image = self.walking_frames_up[frame]
        if self.direction == 'down':
            frame = (self.rect.y//20) % len(self.walking_frames_down)
            self.image = self.walking_frames_down[frame]

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




