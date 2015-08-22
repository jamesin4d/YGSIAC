# Created by a human
# when:
#8/22/2015
#6:20 AM
#
#
#--------------------------------------------------------------------
from entities import *
from items import *

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

    def __init__(self):
        Base.__init__(self)
        self.get_frames('img/hero.png')
        self.angle = self.mouse_angle(pygame.mouse.get_pos())
        if self.weapon is not None:
            self.canShoot = True
            self.damage = self.weapon.damage


    def mouse_angle(self, mouse):
        off = (mouse[1] - self.rect.centery, mouse[0] - self. rect.centerx)
        self.angle = 135 - math.degrees(math.atan2(*off))


    def check_collisions(self, objects):
        self.rect.x += self.xvelocity
        for obj in objects:
            if pygame.sprite.collide_rect(self, obj):
                if self.xvelocity < 0:
                    self.rect.left = obj.rect.right
                if self.xvelocity > 0:
                    self.rect.right = obj.rect.left
        self.rect.y += self.yvelocity
        for obj in objects:
            if pygame.sprite.collide_rect(self, obj):
                if self.yvelocity < 0:
                    self.rect.top = obj.rect.bottom
                if self.yvelocity > 0:
                    self.rect.bottom = obj.rect.top

    def update(self):
        if self.direction == 'left':
            frame = (self.rect.x//20) % len(self.walking_frames_left)
            self.image = self.walking_frames_left[frame]
        elif self.direction == 'right':
            frame = (self.rect.x//20) % len(self.walking_frames_right)
            self.image = self.walking_frames_right[frame]
        elif self.direction == 'up':
            frame = (self.rect.y//20) % len(self.walking_frames_up)
            self.image = self.walking_frames_up[frame]
        elif self.direction == 'down':
            frame = (self.rect.y//20) % len(self.walking_frames_down)
            self.image = self.walking_frames_down[frame]