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
        'weapon' : Peashooter,
        'feet' : None
    }
    head = equipment['head']
    body = equipment['body']
    weapon = equipment['weapon']
    feet = equipment['feet']
    munitions = weapon.clip_size
    action = False
    movement_rate = 4

    def __init__(self, x,y):
        Base.__init__(self)
        self.get_frames('img/hero.png')
        self.angle = self.mouse_angle(pygame.mouse.get_pos())
        if self.weapon is not None:
            self.canShoot = True
            self.damage = self.weapon.damage
        self.rect = pygame.Rect(x,y, 24,24)


    def mouse_angle(self, mouse):
        off = (mouse[1] - self.rect.centery, mouse[0] - self.rect.centerx)
        self.angle = 135 - math.degrees(math.atan2(*off))
        return self.angle

    def check_collisions(self, objects):
        self.rect.x += self.xvelocity
        for obj in objects:
            if pygame.sprite.collide_rect(self, obj):
                if isinstance(obj, EnemyBullet):
                    self.take_damage(2)
                    print self.health
                if isinstance(obj, Enemy):
                    self.take_damage(1)
                    print self.health
                if isinstance(obj, Sign):
                    if self.action:
                        pass
                if self.xvelocity < 0:
                    self.rect.left = obj.rect.right
                if self.xvelocity > 0:
                    self.rect.right = obj.rect.left
        self.rect.y += self.yvelocity
        for obj in objects:
            if pygame.sprite.collide_rect(self, obj):
                if isinstance(obj, EnemyBullet):
                    self.take_damage(2)
                    print self.health
                if isinstance(obj, Enemy):
                    self.take_damage(1)
                    print self.health
                if isinstance(obj, Sign):
                    if self.action:
                        pass
                if self.yvelocity < 0:
                    self.rect.top = obj.rect.bottom
                if self.yvelocity > 0:
                    self.rect.bottom = obj.rect.top


    def reload(self):
        self.munitions = self.weapon.clip_size
        self.canShoot = True

    def update(self):
        if self.munitions > 0:
            self.canShoot = True
        elif self.munitions <= 0:
            self.canShoot = False
            print "press R to reload"
        self.animate()
