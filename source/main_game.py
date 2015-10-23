# Created by a human
# when:
#8/22/2015
#6:29 AM
#
#
#--------------------------------------------------------------------
from game_states import *
from engine import *
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (120,20)

def main():
    WIN_WIDTH = 1200
    WIN_HEIGHT = 480
    DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
    #DEPTH = 32
    #FLAGS = 0
    #CAMERA_SLACK = 32
    pygame.init()
    pygame.display.set_mode(DISPLAY)
    pygame.display.set_caption("You've Gotten Stuck Making A Game!")
    e = Engine()
    e.current_state = Logo()
    e.run()
