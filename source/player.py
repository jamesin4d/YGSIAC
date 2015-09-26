# Created by a human
# when:
#8/22/2015
#6:20 AM
#
#
#--------------------------------------------------------------------
from items import *
from weapons import *
from enemies import *

class Player(Base):
    health = 9
    max_health = 9.0
    med = 2
    equipment = {
        'head' : None,
        'body' : None,
        'weapon' : Rock,
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
    walk_speed = 5
    jump_speed = 11
    gravity = 1.5
    direction = 'right'
    melee_damage = .5
    throwing = False
    def __init__(self):
        Base.__init__(self)
        self.get_frames('img/player/heroLeft.png', 'img/player/heroRight.png','img/player/jumpLeft.png','img/player/jumpRight.png',
                        'img/player/punchLeft.png','img/player/punchRight.png','img/player/idleLeft.png','img/player/idleRight.png')
        if self.weapon is not None:
            self.canShoot = True
            self.damage = self.weapon.damage
        self.rect = pygame.Rect(0,0,16,16)

    def check_ammo(self):
        if self.weapon is not None:
            if self.munitions > 0:
                self.canShoot = True
            elif self.munitions <= 0:
                self.canShoot = False

    def reload(self):
        if self.weapon is not None:
            self.munitions = self.weapon.clip_size
            self.canShoot = True


    def attack(self, attack_type, key_released):
        if not key_released:
            self.action_timer = 0
            self.attack_released = False
            self.attacking = True
            self.idle = False
            if attack_type == 'melee': self.melee = True
            if attack_type == 'throwing': self.throwing = True
        if key_released:
            self.attack_released = True
            self.attacking = True
            self.idle = False



    def update(self, objects):
        self.animate()
        self.move_and_check(objects)
        self.check_ammo()
