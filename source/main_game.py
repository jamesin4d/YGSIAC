from game_states import *
from engine import *

def main():
    pygame.init()
    pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Y.G.S.I.A.C")
    e = Engine()
    e.current_state = Logo()

    e.run()
