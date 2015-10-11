# Created by a human
# when:
#8/22/2015
#4:55 AM
# modified:
# 9/6 7:58 pm
import pygame

#these are just two methods that do the same thing with different arguments
def print_info(surface, msg, x, row=0):
    font = pygame.font.Font(None, 12)
    text = font.render(msg, 1, (254,254,254))
    pos = [x,10+16*row]
    surface.blit(text, pos)
# they are used to put text on a surface, message = 'whatever you want'
def display_info(surface, message, font_size,  x, y):
    near_white = (254,254,254)
    font = pygame.font.Font(None, font_size)
    text = font.render(message, 1, near_white)
    pos = [x,y]
    surface.blit(text, pos)

def text_widget(r,g,b, text, size, x,y):
    screen = pygame.display.get_surface()
    col = color(r,g,b)



def color(r,g,b):
    return pygame.Color((r,g,b))

def rect(x,y,w,h):
    return pygame.Rect(x,y,w,h)

def get_image(image):
    img =  pygame.image.load(image).convert()
    img.set_colorkey((255,255,255))
    return img

def load_graphics(names):
    gfx = {}
    for n in names:
        gfx[n] = get_image(n)
    return gfx

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



