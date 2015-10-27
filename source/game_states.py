# Created by a human
# when:
# 8/22/2015
# 6:29 AM
#
#
# --------------------------------------------------------------------
from mapper import *
from engine import State
from rooms import *
from player import Player
from hud import HUD
from weapons import *
from camera import *
from gooey import *
# GAME STATES *NOW WITH COMMENTS!!*
import sys
pygame.init()


# -----------------Splash screen state---------------------------------------------------------
class Logo(State):
    def __init__(self):
        State.__init__(self)
        self.next = StartScreen()
        self.screen.fill((0,0,0))
        self.image = get_image("img/logo.png")
        self.alpha = 0
        self.image.set_alpha(0)
        self.image = pygame.transform.scale(self.image, self.screen.get_size())
        self.image_pos = center(self.image.get_size(), self.screen.get_size())
        self.fade = False
        self.lifetime = Timer(5)
        self.update_s = True

    def update_screen(self):
        if self.update_s:
#            makes sure the screen stays black
            self.screen.fill((0,0,0))
            self.screen.blit(self.image, self.image_pos)
            pygame.display.update()
    def tick(self):
        self.clock.tick(30)
# this is where the timer comes in, any value is fine
        if self.lifetime.update():
            if not self.fade:
# the real control in how long the splash screen lasts is here, in the alpha
                self.alpha += 6
                self.image.set_alpha(self.alpha)
                self.update_s = True
                if self.alpha > 255:
                    self.fade = True
            else:
                self.alpha -= 6
                self.image.set_alpha(self.alpha)
                self.update_s = True
                if self.alpha < -100:
                    self.quit()

    def check_events(self):
        for e in pygame.event.get():
            if e.type == pygame.VIDEORESIZE:
                self.image = pygame.transform.scale(self.image, (e.w, e.h))
                self.screen = pygame.display.set_mode((e.w, e.h), pygame.RESIZABLE)
            if e.type == pygame.QUIT:
                self.close_game()
# any key skips it, cause I really hate when you cant skip things
            if e.type == pygame.KEYDOWN:
                self.quit()

    def quit(self):
        State.quit(self)

# ----------------Start screen state-------------------------------------------------------------
class StartScreen(State):
    game_start = False
    options_start = False
    quit_game = False
    def __init__(self):
        State.__init__(self)
        self.kill_prev = True
        self.done = False
        self.next = Game()
        self.screen.fill((200,200,200))
        self.image = get_image('img/startscreen/startscreen.png')
        self.start = Widget((147,21),image=get_image('img/startscreen/start.png'))
        self.start.set_position((800,200))
        self.option = Widget((191,24),image=get_image('img/startscreen/option.png'))
        self.option.set_position((800,250))
        self.quitbtn = Widget((125,24),image=get_image('img/startscreen/quit.png'))
        self.quitbtn.set_position((800, 300))
        self.image = pygame.transform.scale(self.image, self.screen.get_size())
        self.image_pos = center(self.image.get_size(), self.screen.get_size())
        self.ups = True
        self.cursor = Widget((64,64), image=get_image('img/startscreen/cursor.png'))
        self.cursor_index = 1
        self.cursor_positioning_guidance_system()


# overly long description of CPGS is unnecessary
    def cursor_positioning_guidance_system(self,selected=False):
        if self.cursor_index > 3: self.cursor_index = 1
        if self.cursor_index < 1: self.cursor_index = 3
        positions = {
            'start':(736,200),
            'options':(736,250),
            'quit':(736,300)
        }
        if self.cursor_index == 1:
            self.cursor.set_position(positions['start'])
            if selected:
                self.next = Game()
                self.quit()
        if self.cursor_index == 2:
            self.cursor.set_position(positions['options'])
            if selected:
                self.next = Options()
                self.quit()
        if self.cursor_index == 3:
            self.cursor.set_position(positions['quit'])
            if selected:
                self.next = RealitySimulator()
                self.quit()

    def update_screen(self):
        if self.ups:
            self.screen.fill((200,200,200))
            self.image = pygame.transform.scale(self.image, self.screen.get_size())
            self.screen.blit(self.image, self.image_pos)
            self.cursor.draw()
            self.start.draw()
            self.option.draw()
            self.quitbtn.draw()
            pygame.display.flip()

    def check_events(self):
        self.cursor_positioning_guidance_system() # checks where cursor should be
        for e in pygame.event.get():
            if e.type == pygame.VIDEORESIZE:
                self.image = pygame.transform.scale(self.image, (e.w, e.h))
                self.screen = pygame.display.set_mode((e.w, e.h), pygame.RESIZABLE)
            if e.type == pygame.QUIT:
                self.close_game()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_DOWN or e.key == pygame.K_s:
                    self.cursor_index += 1
                if e.key == pygame.K_UP or e.key == pygame.K_w:
                    self.cursor_index -= 1
                if e.key == pygame.K_SPACE:
                    self.cursor_positioning_guidance_system(selected=True)
                if e.key == pygame.K_ESCAPE:
                    self.next = RealitySimulator()
                    self.quit()
# ---------------Options state-------------------------------------------------
class Options(State):
     def __init__(self):
        State.__init__(self)
        self.kill_prev = True
        self.done = False
        self.screen.fill((40,40,50))
        self.image = pygame.image.load('img/optionscreen/optionsscreen.png')
        self.image = pygame.transform.scale(self.image, self.screen.get_size())
        self.image_pos = center(self.image.get_size(), self.screen.get_size())
        self.ups = True

     def update_screen(self):
         if self.ups:
             self.screen.fill((40,40,50))
             self.image = pygame.transform.scale(self.image, self.screen.get_size())
             self.screen.blit(self.image, self.image_pos)
             pygame.display.flip()

     def check_events(self):
         for e in pygame.event.get():
             if e.type == pygame.VIDEORESIZE:
                self.image = pygame.transform.scale(self.image, (e.w, e.h))
                self.screen = pygame.display.set_mode((e.w, e.h), pygame.RESIZABLE)
             if e.type == pygame.QUIT:
                 self.close_game()
             if e.type == pygame.KEYDOWN:
                 self.next = StartScreen()
                 self.quit()
                 if e.key == pygame.K_ESCAPE:
                     self.next = RealitySimulator()
                     self.quit()
# --------------------now...close your eyes...----------------------------------------------------
class RealitySimulator(State):
    def __init__(self):
        State.__init__(self)
        self.next = None
        self.screen.fill((200,200,200))
        self.image = pygame.image.load("img/gamequit/quitscreen.png")
        self.alpha = 0
        self.image.set_alpha(0)
        self.image = pygame.transform.scale(self.image, self.screen.get_size())
        self.image_pos = center(self.image.get_size(), self.screen.get_size())
        self.fade = False
        self.lifetime = Timer(1)
        self.update_s = True

    def update_screen(self):
        if self.update_s:
            self.screen.fill((200,200,200))
            self.image = pygame.transform.scale(self.image, self.screen.get_size())
            self.screen.blit(self.image, self.image_pos)
            pygame.display.update()
    def tick(self):
        self.clock.tick(10)
        if self.lifetime.update():
            if not self.fade:
                self.alpha += 10
                self.image.set_alpha(self.alpha)
                self.update_s = True
                if self.alpha > 255:
                    self.fade = True
            else:
                self.alpha -= 10
                self.image.set_alpha(self.alpha)
                self.update_s = True
                if self.alpha < -100:
                    self.close_game()

    def check_events(self):
        for e in pygame.event.get():
            if e.type == pygame.VIDEORESIZE:
                self.image = pygame.transform.scale(self.image, (e.w, e.h))
                self.screen = pygame.display.set_mode((e.w, e.h), pygame.RESIZABLE)
            if e.type == pygame.QUIT:
                self.close_game()
            if e.type == pygame.KEYDOWN:
                self.quit()

    def quit(self):
        State.quit(self)
#------------------------- Game over state --------------------------------------------------------
class GameOver(State):
    def __init__(self):
        State.__init__(self)
        self.next = StartScreen()
        self.screen.fill((40,40,40))
        self.image = pygame.image.load("img/gamequit/gameover.png")
        self.image = pygame.transform.scale(self.image, self.screen.get_size())
        self.image_pos = center(self.image.get_size(), self.screen.get_size())

    def update_screen(self):
        self.screen.fill((40,40,40))
        self.image = pygame.transform.scale(self.image, self.screen.get_size())
        self.screen.blit(self.image, self.image_pos)
        pygame.display.flip()
    def check_events(self):
        for e in pygame.event.get():
            if e.type == pygame.VIDEORESIZE:
                self.image = pygame.transform.scale(self.image, (e.w, e.h))
                self.screen = pygame.display.set_mode((e.w, e.h), pygame.RESIZABLE)
            if e.type == pygame.QUIT:
                self.close_game()
            if e.type == pygame.KEYDOWN:
                self.quit()

class Pause(State):
    def __init__(self):
        State.__init__(self)
        self.kill_prev = False
#------------------------ Game state!--------------------------------------------------------------
class Game(State):
    def __init__(self):
        #blam, initiate that parent class
        State.__init__(self)
        self.kill_prev = True
        self.screen.fill((0,0,0))
        self.show_debug = False
        self.canvas = pygame.image.load('img/blankcanvas.png').convert()
        self.canvas = pygame.transform.scale(self.canvas, self.screen.get_size())
        self.canvas_pos = center(self.canvas.get_size(), self.screen.get_size())
        self.current_room = StartRoom()
        self.player = Player()
        self.player.set_position(self.current_room.player_pos_left)
        self.current_room.player = self.player
        self.heads_up_display = HUD(self.player)

# events loop, feeds the player.dir values to handle player
# animation, also handles the player jump and walk speed
    def check_events(self):
        p = self.player
        pg = pygame
        keypress = pg.KEYDOWN
        keyrelease = pg.KEYUP
        esc = pg.K_ESCAPE
        s_key = pg.K_s
        d_key = pg.K_d
        up_arrow = pg.K_UP
        left_arrow = pg.K_LEFT
        right_arrow = pg.K_RIGHT

        for e in pg.event.get():
            if e.type == pg.QUIT:
                self.close_game()
                sys.exit()
            elif e.type == keypress:
                if e.key == esc:
                    self.close_game()
                    sys.exit()
                if e.key == left_arrow:
                    p.walk_left()
                if e.key == right_arrow:
                    p.walk_right()
                if e.key == up_arrow:
                    p.jump(-p.jump_speed)
                if e.key == s_key:
                    self.current_room.item_list.append(Bullets(p.rect.center,p))
                    p.attack('throwing',False)
                if e.key == d_key:
                    p.attack('melee',False)
            elif e.type == keyrelease:
                if e.key == left_arrow and p.xvelocity < 0:
                    p.move_x(0)
                elif e.key == right_arrow and p.xvelocity > 0:
                    p.move_x(0)
                elif e.key == up_arrow and p.yvelocity < 0:
                    p.move_y(0)
                elif e.key == s_key:
                    p.attack('',True)
                elif e.key == d_key:
                    p.attack('',True)

    def check_collisions(self):
        for e in self.current_room.enemy_list:
            e.target = self.player
            if e.dead:
                pu = PickUp(e.rect.center)
                self.current_room.item_list.append(pu)
                self.current_room.enemy_list.remove(e)
        self.current_room.check_collisions()
        if self.current_room.goto_next:
            self.current_room = self.current_room.next_room()
            self.player.set_position(self.current_room.player_pos_left)
            self.current_room.player = self.player
        if self.current_room.goto_previous:
            self.current_room = self.current_room.previous_room()
            self.player.set_position(self.current_room.player_pos_right)
            self.current_room.player = self.player
        if self.player.dead:
            self.next = GameOver()
            self.quit()

    def update_screen(self):
        self.screen.blit(self.canvas, self.canvas_pos)
        self.current_room.update_screen()
        if self.show_debug:
            self.heads_up_display.show_debug()
        self.heads_up_display.update()
        pygame.display.update()




