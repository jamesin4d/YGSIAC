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


class Energy(Entity):
    def __init__(self, position):
        Entity.__init__(self)
        self.frames = SpriteSheet.strip_sheet('img/entities/dropitems/pickup.png',128,16,16,16)
        self.image = self.frames[0]
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect(center=position)
        self.anim_timer = 0


    def update(self):
        self.anim_timer += 0.5
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



# --------------------------------------------------------------------
# A simple unidirectional bullet class, the 'owner' is whoever shot the bullet
# ---------------------------------------------------------------------
class Bullets(Entity):
    direction = None
    speed = 0
    gravity = 0
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

    def check_collisions(self, solids, entities):
        self.rect.y += self.gravity
        self.rect.x += self.speed
        for s in solids:
            if pygame.sprite.collide_rect(self, s):
                self.kill()
        for e in entities:
            if pygame.sprite.collide_rect(self, e):
                e.take_damage(self.owner.damage)
                self.kill()

    def check_direction(self):
        if self.direction == 'right':
            self.speed = 10
        elif self.direction == 'left':
            self.speed = -10

    def update(self, solids, entities):
        self.gravity += .1
        self.check_collisions(solids, entities)

#-----------------------------------------------------------------
# A more complex Bullet class with an angle, used for shooting with the mouse
#-----------------------------------------------------------------
class ComplexBullet(Entity):
    def __init__(self, loc, angle):
        Entity.__init__(self)
        self.frames = SpriteSheet.strip_sheet('img/bullet.png',24,4,4,4)
        self.original_image = self.frames[0]
        self.angle = -math.radians(angle-136)
        self.image = pygame.transform.rotate(self.original_image, angle-136)
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect(center=loc)
        self.move = [self.rect.x, self.rect.y]
        self.speed_mod = 10
        self.speed = (self.speed_mod*math.cos(self.angle),
                      self.speed_mod*math.sin(self.angle))

    def check_collisions(self, solids, entities):
        for s in solids:
            if pygame.sprite.collide_rect(self, s):
                self.kill()
        for e in entities:
            if pygame.sprite.collide_rect(self, e):
                self.kill()

# a brief explainer on the animation method here
    def animate(self):
        # if the x-axis has speed applied to it
        if self.speed[0] != 0 or self.speed[1] != 0:
            # essentially:
            # frame = the currently displayed frame
            #  (x // y)- returns (floored) quotient of x and y
            # the ' % ' is called a modulus, it returns the remainder of something.
            # so what this line does is as the x-axis moves, itterate over the length(self.frames) I think
            frame = (self.rect.centerx//40) % len(self.frames) # how this equation actually works is something of a black box for me.
            #this is just one of those things that wasn't clearly explained wherever I learned it from, but works so I don't ask any questions.
            # https://docs.python.org/2/library/stdtypes.html <-- head there for *some* further help.
            self.image = pygame.transform.rotate(self.frames[frame], self.angle)

    def update(self, solids, entities):
        self.check_collisions(solids, entities)
        self.move[0] += self.speed[0]
        self.move[1] += self.speed[1]
        self.rect.topleft = self.move
        self.animate()

    def remove(self, screen_rect):
        if not self.rect.colliderect(screen_rect):
            self.kill()
