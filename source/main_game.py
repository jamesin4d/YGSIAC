# Created by a human
# when:
#8/22/2015
#6:29 AM
#
#
#--------------------------------------------------------------------
from game_states import *
from engine import *



def main():
    WIN_WIDTH = 800
    WIN_HEIGHT = 600
    DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
    DEPTH = 32
    FLAGS = 0
    CAMERA_SLACK = 32
    pygame.init()
    pygame.display.set_mode(DISPLAY, FLAGS, DEPTH)
    pygame.display.set_caption("You've Gotten Stuck In A Cave")
    e = Engine()
    e.current_state = Logo()
    e.run()
