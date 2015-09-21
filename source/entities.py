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

# Empty sprite parent class for all to inherit from!
# COME ONE, COME ALL!
class Entity(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

# these are the basic map tiles that the map parsing module creates from
# json data, background tiles and solid tiles are put into seperate lists
# to differentiate between the two for collisions
class BackgroundTile(Entity):
    def __init__(self):
        Entity.__init__(self)

class SolidBlock(Entity):
    def __init__(self):
        Entity.__init__(self)

class ExitBlock(Entity):
    def __init__(self):
        Entity.__init__(self)


# ------------------------------------------------------------
# Base sprite parent class, holds attributes to inherit
# as well as some commonly used methods
#-------------------------------------------------------------
class Base(Entity):
    # empty attributes for children classes to inherit
    health = 0 # the current level of health       
    max_health = 0.0 # the maximum allowed to the entity
    xvelocity = 0 # velocity applied to the x-axis
    yvelocity = 0 # velocity applied to the y-axis

    angle = None # angle is used to determine the angle the bullets shoot at
    dead = False # true if dead
    canShoot = False # true if entity has a weapon that can shoot
    moving = False #true if xvel or yvel != 0
    moving_right = False # true if xvel > 0
    moving_left = False # true if xvel < 0
    jumping = False # true if not on ground and yvel < 0
    falling = False # true if not on ground and yvel > 0
    onGround = False # true if entity has bottom collision
    canJump = False # true if on ground is true
    direction = None # a string of either 'left'/'right'/'up'

    walking_frames_left = [] # lists to hold walking frames
    walking_frames_right = [] # pulled from a spritesheet
    jump_frames_right = []  #jump frames
    jump_frames_left = []
    punch_frames_left = [] # punching frames
    punch_frames_right = []
    idle_frames_left = [] # standing still frames
    idle_frames_right = []
    image = None # which image is being shown
    rect = None # the collision rectangle

    walk_speed = 0
    jump_speed = 0
    gravity = 0.4

    collide_right = False
    collide_left = False
    collide_top = False
    collide_bottom = False

    def __init__(self):
        Entity.__init__(self)

    def get_frames(self, walkL, walkR, jumpL, jumpR, punchL, punchR, idleL, idleR):
        # JESUS FUCK ROBIN! LOOK HOW SHORT THIS FRAME GETTING METHOD GOT!
        strip = SpriteSheet.strip_sheet
        # refer to utilities.SpriteSheet.strip_sheet() for argument explainations

        self.walking_frames_left = strip(walkL,96,20,16,20)
        self.walking_frames_right = strip(walkR,96,20,16,20)

        self.jump_frames_right = strip(jumpR,48,20,16,20)
        self.jump_frames_left = strip(jumpL,48,20,16,20)

        self.punch_frames_left = strip(punchL,48,20,16,20)
        self.punch_frames_right = strip(punchR,48,20,16,20)

        self.idle_frames_left = strip(idleL,48,20,16,20)
        self.idle_frames_right = strip(idleR,48,20,16,20)

        self.image = self.idle_frames_right[2]
        self.rect = pygame.Rect((0,0,16,20))

    def set_position(self, (x, y)):
        # position setter method
        self.rect.x = x
        self.rect.y = y
    
    def get_position(self):
            #position get method, returns (x,y)
            return self.rect.topleft

    def get_rect_position(self):
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
        print "left, right, top, bottom"
        print rectangle
        print 'midleft, midright, midtop, midbottom'
        print rectangle_two
        return rectangle

    def aim(self, target):
        offset = (target.rect.centery - self.rect.centery, target.rect.centerx - self.rect.centerx)
        self.angle = 135 - math.degrees(math.atan2(*offset))
        return self.angle

    def take_damage(self, quanta):
        self.health -= quanta
        if self.health < 1:
            self.kill()
            self.dead = True

    def give_damage(self, what):
        damage = self.damage
        what.health -= damage

# below are the various movement methods used to manuever entities around
    def move_x(self, x):
        self.xvelocity = x
    def move_y(self, y):
        self.yvelocity = y
    def move(self, x,y):
        return self.move_x(x), self.move_y(y)

    def walk(self, speed):
        return self.move_x(speed)


    def jump(self, speed):
        if self.canJump:
            self.jumping = True
            self.onGround = False
            self.move_y(speed)

    def move_and_check(self, objs):
        self.rect.x += self.xvelocity
        self.collide_left = False
        self.collide_right = False
        self.check_for_collision(self.xvelocity, 0, objs)
        self.rect.y += self.yvelocity
        self.collide_top = False
        self.collide_bottom = False
        self.check_for_collision(0, self.yvelocity, objs)

        if self.xvelocity < 0:
            self.moving_left = True
            self.direction = 'left'
        elif self.xvelocity > 0:
            self.moving_right = True
            self.direction = 'right'
        else:
            self.moving_right = False
            self.moving_left = False

        if self.yvelocity < 0:
            self.jumping = True
        if self.yvelocity > 0:
            self.falling = True

        if not self.onGround:
            self.canJump = False
            self.yvelocity += self.gravity
            if self.yvelocity > 20:
                self.yvelocity = 20

        if self.onGround:
            self.canJump = True
            self.jumping = False
            self.falling = False

        if self.falling or self.jumping:
            self.onGround = False

        if self.xvelocity != 0 or self.jumping or self.falling:
            self.moving = True
        else: self.moving = False


    def check_for_collision(self, xvel, yvel, objects):
        self.onGround = False
        for obj in objects:
            if pygame.sprite.collide_rect(self, obj):
                if xvel < 0:
                    self.rect.left = obj.rect.right
                    self.collide_left = True
                if xvel > 0:
                    self.rect.right = obj.rect.left
                    self.collide_right = True
                if yvel < 0:
                    self.rect.top = obj.rect.bottom
                    self.collide_top = True
                if yvel > 0:
                    self.rect.bottom = obj.rect.top
                    self.onGround = True
                    self.collide_bottom = True

    def animate(self):
        if self.moving_left:
            frame = (self.rect.x//15) % len(self.walking_frames_left)
            self.image = self.walking_frames_left[frame]
        if self.moving_right:
            frame = (self.rect.x//15) % len(self.walking_frames_right)
            self.image = self.walking_frames_right[frame]
        if self.jumping:
            if self.direction == "left":
                self.image = self.jump_frames_left[2]
            if self.direction == "right":
                self.image = self.jump_frames_right[0]
        if self.falling:
            if self.direction == "left":
                frame = (self.rect.y//10) % len(self.jump_frames_left)
                self.image = self.jump_frames_left[frame]
            if self.direction == "right":
                frame = (self.rect.y//10) % len(self.jump_frames_right)
                self.image = self.jump_frames_right[frame]

        if not self.moving:
            if self.direction == "right":
                self.image = self.idle_frames_right[0]

            if self.direction == "left":
                self.image = self.idle_frames_left[2]

    def update(self, objects):
        pass






