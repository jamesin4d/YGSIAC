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
        self.image = None

# these are the basic map tiles that the map parsing module creates from
# json data, background tiles and solid tiles are put into seperate lists
# to differentiate between the two for collisions
class BackgroundTile(Entity):
    def __init__(self):
        Entity.__init__(self)

class SolidBlock(Entity):
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
    attacking = False #true if entity is attacking
    attack_released = False
    hit_timer = Timer(30)
    hit_timer.deactivate()

    image = None # which image is being shown
    rect = None # the collision rectangle

    walk_speed = 0
    jump_speed = 0
    gravity = 0

    collide_right = False
    collide_left = False
    collide_top = False
    collide_bottom = False


    action_timer = 0
    idle = False

    def __init__(self):
        Entity.__init__(self)

    @staticmethod
    def get_frames(frame_sheet, ix, iy, fx, fy):
        # JESUS FUCK ROBIN! LOOK HOW SHORT THIS FRAME GETTING METHOD GOT!
        strip = SpriteSheet.strip_sheet
        return strip(frame_sheet, ix, iy, fx, fy)


    def set_position(self, (x, y)):
        # position setter method
        self.rect.x = x
        self.rect.y = y

    def get_position(self):
        #position get method, returns (x,y)
        return self.rect.topleft

    def aim(self, target):
        offset = (target.rect.centery - self.rect.centery, target.rect.centerx - self.rect.centerx)
        self.angle = 135 - math.degrees(math.atan2(*offset))
        return self.angle

    def take_damage(self, quanta):
        if not self.hit_timer.active:
            self.hit_timer.activate()
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

    def walk_left(self):
        return self.move_x(-self.walk_speed)

    def walk_right(self):
        return self.move_x(self.walk_speed)

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
            if self.yvelocity > 3:
                self.yvelocity = 3

        if self.falling or self.jumping:
            self.onGround = False

        if self.xvelocity != 0 or self.jumping or self.falling:
            self.moving = True
        else: self.moving = False

        if self.moving:
            self.idle = False
        if not self.moving:
            self.idle = True

    def check_for_collision(self, xvel, yvel, objects):
        if self.hit_timer.active: self.hit_timer.update()
        if self.hit_timer.update(): self.hit_timer.deactivate()
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
        pass


class Loading_animated(Base):
    def __init__(self):
        Base.__init__(self)
        self.frames = self.get_frames('img/trans/loading.png',200,96,200,32)
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.anim_duration = 10
        self.anim_counter = 0
        self.current_frame = 0

    def animate(self):
        if self.anim_counter < self.anim_duration:
            self.anim_counter += 1
        if self.anim_counter == self.anim_duration:
            self.current_frame += 1
            self.anim_counter = 0
        if self.current_frame >= len(self.frames):
            self.current_frame = 0
        self.image = self.frames[self.current_frame]

    def update(self):
        #print 'count:', self.anim_counter
        #print 'current', self.current_frame
        self.animate()





