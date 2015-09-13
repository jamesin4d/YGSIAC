# Created by a human
# when:
#8/22/2015
#6:20 AM
#
#
#--------------------------------------------------------------------
from entities import *
from items import *
from enemies import *

class Player(Base):
    health = 100
    max_health = 100.0
    med = 20
    equipment = {
        'head' : None,
        'body' : None,
        'weapon' : None,
        'feet' : None
    }
    head = equipment['head']
    body = equipment['body']
    weapon = equipment['weapon']
    feet = equipment['feet']
    if weapon is not None:
        munitions = weapon.clip_size
    if weapon is None:
        munitions = 0
    action = False
    onGround = False
    canJump = False
    walk_speed = 6
    jump_speed = 7.5
    gravity = 0.7
    def __init__(self):
        Base.__init__(self)
        self.get_frames('img/heroguy.png')
        self.angle = self.mouse_angle(pygame.mouse.get_pos())
        if self.weapon is not None:
            self.canShoot = True
            self.damage = self.weapon.damage
        self.rect = pygame.Rect(0,0,16,20)
        self.reload_line = Line_of_text('reload',(255,255,255))

    def mouse_angle(self, mouse):
        off = (mouse[1] - self.rect.centery, mouse[0] - self.rect.centerx)
        self.angle = 135 - math.degrees(math.atan2(*off))
        return self.angle

    def check_collisions(self, objects):
        self.onGround = False
        self.rect.x += self.xvelocity
        for obj in objects:
            if pygame.sprite.collide_rect(self, obj):
                if self.direction == "left" or self.xvelocity < 0:
                    self.rect.left = obj.rect.right
                if self.direction == "right" or self.xvelocity > 0:
                    self.rect.right = obj.rect.left
        self.rect.y += self.yvelocity
        for obj in objects:
            if pygame.sprite.collide_rect(self, obj):
                if self.yvelocity < 0:
                    self.rect.top = obj.rect.bottom
                if self.yvelocity > 0:
                    self.rect.bottom = obj.rect.top
                    self.onGround = True



    def check_ammo(self):
        if self.weapon is not None:
            if self.munitions > 0:
                self.canShoot = True
            elif self.munitions <= 0:
                self.canShoot = False
                self.reload_line.set_pos(self.rect.midright)
                self.reload_line.update()


    def reload(self):
        if self.weapon is not None:
            self.munitions = self.weapon.clip_size
            self.canShoot = True

    def update(self, objects):
        self.animate()
        self.check_collisions(objects)
        self.check_self()
        self.check_ammo()
