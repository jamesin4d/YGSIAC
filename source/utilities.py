# Created by a human
# when:
#8/22/2015
#4:55 AM
#
#
import pygame

class Event_coordinator(object):
    pg = pygame
    L = False
    R = False
    U = False
    D = False
    close = False


    def __init__(self, pl):
        self.player = pl

    def check(self):
        p = self.player
        pg = self.pg
        k_d = pg.KEYDOWN
        k_u = pg.KEYUP
        up = pg.K_w and pg.K_UP
        down = pg.K_s and pg.K_DOWN
        left = pg.K_a and pg.K_LEFT
        right = pg.K_d and pg.K_RIGHT
        left_click = pygame.MOUSEBUTTONDOWN
        q = pg.QUIT

        for e in pg.event.get():
            if e.type == q:
                self.close = True
            if e.type == k_d and e.key == up:
                p.up()
            if e.type == k_d and e.key == left:
                p.left()
            if e.type == k_d and e.key == right:
                p.right()
            if e.type == k_d and e.key == down:
                p.down()




try:
    pygame.mixer.init()
except:
    print "could not initialize sound"
    sound = False

class NoSound:
    def play(self): pass

# ----------------------------------------------------------------------------------------------------
# DataGod prototype object for a data caching script to load all graphics and sounds once on start up.
# ----------------------------------------------------------------------------------------------------
class DataGod(object):
    def __init__(self):
        self.game_images = None
        self.game_sounds = None

    def load_game_images(self):
        names = [
            "img/logo.png",
            "img/startscreen.png",
            "img/quitscreen.png",
            "img/security.png",
            "img/hero.png",
            "img/bullet2.png",
            "img/cursor.png",
            "img/dialog.png",
            "img/health.png",
            "maps/set.png",  ]
        self.game_images = self.load_graphics(names)
        return self.game_images

    @staticmethod
    def color(r,g,b,a):
        return pygame.Color((r,g,b,a))

    @staticmethod
    def rect(x,y,w,h):
        return pygame.Rect(x,y,w,h)

    @staticmethod
    def load_sound(sound_file):
        try:
            return pygame.mixer.Sound(sound_file)
        except:
            print "could not load sound:", sound_file
        return NoSound()

    @staticmethod
    def set_music(filename):
        pygame.mixer.music.load(filename)

    @staticmethod
    def get_image(image):
        img =  pygame.image.load(image).convert()
        img.set_colorkey((255,255,255))
        return img

    def load_graphics(self, names):
        gfx = {}
        for n in names:
            gfx[n] = self.get_image(n)
        return gfx

    def load_sounds(self, names):
        sounds = {}
        for n in names:
            sounds[n] = self.load_sound(n)
        return sounds

class Timer(object):
    def __init__(self, interval):
        self.count = 0
        self.interval = interval
        self.active = True

    def update(self):
        if not self.active:
            return None
        if self.count < self.interval:
            self.count += 1
        if self.count >= self.interval:
            self.count = 0
            return True
        return False

    def set_interval(self, value):
        self.interval = value

    def deactivate(self):
        self.active = False

    def activate(self):
        self.count = 0
        self.active = True


#centers one image in another->(surface)
def center(img_size, surf_size):
    img_x, img_y = img_size
    sur_x, sur_y = surf_size
    cen_x = sur_x/2 - img_x/2
    cen_y = sur_y/2 - img_y/2
    return [cen_x, cen_y]


#--------------------------------------------------------------------
class SpriteSheet(object):
#-------------------------------------------------------------------------
#pulls an image from a sheet, works well
# directions:
#   sheet = 'img/spritesheetpicture.png'
#   s = SpriteSheet(sheet)
#   s.get_image(x, y, w, h)
#           x: x location on sheet, y: y location
#           w: width of subimage, h: height
#-------------------------------------------------------------------------
    sprite_sheet = None
    def __init__(self, file_name):
        self.sprite_sheet = pygame.image.load(file_name).convert()
    def get_image(self, x, y, width, height):
        image = pygame.Surface([width, height]).convert()
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey((255,255,255))
        return image

#-----------------------------------------------------------------------------------
#Generic parent class for GUIs
# below is my attempts at gui. the parent class Widget works pretty well
# as does the Line_of_text class, the Bar won't update right
#TODO fix  bar.update
#-----------------------------------------------------------------------------------
class Widget(pygame.Surface):
    def __init__(self, size):
        pygame.Surface.__init__(self, size)
        self.size = size
        self.screen = pygame.display.get_surface()
        self.rect = self.get_rect()
#---positioning methods
    def set_pos(self, pos):
        self.rect.topleft = pos
    def get_pos(self):
        return self.rect.topleft
#-------------drawing method
    def redraw(self):
        self.screen.blit(self, self.rect)
        pygame.display.update(self.rect)

#int(max(min(currentHP / float(maxHP) * health_bar_width, health_bar_width), 0))
# health bar widget
class Bar(Widget):
    def __init__(self, size=(100, 14)):
        Widget.__init__(self, size)
        self.length = size[0]
    def update(self, length, max_length):
        self.fill((100,130,90))
        self.length = int(max(min(length/ float(max_length)*100, 100), 0))
        #pygame.draw.line(self, (100,130,100), (0, 2), (self.length*perc,2),10)
        self.redraw()
# line of text widget

class Line_of_text(Widget):
    def __init__(self, text, bgc, size=16, font="8bit.ttf"):
        self.font = pygame.font.Font(font, size)
        image = self.font.render(text, 0, (0,0,0), bgc)
        Widget.__init__(self, image.get_size())
        self.blit(image, (0,0))

    def update(self, text, bgc):
        image = self.font.render(text, 0, (0,0,0), bgc)
        self.blit(image, (0,0))
        self.redraw()