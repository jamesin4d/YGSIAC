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
    pygame.init()
    pygame.display.set_mode((800, 600), pygame.RESIZABLE)
    pygame.display.set_caption("You've Gotten Stuck In A Cave")
    e = Engine()
    e.current_state = Logo()
    e.run()
