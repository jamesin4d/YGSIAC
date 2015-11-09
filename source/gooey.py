# Created by a human
# when:
# 10/27/2015
# 9:31 AM
# monkey number one million with a typewriter
#
# --------------------------------------------------------------------
import pygame

def print_info(surface, msg, x=10, row=0):
    font = pygame.font.Font(None, 16)
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
    col = pygame.Color((r,g,b))

class Label(pygame.sprite.Sprite):
    # a basic label
    #   properties:
    #       font: font to use
    #       text: text to display
    #       fgColor: foreground color
    #       bgColor: background color
    #       center: position of label's center
    #       size: (width, height) of label

    def __init__(self, fontName = "freesansbold.ttf"):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(fontName, 20)
        self.text = ""
        self.fgColor = ((0x00, 0x00, 0x00))
        self.bgColor = ((0xFF, 0xFF, 0xFF))
        self.center = (100, 100)
        self.size = (150, 30)

    def update(self):
        self.image = pygame.Surface(self.size)
        self.image.fill(self.bgColor)
        fontSurface = self.font.render(self.text, True, self.fgColor, self.bgColor)
        #center the text
        xPos = (self.image.get_width() - fontSurface.get_width())/2

        self.image.blit(fontSurface, (xPos, 0))
        self.rect = self.image.get_rect()
        self.rect.center = self.center

class Button(Label):
    """ a button based on the label
        same properties as label +
        active: True if user is clicking on sprite
                False if user is not currently clicking
        clicked: True when user releases mouse over a
                 currently active button
    """

    def __init__(self, image, (pos)):
        Label.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.position = pos
        self.rect.topleft = pos
        self.active = False
        self.clicked = False
        self.bgColor = (0xCC, 0xCC, 0xCC)

    def update(self):
        self.clicked = False
        #check for mouse input
        if pygame.mouse.get_pressed() == (1, 0, 0):
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.active = True
                print 'active'

        #check for mouse release
        if self.active:
            if pygame.mouse.get_pressed() == (0, 0, 0):
                self.active = False
                if self.rect.collidepoint(pygame.mouse.get_pos()):
                    self.clicked = True
                    print 'clicked'

class Scroller(Button):
    """ like a button, but has a numeric value that
        can be decremented by clicking on left half
        and incremented by clicking on right half.
        new atributes:
            value: the scroller's numeric value
            minValue: minimum value
            maxValue: maximum value
            increment: How much is added or subtracted
            format: format of string interpolation
    """

    def __init__(self):
        Button.__init__(self)
        self.minValue = 0
        self.maxValue = 10
        self.increment = 1
        self.value = 5
        self.format = "<<  %.2f  >>"

    def update(self):
        Button.update(self)
        if self.active:
            (mousex, mousey) = pygame.mouse.get_pos()
            if mousex < self.rect.centerx:
                self.value -= self.increment
                if self.value < self.minValue:
                    self.value = self.minValue
            else:
                self.value += self.increment
                if self.value > self.maxValue:
                    self.value = self.maxValue

        self.text = self.format % self.value

class MultiLabel(pygame.sprite.Sprite):
    # accepts a list of strings, creates a multi-line
    # label to display text
    # same properties as label except textLines
    # is a list of strings. There is no text property.
    # Set the size manually. Vertical size should be at
    # least 30 pixels per line (with the default font)


    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.textLines = ["This", "is", "sample", "text"]
        self.font = pygame.font.Font("freesansbold.ttf", 20)
        self.fgColor = ((0x00, 0x00, 0x00))
        self.bgColor = ((0xFF, 0xFF, 0xFF))
        self.center = (100, 100)
        self.size = (150, 100)

    def update(self):
        self.image = pygame.Surface(self.size)
        self.image.fill(self.bgColor)
        numLines = len(self.textLines)
        vSize = self.image.get_height() / numLines

        for lineNum in range(numLines):
            currentLine = self.textLines[lineNum]
            fontSurface = self.font.render(currentLine, True, self.fgColor, self.bgColor)
            #center the text
            xPos = (self.image.get_width() - fontSurface.get_width())/2
            yPos = lineNum * vSize
            self.image.blit(fontSurface, (xPos, yPos))

        self.rect = self.image.get_rect()
        self.rect.center = self.center




class Widget(pygame.Surface):
    def __init__(self, size, image=None):
        pygame.Surface.__init__(self, size)
        self.image = image
        self.size = size
        self.screen = pygame.display.get_surface()
        self.rect = self.get_rect()

    def set_position(self, pos):
        self.rect.topleft = pos

    def get_position(self):
        return self.rect.topleft

    def draw(self):
        if self.image is None:
            self.screen.blit(self, self.rect)
        else: self.screen.blit(self.image, self.rect)
        pygame.display.update(self.rect)


class Score(Widget):
    def __init__(self, title="", digits=8, size=18):
        self.color = (183,0,0)
        self.font = pygame.font.Font(None,size)
        self.title = title
        self.score = 0
        self.digits = digits
        self.text = title
        self.image = self.gen_image()
        Widget.__init__(self, self.image.get_size())
        self.fill((0,0,0))
        self.blit(self.gen_image(), (0,0))


    def gen_image(self):
        score = str(self.score)
        zeroes = "0" * (self.digits - len(score))
        msg = self.title + zeroes + score
        self.text = msg
        return self.font.render(msg, 0, self.color, (0,0,0))

    def update(self, score):
        self.score = score
        self.fill((0,0,0))
        self.blit(self.gen_image(), (0,0))
        self.draw()