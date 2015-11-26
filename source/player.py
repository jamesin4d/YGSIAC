# Created by a human
# when:
#8/22/2015
#6:20 AM
#
#
#--------------------------------------------------------------------
from weapons import *
from enemies import *
from bot_buddy import Nimbot

class Inventory(object):
    def __init__(self):
        self.slots = {}

    def gain(self, key, value):
        self.slots[key] = value




class Player(Base):
    health = 9
    max_health = 9.0
    action = False

    walking_frames_left = [] # lists to hold walking frames
    walking_frames_right = [] # pulled from a spritesheet
    jump_frames_right = []  #jump frames
    jump_frames_left = []
    punch_frames_left = [] # punching frames
    punch_frames_right = []
    idle_frames_left = [] # standing still frames
    idle_frames_right = []

    walk_speed = 15.0
    jump_speed = 22.0
    gravity = 2.0
    direction = 'right'
    save = None
    score = 0

    def __init__(self):
        Base.__init__(self)
        self.gather_frame_sets()
        self.image = self.walking_frames_right[0]
        self.rect = pygame.Rect(0,0,32,32)
        self.friend = Nimbot()
        self.friend.set_position(self.rect.topleft)
        self.knife_attack = Knife()
        jumpSound = 'sounds/jump.wav'
        self.jumpSound = pygame.mixer.Sound(jumpSound)




    def gather_frame_sets(self):
        self.walking_frames_left = self.get_frames('img/player/greyL.png',192,32,32,32)
        self.walking_frames_right = self.get_frames('img/player/greyR.png',192,32,32,32)
        # strips the jumping frames
        jump_frames = self.get_frames('img/player/greyJump.png',192,32,32,32)
        self.jump_frames_left = (jump_frames[0],jump_frames[1],jump_frames[2])
        self.jump_frames_right = (jump_frames[3],jump_frames[4],jump_frames[5])
        # it stripes the attack frames
        punch_frames = self.get_frames('img/player/greyPunch.png',192,32,32,32)
        self.punch_frames_left = (punch_frames[0],punch_frames[1],punch_frames[2])
        self.punch_frames_right = (punch_frames[3],punch_frames[4],punch_frames[5])
        # grab all the idles frames froms thes sheets
        idle_frames = self.get_frames('img/player/greyIdle.png',256,32,32,32)
        self.idle_frames_left = (idle_frames[0],idle_frames[1],idle_frames[2],idle_frames[3])
        self.idle_frames_right = (idle_frames[4],idle_frames[5],idle_frames[6],idle_frames[7])


    def attack(self, key_released):

        if not key_released:
            self.attack_released = False
            self.attacking = True
            self.idle = False
        if key_released:
            self.attack_released = True
            self.attacking = True
            self.idle = False

            if self.direction == 'left':
                self.knife_attack.set_position(self.rect.midleft)
                self.knife_attack.direction = 1
                self.knife_attack.finished = False
            if self.direction == 'right':
                self.knife_attack.set_position(self.rect.midright)
                self.knife_attack.direction = 0
                self.knife_attack.finished = False


    def animate(self):
        if self.attacking:
            #while the attack key is held, display this frame
            if not self.attack_released:
                self.action_timer = 0
                if self.direction == 'left':
                    self.image = self.punch_frames_left[2]
                elif self.direction == 'right':
                    self.image = self.punch_frames_right[0]
            # when the key is released, animate, mate.
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

                    self.attacking = False
                    self.idle = True

        if self.moving:
            if self.direction == "left":
                frame = (self.rect.x//50) % len(self.walking_frames_left)
                self.image = self.walking_frames_left[frame]
            elif self.direction == "right":
                frame = (self.rect.x//50) % len(self.walking_frames_right)
                self.image = self.walking_frames_right[frame]

        if self.jumping:

            if self.direction == "left":
                self.image = self.jump_frames_left[2]
            if self.direction == "right":
                self.image = self.jump_frames_right[0]

        if self.falling:
            if not self.attacking:
                if self.direction == "left":
                    self.image = self.jump_frames_left[1]
                if self.direction == "right":
                    self.image = self.jump_frames_right[1]

# for the record I've found a better method of animating since coding this, but I ain't
# changing it, I don't got time for that, i'm a busy man.
        if self.idle and not self.attacking:
            self.action_timer += 1
            if self.action_timer == 20:
                self.action_timer = 0
            if self.direction == "right":
                if self.action_timer > 0:
                    self.image = self.idle_frames_right[0]
                if self.action_timer > 6:
                    self.image = self.idle_frames_right[1]
                if self.action_timer > 12:
                    self.image = self.idle_frames_right[2]
            if self.direction == "left":
                if self.action_timer > 0:
                    self.image = self.idle_frames_left[0]
                if self.action_timer > 6:
                    self.image = self.idle_frames_left[1]
                if self.action_timer > 12:
                    self.image = self.idle_frames_left[2]


    def update(self, objects):
        self.animate()
        self.move_and_check(objects)
        tl = self.rect.topleft
        x = tl[0]
        y = tl[1] - 32
        self.friend.set_position((x,y))
        self.friend.update()
        self.knife_attack.update(objects)