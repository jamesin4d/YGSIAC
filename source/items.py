# Created by a human
# when:
#8/22/2015
#6:24 AM
#
#
#--------------------------------------------------------------------
from entities import *

class Item(Base):
    def __init__(self):
        Base.__init__(self)

class Sign(Item):
    def __init__(self):
        Item.__init__(self)



