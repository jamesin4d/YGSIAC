# Created by a human
# when:
#9/21/2015
#5:46 AM
# please note the above time stamp
# so if my comments don't make much sense
# refer to the previous two statements
#--------------------------------------------------------------------
from entities import *

# wham Weapon class
class Weapon(Base):
    def __init__(self):
        # is a subclass of the Base class
        Base.__init__(self)
        # has the following attributes for it's own children to inherit
        self.owner = None
        self.clip_size = 0
        self.damage = 0
        self.speed = 0
    # call this method when the weapon is picked up, clear it from screen give it an owner
    def picked_up(self, owner):
        self.owner = owner


class Rock(Weapon):
    # Rock is sort of interesting.
    frames = SpriteSheet.strip_sheet_no_convert('img/player/shot.png',16,4,4,4)
    image = frames [0]
    clip_size = 3 # the amount of rocks one could feasibly carry in ones hands
    damage = 2 # how much it would hurt to be hit by aforementioned rocks.
    def __init__(self, position, shooter):
        Weapon.__init__(self)
        self.frames = SpriteSheet.strip_sheet('img/player/shot.png',16,4,4,4)
        self.image = self.frames[0]
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect(center=position) # this sets the rect.center to the position argument
        self.owner = shooter
        self.direction = self.owner.direction # this lets the rock know which way to go
        self.count = 0  # this is the count rockula.
        self.check_direction() # this method is called on __init__ cause that's the only time we need to know it
        # -----here's a section of interest ------
        self.weight = random.randint(2,5) # every rock gets a unique random integer between (a, b)
        self.gravity = random.randint(-6, -2) # the gravity begins as very slight anti-gravity

    # uninteresting crap
    def remove(self, screen_rect):
        if not self.rect.colliderect(screen_rect):
            self.kill() #killyourself

    def check_collisions(self, solids, entities):
        self.rect.y += self.gravity
        self.rect.x += self.speed
        self.onGround = False

        for s in solids:
            if pygame.sprite.collide_rect(self, s):
                if self.speed < 0:
                    self.rect.left = s.rect.right
                    self.collide_left = True
                if self.speed > 0:
                    self.rect.right = s.rect.left
                    self.collide_right = True
                if self.gravity <0:
                    self.rect.top = s.rect.bottom
                    self.collide_top = True
                if self.gravity > 0:
                    self.rect.bottom = s.rect.top
                    self.collide_bottom = True
                    self.onGround = True
        for e in entities:
            if pygame.sprite.collide_rect(self, e):
                e.take_damage(self.owner.damage)
                self.kill()
        if self.onGround:
            if self.gravity > 3:
                self.gravity = 3
        if self.collide_left:
            self.speed = 4
        if self.collide_right:
            self.speed = -4
        if self.collide_top:
            self.gravity = 2
    def check_direction(self):
        if self.direction == 'right':
            self.speed = 8
        elif self.direction == 'left':
            self.speed = -8

# --------------- LOOK --------------------------------
    def update(self, solids, entities):
        self.count += 1 # Count Rockula counts at 30 beats/sec
        if self.count >= 10: # so after a fraction of a second
            if self.gravity <= 0: # if you've got anti-grav rocks
                self.gravity = self.weight*.1 # blam! weight times desired gravity constant bitch.
            if self.count >= 10:  # to make it look more realistic, as time goes up, gravity increases
                self.gravity += .4
            if self.count >= 15:
                self.gravity += .8
                self.count = 15
            if pygame.sprite.collide_rect(self, self.owner):
                self.kill()
                self.owner.munitions += 1
        self.check_collisions(solids, entities)








