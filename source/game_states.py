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
from entities import *
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


class Transition(State):
    def __init__(self, next_state):
        State.__init__(self)
        self.next_state = next_state
        self.screen.fill((0,0,0))
        self.image = get_image("img/trans/transition.png")
        self.image = pygame.transform.scale(self.image, self.screen.get_size())
        self.image_pos = center(self.image.get_size(), self.screen.get_size())
        self.loading_bar = Loading_animated()
        self.loading_bar_pos = (600, 440)
        self.update_s = True
        self.length = 90
        self.count = 0



    def update_screen(self):
        self.loading_bar.update()
        self.counter()
        if self.update_s:
#            makes sure the screen stays black
            self.screen.fill((0,0,0))
            self.screen.blit(self.image, self.image_pos)
            self.screen.blit(self.loading_bar.image, self.loading_bar_pos)

            pygame.display.update()

    def counter(self):
        if self.count < self.length:
            self.count += 1
            if self.count >= self.length:
                self.next = self.next_state()
                self.quit()


    def check_events(self):
        for e in pygame.event.get():
            if e.type == pygame.VIDEORESIZE:
                self.image = pygame.transform.scale(self.image, (e.w, e.h))
                self.screen = pygame.display.set_mode((e.w, e.h), pygame.RESIZABLE)
            if e.type == pygame.QUIT:
                self.close_game()

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
        self.image = get_image('img/startscreen/title.png')
        self.image = pygame.transform.scale(self.image, self.screen.get_size())
        self.image_pos = center(self.image.get_size(), self.screen.get_size())
        self.ups = True
        self.set_up_buttons()
        music = 'sounds/startscreen.wav'
        self.music = pygame.mixer.Sound(music)
        #self.music.play()


    def set_up_buttons(self):
        logo = get_image('img/startscreen/titlelogo.png')
        logo_pos = (100, 20)
        self.logo = Button(logo, logo_pos)

        start_image = get_image('img/startscreen/new.png')
        start_pos = (500,280)
        self.start = Button(start_image, start_pos)
        load_image = get_image('img/startscreen/load.png')
        load_pos = (500, 325)
        self.load = Button(load_image, load_pos)
        options_image = get_image('img/startscreen/option.png')
        option_pos = (500,370)
        self.options = Button(options_image, option_pos)
        quit_image = get_image('img/startscreen/quit.png')
        quit_pos = (500,415)
        self.quit_button = Button(quit_image, quit_pos)
        self.button_list = (self.logo,self.start, self.load, self.options, self.quit_button)


    def update_screen(self):
        if self.ups:
            self.screen.fill((200,200,200))
            self.image = pygame.transform.scale(self.image, self.screen.get_size())
            self.screen.blit(self.image, self.image_pos)
            for b in self.button_list:
                self.screen.blit(b.image, b.position)

            pygame.display.flip()

    def check_events(self):
        for b in self.button_list:
            b.update()
        if self.start.clicked:
            self.next = Transition(Game)
            self.quit()
        if self.options.clicked:
            self.next = Options()
            self.quit()
        if self.quit_button.clicked:
            self.next = RealitySimulator()
            self.quit()
        for e in pygame.event.get():
            if e.type == pygame.VIDEORESIZE:
                self.image = pygame.transform.scale(self.image, (e.w, e.h))
                self.screen = pygame.display.set_mode((e.w, e.h), pygame.RESIZABLE)
            if e.type == pygame.QUIT:
                self.close_game()
            if e.type == pygame.KEYDOWN:
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
                    p.jumpSound.play()
                    p.jump(-p.jump_speed)
                if e.key == s_key:
                    p.attack(False)

            elif e.type == keyrelease:
                if e.key == left_arrow and p.xvelocity < 0:
                    p.move_x(0)
                elif e.key == right_arrow and p.xvelocity > 0:
                    p.move_x(0)
                elif e.key == up_arrow and p.yvelocity < 0:
                    p.move_y(0)
                elif e.key == s_key:
                    p.attack(True)


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




