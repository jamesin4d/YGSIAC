# Created by a human
# when:
#9/20/2015
#6:50 AM
#
#
#--------------------------------------------------------------------
from utilities import *
from entities import Entity
import math


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


