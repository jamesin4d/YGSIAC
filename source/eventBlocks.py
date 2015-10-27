# Created by a human
# when:
# 10/26/2015
# 1:05 PM
#
# the idea here is EventBlocks will be invisible event triggering rects
# in the game world, triggering dialog boxes and the like
# --------------------------------------------------------------------
from entities import *


class EventBlock(Base):
    def __init__(self,x,y):
        Base.__init__(self)
        self.rect = pygame.Rect(x,y,16,16)
