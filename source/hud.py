# Created by a human
# when:
#9/20/2015
#7:30 PM
#
#
#--------------------------------------------------------------------
from gooey import *
from utilities import *

class HUD(object):
    def __init__(self, player):
        self.player = player
        self.healthBarImage = 'img/HUD/health_bar.png'
        self.screen = pygame.display.get_surface()
        self.various = SpriteSheet.strip_sheet('img/HUD/var.png',96,32,32,32)
        self.canvas = pygame.image.load('img/HUD/Canvas.png')
        self.box = pygame.image.load('img/HUD/Box.png')
        self.box.set_colorkey((255,255,255))
        self.score = Score('Score')

    def draw_hud_canvas(self):
        pos = [0,0]
        self.screen.blit(self.canvas, pos)

    def display_ammo(self):
        #ammo = self.player.munitions
        x = self.player.rect.x
        y = self.player.rect.y-10
        #display_info(self.screen, "Ammunition: " + str(ammo),20,144,6)
        #if ammo <= 0:
         #   display_info(self.screen, "press 'R' ", 12, x,y)

    def display_viewer(self):
        pos = [110,0]
        self.screen.blit(self.box, pos)
        #self.box.blit(self.player.weapon.image, (16,16))

    def display_health_bar(self):
        health = self.player.health
        heart_one_Position = [6,0]
        heart_two_Position = [40,0]
        heart_three_Position = [74,0]
        if health == 9:
            self.screen.blit(self.various[1],heart_one_Position)
            self.screen.blit(self.various[1],heart_two_Position)
            self.screen.blit(self.various[1],heart_three_Position)
        if health == 6:
            self.screen.blit(self.various[1],heart_one_Position)
            self.screen.blit(self.various[1],heart_two_Position)
        if health == 3:
            self.screen.blit(self.various[1],heart_one_Position)


    def show_debug(self):
        p = self.player
        print_info(self.screen, "-Left & Right arrows adjust walk speed, Up & down adjust jump-",10, 0)
        print_info(self.screen,"Player y-velocity: " + str(p.yvelocity),10,1)
        print_info(self.screen,"Player x-velocity: " + str(p.xvelocity),10,2)
        print_info(self.screen,"Player on the ground: " + str(p.onGround),10,3)
        print_info(self.screen,"Player walk speed: " + str(p.walk_speed),10,4)
        print_info(self.screen,"Player jump speed: " + str(p.jump_speed),10,5)
        print_info(self.screen,"Gravity: " + str(p.gravity),10,6)
        print_info(self.screen,"'G' raises gravity, 'F' lowers it",10,7)
        print_info(self.screen,"Collide Left: " + str(p.collide_left),10,8)
        print_info(self.screen,"Collide Right: " + str(p.collide_right),10,9)
        print_info(self.screen,"Collide Top: " + str(p.collide_top),10,10)
        print_info(self.screen,"Collide bottom: " + str(p.collide_bottom),10,11)
        print_info(self.screen,"Player melee: " + str(p.melee),10,12)


    def update(self):
        self.display_ammo()
        self.display_health_bar()
        self.display_viewer()
