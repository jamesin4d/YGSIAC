# Created by a human
# when:
#8/22/2015
#6:24 AM
#
#
#--------------------------------------------------------------------

from entities import *

class Peashooter(Item):
    damage = random.randint(5,10)
    def __init__(self):
        Item.__init__(self)
