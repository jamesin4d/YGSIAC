# Created by a human
# when:
#8/22/2015
#4:55 AM
# modified:
# 9/6 7:58 pm
import pygame

try:
    pygame.mixer.init()
except:
    print "could not initialize sound"
    sound = False

def print_info(surface, msg, x, row=0):
    font = pygame.font.Font(None, 12)
    text = font.render(msg, 1, (254,254,254))
    pos = [x,10+16*row]
    surface.blit(text, pos)

def display_info(surface, message, font_size,  x, y):
    near_white = (254,254,254)
    font = pygame.font.Font(None, font_size)
    text = font.render(message, 1, near_white)
    pos = [x,y]
    surface.blit(text, pos)

class NoSound:
    def play(self): pass

def load_game_images():
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
    game_images = load_graphics(names)
    return game_images

def color(r,g,b,a):
    return pygame.Color((r,g,b,a))

def rect(x,y,w,h):
    return pygame.Rect(x,y,w,h)


def load_sound(sound_file):
    try:
        return pygame.mixer.Sound(sound_file)
    except:
        print "could not load sound:", sound_file
    return NoSound()

def set_music(filename):
    pygame.mixer.music.load(filename)

def get_image(image):
    img =  pygame.image.load(image).convert()
    img.set_colorkey((255,255,255))
    return img

def load_graphics(names):
    gfx = {}
    for n in names:
        gfx[n] = get_image(n)
    return gfx

def load_sounds(names):
    sounds = {}
    for n in names:
        sounds[n] = load_sound(n)
    return sounds

#---------------------------------------------------------------------
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
    sprite_sheet = None
    def __init__(self, file_name):
        self.sprite_sheet = pygame.image.load(file_name).convert()

    def get_image(self, x, y, width, height):
        image = pygame.Surface([width, height]).convert()
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey((255,255,255))
        return image

    @staticmethod
    def strip_sheet_no_convert(filename,sheet_x,sheet_y,image_x,image_y):
        frames = []
        sprite_sheet = pygame.image.load(filename)
        sprite_sheet.set_colorkey((255,255,255))
        sheet_width = sheet_x
        sheet_height = sheet_y
        img_width = image_x
        img_height = image_y
        for y in range(0, sheet_height, img_height):
            for x in range(0, sheet_width, img_width):
                r = pygame.Rect(x,y,img_width, img_height)
                t = sprite_sheet.subsurface(r)
                frames.append(t)
        return frames

    @staticmethod
    def strip_sheet(filename,sheet_x,sheet_y,image_x,image_y):
        frames = []
        sprite_sheet = pygame.image.load(filename).convert()
        sprite_sheet.set_colorkey((255,255,255))
        sheet_width = sheet_x
        sheet_height = sheet_y
        img_width = image_x
        img_height = image_y
        for y in range(0, sheet_height, img_height):
            for x in range(0, sheet_width, img_width):
                r = pygame.Rect(x,y,img_width, img_height)
                t = sprite_sheet.subsurface(r)
                frames.append(t)
        return frames



