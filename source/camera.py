# Created by a human
# when:
#10/2/2015
#4:21 PM
#
#
#--------------------------------------------------------------------
import pygame

class Camera(object):
    def __init__(self, camera_function, (width, height)):
        self.camera_function = camera_function
        self.state = pygame.Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_function(self.state, target.rect)

def simple_camera(camera, target_rect):
    screen = pygame.display.get_surface()
    HALF_WIDTH = screen.width / 2
    HALF_HEIGHT = screen.height / 2
    l, t, _, _ = target_rect
    _, _, w, h = camera
    return pygame.Rect(-l+HALF_WIDTH, -t+HALF_HEIGHT, w, h)

def complex_camera(camera, target_rect):
    screen = pygame.display.get_surface()
    screen_rect = screen.get_rect()
    WIN_WIDTH = screen_rect.width
    WIN_HEIGHT = screen_rect.height
    HALF_WIDTH = screen_rect.width / 2
    HALF_HEIGHT = screen_rect.height / 2
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t, _, _ = -l+HALF_WIDTH, -t+HALF_HEIGHT, w, h

    l = min(0, l)                           # stop scrolling at the left edge
    l = max(-(camera.width-WIN_WIDTH), l)   # stop scrolling at the right edge
    t = max(-(camera.height-WIN_HEIGHT), t) # stop scrolling at the bottom
    t = min(0, t)                           # stop scrolling at the top
    return pygame.Rect(l, t, w, h)