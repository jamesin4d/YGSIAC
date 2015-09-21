# Created by a human
# when:
# 8/22/2015
# 6:29 AM
#
#
# --------------------------------------------------------------------
from mapper import Mapper
from engine import State
from rooms import *
from player import Player
from projectiles import Shot
from hud import display_info, HUD
# GAME STATES *NOW WITH COMMENTS!!*
import sys
pygame.init()

# -----------------Splash screen state---------------------------------------------------------
class Logo(State):
    def __init__(self):
        State.__init__(self)
        self.next = StartScreen()
        self.screen.fill((0,0,0))
        self.image = pygame.image.load("img/logo.png")
        self.alpha = 0
        self.image.set_alpha(0)
        self.image_pos = center(self.image.get_size(), self.screen.get_size())
        self.fade = False
        self.lifetime = Timer(1)
        self.update_s = True

    def update_screen(self):
        if self.update_s:
#            makes sure the screen stays black
            self.screen.fill((0,0,0))
            self.screen.blit(self.image, self.image_pos)
            pygame.display.update()
# alternately, pygame.display.update() can be used,
    def tick(self):
        self.clock.tick(10)
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
            if e.type == pygame.QUIT:
                self.close_game()
# any key skips it, cause I really hate when you cant skip things
            if e.type == pygame.KEYDOWN:
                self.quit()

    def quit(self):
        State.quit(self)
# cursor object -------------------------------------------------------------------------------
# currently hardcoded for only startscreen state positions, but works well
# extending it to work else where would probably only require putting
# in more location dictionaries to cycle through for different screens
# ----------------------------------------------------------------------------------------------
class Cursor(object):
    def __init__(self):
        self.image = pygame.image.load('img/cursor.png')
        self.positions = {
            'start': (400, 356),
            'options': (400, 416),
            'quit': (400, 478)
        }
        self.pos = self.positions['start']
        self.pos_list = [
            self.positions['start'],
            self.positions['options'],
            self.positions['quit']
        ]
        self.index = 0

    def select(self):
        if self.index == 0:
            return Game()
        if self.index == 1:
            return StartScreen()
        if self.index == 2:
            return RealitySimulator()

    def cycle_down(self):
        if self.index == 2:
            self.index = 0
            self.pos = self.pos_list[self.index]
        else:
            self.index += 1
            self.pos = self.pos_list[self.index]
        return

    def cycle_up(self):
        if self.index == 0:
            self.index = 2
            self.pos = self.pos_list[self.index]
        else:
            self.index -= 1
            self.pos = self.pos_list[self.index]
        return

    def display(self, screen):
        screen.blit(self.image, self.pos)
# ----------------Start screen state-------------------------------------------------------------
class StartScreen(State):
    def __init__(self):
        State.__init__(self)
        self.kill_prev = True
        self.done = False
        self.next = Game()
        self.screen.fill((200,200,200))
        self.image = pygame.image.load('img/startscreen.png')
        self.image_pos = center(self.image.get_size(), self.screen.get_size())
        self.ups = True
        self.cursor = Cursor()


    def update_screen(self):
        if self.ups:
            self.screen.fill((200,200,200))
            self.screen.blit(self.image, self.image_pos)
            self.cursor.display(self.screen)
            pygame.display.flip()
# MOTHERFUCKING OR STATEMENTS!??!?
        # GTFO
    def check_events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.close_game()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_DOWN or e.key == pygame.K_s:
                    self.cursor.cycle_down()
                if e.key == pygame.K_UP or e.key == pygame.K_w:
                    self.cursor.cycle_up()
                if e.key == pygame.K_SPACE:
                    self.next = self.cursor.select()
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
        self.image = pygame.image.load("img/quitscreen.png")
        self.alpha = 0
        self.image.set_alpha(0)
        self.image_pos = center(self.image.get_size(), self.screen.get_size())
        self.fade = False
        self.lifetime = Timer(1)
        self.update_s = True

    def update_screen(self):
        if self.update_s:
            self.screen.fill((200,200,200))
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
        self.image = pygame.image.load("img/gameover.png")
        self.image_pos = center(self.image.get_size(), self.screen.get_size())

    def update_screen(self):
        self.screen.fill((40,40,40))
        self.screen.blit(self.image, self.image_pos)
        pygame.display.flip()
    def check_events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.close_game()
            if e.type == pygame.KEYDOWN:
                self.quit()
#------------------------ Game state!--------------------------------------------------------------
class Game(State):

    def __init__(self):
        #blam, initiate that parent class
        State.__init__(self)
        self.kill_prev = True
        self.screen.fill((0,0,0))
        self.show_debug = False

        self.room_list = [
            StartRoom(),
            RoomTwoTheCave(),
        ]
        self.current_room_number = 0
        self.current_room = self.room_list[self.current_room_number]
        self.map_parser = Mapper()
        self.map_parser.open_map(self.current_room.map_file)
        self.map_parser.reinit()



        self.player = Player()
        self.player.set_position(self.current_room.player_pos_left)
        self.heads_up_display = HUD(self.player)
        self.mainSprite = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.solids = pygame.sprite.Group()
        self.background = pygame.sprite.Group()
        self.enemy_projectiles = pygame.sprite.Group()
        self.mainSprite.add(self.player)
        self.reset_groups()

    def reset_groups(self):
        level = self.map_parser
        self.background = None
        self.solids = None
        self.enemies = None
        self.projectiles = None
        self.enemy_projectiles = None

        self.projectiles = pygame.sprite.Group()
        self.enemy_projectiles = pygame.sprite.Group()
        self.background = pygame.sprite.Group()
        for b in level.background:
            self.background.add(b)
        self.solids = pygame.sprite.Group()
        for so in level.collisionList:
            self.solids.add(so)
        self.enemies = pygame.sprite.Group()
        for e in self.current_room.enemy_list:
            e.target = self.player
            self.enemies.add(e)
        return

# events loop, feeds the player.dir values to handle player
# animation, also handles the player jump and walk speed
    def check_events(self):
        p = self.player
        pg = pygame
        keypress = pg.KEYDOWN
        keyrelease = pg.KEYUP
        esc = pg.K_ESCAPE
        w = pg.K_w
        s = pg.K_s
        d = pg.K_d
        a = pg.K_a
        j = pg.K_j
        up = pg.K_UP
        down = pg.K_DOWN
        left = pg.K_LEFT
        right = pg.K_RIGHT
        r = pg.K_r
        tab = pg.K_TAB
        for e in pg.event.get():
            if e.type == pg.QUIT:
                self.close_game()
                sys.exit()
            elif e.type == keypress:
                if e.key == esc:
                    self.close_game()
                    sys.exit()
                if e.key == a:
                    p.walk(-p.walk_speed)
                elif e.key == d:
                    p.walk(p.walk_speed)
                elif e.key == w:
                    p.jump(-p.jump_speed)
                elif e.key == j:
                    if p.canShoot:
                        self.projectiles.add(Shot(p.rect.center, p))
                        p.munitions -= 1
                elif e.key == tab:
                    self.show_debug = not self.show_debug
                elif e.key == up:
                    if self.show_debug:
                        p.jump_speed += 0.25
                elif e.key == down:
                    if self.show_debug:
                        p.jump_speed -= 0.25
                elif e.key == left:
                    if self.show_debug:
                        p.walk_speed -= 0.25
                elif e.key == right:
                    if self.show_debug:
                        p.walk_speed += 0.25
                elif e.key == pg.K_g:
                    if self.show_debug:
                        p.gravity += 0.1
                elif e.key == pg.K_f:
                    if self.show_debug:
                        p.gravity -= 0.1

            elif e.type == keyrelease:
                if e.key == a and p.xvelocity < 0:
                    p.move_x(0)
                elif e.key == d and p.xvelocity > 0:
                    p.move_x(0)
                elif e.key == w and p.yvelocity < 0:
                    p.move_y(0)
                elif e.key == s and p.yvelocity > 0:
                    p.move_y(0)
                elif e.key == r:
                    p.reload()

    def check_collisions(self):
        # set up some local variables
        L = self.map_parser
        solids = L.collisionList
        player = self.player
        projectiles = self.projectiles
        player.update(solids)
        projectiles.update(solids, self.enemies)
        self.enemy_projectiles.update(solids)
        for en in self.enemies:
            en.update(solids)

        playerExitStageRight = player.rect.x > 800
        playerExitStageLeft = player.rect.x < 0
        if playerExitStageRight: # if the player is off the screen

            self.current_room_number += 1         # cycle the map up
            self.current_room = self.room_list[self.current_room_number]
            L.open_map(self.current_room.map_file)   # call new instance method to load new room
            L.reinit()          # the reinitialize method to build new room
            player.set_position(self.current_room.player_pos_left)
            self.reset_groups()  # finally reset the Game state's sprite groups
        elif playerExitStageLeft:
            self.current_room_number -= 1
            self.current_room = self.room_list[self.current_room_number]
            L.open_map(self.current_room.map_file)
            L.reinit()
            player.set_position(self.current_room.player_pos_right)
            self.reset_groups()

        if player.dead:
            self.next = GameOver()
            self.quit()

    def update_screen(self):
        self.background.draw(self.screen)
        self.mainSprite.draw(self.screen)
        self.solids.draw(self.screen)
        self.enemies.draw(self.screen)
        self.projectiles.draw(self.screen)
        self.enemy_projectiles.draw(self.screen)
        if self.show_debug:
            self.heads_up_display.show_debug()
        self.heads_up_display.update()
        pygame.display.update()




