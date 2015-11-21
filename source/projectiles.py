# Created by a human
# when:
#9/20/2015
#6:50 AM
#
#
#--------------------------------------------------------------------

from entities import *
import math


class Swing(Base):
    def __init__(self):
        Base.__init__(self)
        self.right_frames = self.get_frames('img/player/swing.png', 80, 16, 16, 16)
        self.left_frames = self.get_frames('img/player/swingL.png', 80, 16, 16, 16)
        self.image = self.right_frames[0]
        self.rect = self.image.get_rect()
        self.anim_duration = 7
        self.anim_counter = 0
        self.current_frame = 0
        self.direction =  0
        #------ programming tangent -----------------------------------------
        # experimenting with using 0, and 1 as 'placeholder' boolean values,
        # in situations where true/false isn't relative, and hurts the understandability of code.
        # direction = false/true - built in language boolean tool, probably computed pretty quickly
        # BUT -- it doesn't make any DAMN sense in human language.
        # direction = "left"/"right" - more readable, but i'd imagine string comparisons take a little
        # more time to compute. ---- So the reasoning here is that the machine-friendly number is
        # human-friendly enough when used carefully, a cool language feature would be to be able
        # to string together normally incompatible value types like so;---------------------
        # direction = 0 = 'left'
        # but i think thats about the same as having a direction dictionary key/value relationship
        # to itterate the data.
        # i'm sure it doesn't really matter when making a 2d not-so-resource-hungry game.

    def animate(self):
        if self.anim_counter < self.anim_duration:
            self.anim_counter += 1
        if self.anim_counter == self.anim_duration:
            self.current_frame += 1
            self.anim_counter = 0
        if self.current_frame >= len(self.right_frames):
            self.current_frame = 0

        self.image = self.right_frames[self.current_frame]

    def update(self):
        self.animate()


class PickUp(Entity):
    def __init__(self, position):
        Entity.__init__(self)
        self.frames = SpriteSheet.strip_sheet('img/entities/dropitems/pickup.png',128,16,16,16)
        self.image = self.frames[0]
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect(center=position)
        self.anim_timer = 0
        self.inactive = False

    def check_collisions(self, obj):
        col = pygame.sprite.collide_rect(self, obj)
        if col:
            self.inactive = True


    def animate(self):
        self.anim_timer += 1
        if self.anim_timer > 0:
            self.image = self.frames[0]
        if self.anim_timer > 5:
            self.image = self.frames[1]
        if self.anim_timer > 10:
            self.image = self.frames[2]
        if self.anim_timer > 15:
            self.image = self.frames[3]
        if self.anim_timer > 20:
            self.image = self.frames[4]
        if self.anim_timer > 25:
            self.image = self.frames[5]
        if self.anim_timer > 30:
            self.anim_timer = 0


    def update(self):
        self.animate()



# --------------------------------------------------------------------
# A simple unidirectional bullet class, the 'owner' is whoever shot the bullet
# ---------------------------------------------------------------------
class Bullets(Entity):
    direction = None
    speed = 0
    gravity = 0
    dead = False
    def __init__(self, position, shooter):
        Entity.__init__(self)
        self.frames = SpriteSheet.strip_sheet('img/player/shot.png',16,4,4,4)
        self.image = self.frames[0]
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect(center=position)
        self.owner = shooter
        self.direction = self.owner.direction
        self.count = 0
        self.check_direction()

    def remove(self, screen_rect):
        if not self.rect.colliderect(screen_rect):
            self.kill()

    def check_collisions(self, solids):
        self.rect.y += self.gravity
        self.rect.x += self.speed
        for s in solids:
            if pygame.sprite.collide_rect(self, s):
                self.dead = True

    def check_direction(self):
        if self.direction == 'right':
            self.speed = 15
        elif self.direction == 'left':
            self.speed = -15

    def update(self, solids):
       self.check_collisions(solids)


