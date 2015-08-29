# Created by a human
# when:
#8/22/2015
#6:19 AM
#
#
#--------------------------------------------------------------------
from entities import *
from utilities import Timer

# ---------------------------------------------------------------------------------------------------
# so the idea here is: subclass the Base class so that we have an
# Enemy type, then use the Enemy class as a parent to the different types
# of enemy. the parent enemy class will have a 'behavioural tree' of methods
# for the child class to inherit from, deciding what to do based on state
# ------------------------------------------------------------------------
class Enemy(Base):

    def __init__(self):
        Base.__init__(self)
        self.target = None
        self.barriers = None
        self.dx = ()
        self.dy = ()
        self.target_in_range = False

    def distance_to_target(self):
        target_position = self.target.get_position()
        position = self.get_position()
        tp = target_position
        sp = position
        # dx = target.x - self.x
        dx = tp[0] - sp[0]
        # dy = target.y - self.y
        dy = tp[1] - sp[1]
        self.dx = dx
        self.dy = dy
        if dx > 150 or dx < -150:
            self.target_in_range = False
        if dy > 150 or dy < -150:
            self.target_in_range = False
        else:
            self.target_in_range = True

    def check_collisions(self, objects):
        self.rect.x += self.xvelocity
        for o in objects:
            if pygame.sprite.collide_rect(self, o):
                if isinstance(o, Solid):
                    if self.xvelocity < 0:
                        self.rect.left = o.rect.right
                    if self.xvelocity > 0:
                        self.rect.right = o.rect.left
        self.rect.y += self.yvelocity
        for o in objects:
            if pygame.sprite.collide_rect(self, o):
                if isinstance(o, Solid):
                    if self.yvelocity < 0:
                        self.rect.top = o.rect.bottom
                    if self.yvelocity > 0:
                        self.rect.bottom = o.rect.top

    def pursue_target(self):
# oooh. thats good. I love when you figure something out
# and it just looks so simple and elegant
# the if - or - statement here is the key!!
# if only you knew how long I struggled to figure out
# just the right way to word this script to fix the
# issue I was having! but it seems to follow the target well.
# call this method when player is in radius
# or after the enemy has been provoked. or really any time
# I don't give a shit, it checks if EITHER vector is not equal to 0
# so if dx = 0 and dy isnt, only the dy instructions pass, and vice-versa
# so the enemy no longer walks like an asshole. note it checks the x-axis first
# you can kind of see how this effects behavior in game.
        self.distance_to_target()
        if self.target_in_range:
            dx = self.dx
            dy = self.dy
            if dx != 0 or dy != 0:
                if dx < -1:
                    self.move(-2,0)
                if dx > 1:
                    self.move(2,0)
                if dy < -1:
                    self.move(0,-2)
                if dy > 1:
                    self.move(0,2)


    def flee_target(self):
        self.distance_to_target()
        if self.target_in_range:
            dx = self.dx
            dy = self.dy
            if dx != 0 or dy != 0:
                if dx < -1:
                    self.move(2,0)
                if dx > 1:
                    self.move(-2,0)
                if dy < -1:
                    self.move(0,2)
                if dy > 1:
                    self.move(0,-2)

    def flee_directly(self):
        self.distance_to_target()
        if self.target_in_range:
            if self.dx != 0:
                if self.dx < -10:
                    self.move_x(2)
                elif self.dx > 10:
                    self.move_x(-2)
            if self.dy != 0:
                if self.dy < -10:
                    self.move_y(2)
                elif self.dy > 10:
                    self.move_y(-2)

class Security(Enemy):
    def __init__(self):
        self.get_frames('img/security.png')
        Enemy.__init__(self)
        self.health = random.randint(5,10)
        self.max_health = 12.0

    def update(self):
        if self.health > 5:
            self.pursue_target()
        else:
            random.choice((self.flee_target(),self.flee_directly()))
        self.animate()

class Blob(Enemy):
    def __init__(self):
        self.get_frames('img/finnyblub.png')
        Enemy.__init__(self)
        self.health = 10
        self.max_health = 10

    def update(self):
        self.animate()




