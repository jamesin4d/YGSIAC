# Created by a human
# when:
#8/22/2015
#6:20 AM
#
#
#--------------------------------------------------------------------
from weapons import *
from enemies import *
import json

def jdefault(obj):
    return obj.__dict__

class Save(object):
    def __init__(self, health, location, ammo):
        self.health = health
        self.current_location = location
        self.ammunition = ammo

    def load_progress(self, player):
        save_file = open('player.json').read()
        opened_save = json.loads(save_file)
        if 'ammunition' in opened_save:
            ammo = opened_save['ammunition']
            self.ammunition = ammo
        if 'health' in opened_save:
            health = opened_save['health']
            self.health = health
        if 'current_location' in opened_save:
            current_location = opened_save['current_location']
            player.set_position((current_location[0], current_location[1]))

    def save_progress(self):
        with open('player.json','w') as outfile:
            json.dump(self, default=jdefault, fp=outfile,indent=4)





class Player(Base):
    health = 9
    max_health = 9.0
    med = 2
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
    ammo = None
    action = False

    walking_frames_left = [] # lists to hold walking frames
    walking_frames_right = [] # pulled from a spritesheet
    jump_frames_right = []  #jump frames
    jump_frames_left = []
    punch_frames_left = [] # punching frames
    punch_frames_right = []
    idle_frames_left = [] # standing still frames
    idle_frames_right = []
    walk_speed = 10.0
    jump_speed = 20.0
    gravity = 2.0
    direction = 'right'
    melee_damage = .5
    save = None
    melee = False
    throwing = False
    def __init__(self):
        Base.__init__(self)
        self.walking_frames_left = self.get_frames('img/player/heroLeft.png',384,80,64,80)
        self.walking_frames_right = self.get_frames('img/player/heroRight.png',384,80,64,80)
        self.jump_frames_left = self.get_frames('img/player/jumpLeft.png',192,80,64,80)
        self.jump_frames_right = self.get_frames('img/player/jumpRight.png',192,80,64,80)
        self.idle_frames_left = self.get_frames('img/player/idleLeft.png',192,80,64,80)
        self.idle_frames_right = self.get_frames('img/player/idleRight.png',192,80,64,80)
        self.punch_frames_left = self.get_frames('img/player/punchLeft.png',192,80,64,80)
        self.punch_frames_right = self.get_frames('img/player/punchRight.png',192,80,64,80)
        self.image = self.walking_frames_right[0]
        self.rect = pygame.Rect(0,0,64,80)

        if self.weapon is not None:
            self.canShoot = True
            self.damage = self.weapon.damage



    def check_ammo(self):
        if self.weapon is not None:
            if self.ammo > 0:
                self.canShoot = True
            elif self.ammo <= 0:
                self.canShoot = False

    def reload(self):
        if self.weapon is not None:
            self.ammo = self.weapon.clip_size
            self.canShoot = True

    def attack(self, attack_type, key_released):
        if not key_released:
            self.attack_released = False
            self.attacking = True
            self.idle = False
            if attack_type == 'melee': self.melee = True
            if attack_type == 'throwing': self.throwing = True
        if key_released:
            self.attack_released = True
            self.attacking = True
            self.idle = False


    def animate(self):
        if self.attacking:
            if not self.attack_released:
                self.action_timer = 0
                if self.direction == 'left':
                    self.image = self.punch_frames_left[2]
                elif self.direction == 'right':
                    self.image = self.punch_frames_right[0]
            if self.attack_released:
                self.action_timer += 1
                if self.action_timer == 2:
                    if self.direction == 'left':
                        self.rect.x -= 2
                        self.image = self.punch_frames_left[0]
                    elif self.direction == 'right':
                        self.rect.x += 2
                        self.image = self.punch_frames_right[1]
                if self.action_timer == 3:
                    if self.direction == 'left':
                        self.rect.x -= 4
                        self.image = self.punch_frames_left[1]
                    if self.direction == 'right':
                        self.rect.x += 4
                        self.image = self.punch_frames_right[2]
                if self.action_timer == 6:
                    if self.melee: self.melee = False
                    if self.throwing: self.throwing = False
                    self.attacking = False
                    self.idle = True

        if self.moving:
            if self.direction == "left":
                frame = (self.rect.x//29) % len(self.walking_frames_left)
                self.image = self.walking_frames_left[frame]
            elif self.direction == "right":
                frame = (self.rect.x//29) % len(self.walking_frames_right)
                self.image = self.walking_frames_right[frame]

        if self.jumping:
            if self.direction == "left":
                self.image = self.jump_frames_left[2]
            elif self.direction == "right":
                self.image = self.jump_frames_right[0]

        if self.falling:
            if not self.attacking:
                if self.direction == "left":
                    self.image = self.jump_frames_left[1]
                elif self.direction == "right":
                    self.image = self.jump_frames_right[1]

        if self.idle and not self.attacking:
            self.action_timer += .5
            if self.action_timer == 20:
                self.action_timer = 0
            if self.direction == "right":
                if self.action_timer > 0:
                    self.image = self.idle_frames_right[0]
                if self.action_timer > 6:
                    self.image = self.idle_frames_right[1]
                if self.action_timer > 12:
                    self.image = self.idle_frames_right[2]
            elif self.direction == "left":
                if self.action_timer > 0:
                    self.image = self.idle_frames_left[0]
                if self.action_timer > 6:
                    self.image = self.idle_frames_left[1]
                if self.action_timer > 12:
                    self.image = self.idle_frames_left[2]


    def update(self, objects):
        self.animate()
        self.move_and_check(objects)
        self.check_ammo()
