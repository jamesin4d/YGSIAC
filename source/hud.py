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
        self.box.blit(self.player.knife_attack.image, (8,13))

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


    def update(self):
        self.display_ammo()
        self.display_health_bar()
        self.display_viewer()
