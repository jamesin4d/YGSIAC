# Created by a human
# when:
# 8/22/2015
# 6:29 AM
#
#
# --------------------------------------------------------------------
from mapper import *
from engine import State



from player import Player
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

    def check_events(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.close_game()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_DOWN:
                    self.cursor.cycle_down()
    # i wish this was an 'or' statement
    # like if(down-arrow OR s is pressed)
                if e.key == pygame.K_s:     # press s for down
                    self.cursor.cycle_down()
                if e.key == pygame.K_UP:
                    self.cursor.cycle_up()
                if e.key == pygame.K_w:     # or w for up!
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
        #this is how maps get changed
        self.i = 0
        self.level = Mapper()
        self.level.new_inst(self.i)
        self.level.re_init()
        self.player = Player(40,300)
        self.player.move(0,0)
        self.mainSprite = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.exitLeft = pygame.sprite.Group()
        self.exitRight = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.solids = pygame.sprite.Group()
        self.background = pygame.sprite.Group()
        self.enemy_projectiles = pygame.sprite.Group()
        self.mainSprite.add(self.player)
        self.reset_groups()

    # this function takes any sprite the Mapper put into a list
    # and puts them into groups for ease of access here
    def reset_groups(self):
        level = self.level
        self.exitRight = None
        self.exitLeft = None
        self.background = None
        self.solids = None
        self.enemies = None
        self.projectiles = None
        self.enemy_projectiles = None

        self.projectiles = pygame.sprite.Group()
        self.enemy_projectiles = pygame.sprite.Group()
        self.exitLeft = pygame.sprite.Group()
        for ex in level.exitL:
            self.exitLeft.add(ex)
        self.exitRight = pygame.sprite.Group()
        for ex in level.exitR:
            self.exitRight.add(ex)
        self.background = pygame.sprite.Group()
        for b in level.background:
            self.background.add(b)
        self.solids = pygame.sprite.Group()
        for so in level.collisionList:
            self.solids.add(so)
        self.enemies = pygame.sprite.Group()
        for e in level.enemyList:
            self.enemies.add(e)
        return

# events loop, feeds the player.dir values to handle player
# animation, also handles the player jump and walk speed
    def check_events(self):
        p = self.player
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.close_game()
                sys.exit()
            elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                if p.canShoot:
                    self.projectiles.add(Bullet(p.rect.center, p.angle))
                    p.munitions -= 1
            elif e.type == pygame.MOUSEMOTION:
                p.mouse_angle(e.pos)
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    self.close_game()
                    sys.exit()
                if e.key == pygame.K_a:
                    p.move(-5,0)
                elif e.key == pygame.K_d:
                    p.move(5,0)
                elif e.key == pygame.K_w:
                    p.move(0,-5)
                elif e.key == pygame.K_s:
                    p.move(0,5)
                elif e.key == pygame.K_e:
                    p.action = True
            elif e.type == pygame.KEYUP:
                if e.key == pygame.K_a and p.xvelocity < 0:
                    p.move_x(0)
                elif e.key == pygame.K_d and p.xvelocity > 0:
                    p.move_x(0)
                elif e.key == pygame.K_w and p.yvelocity < 0:
                    p.move_y(0)
                elif e.key == pygame.K_s and p.yvelocity > 0:
                    p.move_y(0)
                elif e.key == pygame.K_e:
                    p.action = False
                elif e.key == pygame.K_r:
                    p.reload()

# the collision detection has been cleaned up quite a bit, it's no longer
    def check_collisions(self):
        # set up some local variables
        L = self.level
        solids = L.collisionList
        player = self.player
        projectiles = self.projectiles
        EL = L.exitL
        ER = L.exitR
        enemies = L.enemyList

        player.check_collisions(solids)
        player.update()
        for e in enemies:
            e.target = player
            e_h = pygame.sprite.spritecollide(e, projectiles, True)
            if e_h:
                e.take_damage(player.damage)
                if e.health < 0:
                    e.kill()
                    enemies.remove(e)
            e.barriers = solids
            e.check_collisions(solids)
            e.update()
            bullets = e.bullets
            for b in bullets:
                self.enemy_projectiles.add(b)
        projectiles.update(solids)
        self.enemy_projectiles.update(solids)

        e_p = pygame.sprite.spritecollide(player, enemies, False)
        if e_p:
            player.take_damage(1)


# here is the best solution i've found to the 'room change' effect.
# it works well, and it's only 14 lines
        playerExitStageRight = pygame.sprite.spritecollide(player, ER, False)
        playerExitStageLeft = pygame.sprite.spritecollide(player, EL, False)
        if playerExitStageRight: # player collides with exit block
            player.rect.x = 40   # move x-axis to start of next room
            self.i += 1          # cycle the map up
            L.new_inst(self.i)   # call new instance method to load new room
            L.re_init()          # the reinitialize method to build new room
            self.reset_groups()  # finally reset the Game state's sprite groups
        elif playerExitStageLeft:
            player.rect.x = 700
            self.i -= 1
            L.new_inst(self.i)
            L.re_init()
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
        pygame.display.update()
