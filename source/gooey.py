# Created by a human
# when:
#10/11/2015
#3:02 AM
#
#
#--------------------------------------------------------------------
import pygame

class Widget(pygame.Surface):
    def __init__(self, size):
        pygame.Surface.__init__(self, size)
        self.size = size
        self.screen = pygame.display.get_surface()
        self.rect = self.get_rect()

    def set_position(self, pos):
        self.rect.topleft = pos

    def get_position(self):
        return self.rect.topleft

    def draw(self):
        self.screen.blit(self, self.rect)
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