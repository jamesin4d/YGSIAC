# Created by a human
# when:
#8/16/2015
#1:47 PM
from game_states import *

#-------------------------------------------------------------------------------------------------------
#Player class *NOW WITH COMMENTS!*
#--------------------------------------------------------------------------------------------------------
class Player(pygame.sprite.Sprite):
# used for determining which image is shown for animation
    dir = None
    dead = False
    canShoot = False
        #sets the player's health too 100%
    hp = 100
    max_hp = 100.0
    med = 20

    equipment = {
        'head': None,
        'body': None,
        'tool': None,
        'weapon': PeaShoot(),
        'feet': None
    }
    head = equipment['head']
    body = equipment['body']
    tool = equipment['tool']
    weapon = equipment['weapon']
    feet = equipment['feet']
    damage = weapon.damage
#empty lists to hold the walking frames pulled from the spritesheet
    WFL = []
    WFR = []
    WFD = []
    WFU = []
    def __init__(self):
        print self.damage
        if self.equipment['weapon'] != None:
            self.canShoot = True
        pygame.sprite.Sprite.__init__(self)
        self.set_yoself()

    def set_yoself(self):
        sprite_sheet = ('img/hero.png')
        s = SpriteSheet(sprite_sheet)
#--------walking right images
        image = s.get_image(0, 32, 32, 32)
        self.WFL.append(image)
        image = s.get_image(32, 32, 32, 32)
        self.WFL.append(image)
        image = s.get_image(64, 32, 32, 32)
        self.WFL.append(image)
#---------walking left images
        image = s.get_image(0, 64, 32, 32)
        self.WFR.append(image)
        image = s.get_image(32, 64, 32, 32)
        self.WFR.append(image)
        image = s.get_image(64, 64, 32, 32)
        self.WFR.append(image)
#-------walking down images
        image = s.get_image(0, 0, 32, 32)
        self.WFD.append(image)
        image = s.get_image(32, 0, 32, 32)
        self.WFD.append(image)
        image = s.get_image(64, 0, 32, 32)
        self.WFD.append(image)
#-------walking up images
        image = s.get_image(0, 96, 32, 32)
        self.WFU.append(image)
        image = s.get_image(32, 96, 32, 32)
        self.WFU.append(image)
        image = s.get_image(64, 96, 32, 32)
        self.WFU.append(image)
#---------sets start image and gets_rect
        self.image = self.WFD[0]
# the player maintains a 32,32 rect, the ground tiles get a 32,16 rect so that the
# player sinks into things a bit
        self.rect = pygame.Rect(32, 32, 32, 22)
        self.xvel = 0
        self.yvel = 0
#makes an instance of the Bar class from the widgets.py
        self.hp_bar = Bar()
#sets the health bar position (x, y)
        self.hp_bar.set_pos((10, 32))
#feeds the update method of Bar() the players hp
        self.health_text = Line_of_text(": health :", (125,125,125))
        self.health_text.set_pos((16, 12))
        self.angle = self.mouse_angle(pygame.mouse.get_pos())

    #TODO fix the hud that doesn't update
    def hud_draw(self):
        pass


    def add_health(self, amount):
        self.hp += amount
        if self.hp > self.max_hp:
            self.hp = self.max_hp
        if self.hp <= 0:
            self.dead = True

    def mouse_angle(self, mouse):
        off = (mouse[1]-self.rect.centery, mouse[0]-self.rect.centerx)
        self.angle = 135-math.degrees(math.atan2(*off))

    def set_position(self, x, y):
        self.rect.x += x
        self.rect.y += y

    def get_position(self):
        return self.rect.topleft
# this method takes from the health the damage given

    def get_hit(self, damage):
        self.hp -= damage
        if self.hp < 1:
            self.kill()
            self.dead = True

    def hit(self, what):
        damage = self.damage
        what.hp -= damage


#using separate speed methods for either vector
    def speedX(self, x):
        self.xvel = x
    def speedY(self, y):
        self.yvel = y
#the update method checks if the player is:
    def update(self):
        # walking left?
        if self.dir == "left":
            frame = (self.rect.x // 20) % len(self.WFL)
            self.image = self.WFL[frame]
        # walking right?
        elif self.dir == "right":
            frame = (self.rect.x // 20) % len(self.WFR)
            self.image = self.WFR[frame]
        elif self.dir == "up":
            frame = (self.rect.y // 20) % len (self.WFU)
            self.image = self.WFU[frame]
        elif self.dir == "down":
            frame = (self.rect.y // 20) % len (self.WFD)
            self.image = self.WFD[frame]
        # not walking at all?
        else:
            self.image = self.WFD[0]