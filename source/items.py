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

class StarterGun(Item):
    def __init__(self,x,y):
        Item.__init__(self)
        start_img = 'img/entities/dropitems/gun.png'
        self.image = get_image(start_img)
        self.rect = self.image.get_rect()
        self.set_position((x,y))

class Candle(Item):
    def __init__(self,x,y):
        Item.__init__(self)
        candle_sheet = 'img/entities/candle/candle.png'
        self.frames = SpriteSheet.strip_sheet(candle_sheet,128,16,16,16)
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.set_position((x,y))
        self.animation_timer = 0

    def animate(self):
        random_frame = random.randint(0,7)
        self.animation_timer += 1
        if self.animation_timer >= 5:
            self.image = self.frames[random_frame]
            self.animation_timer = 0

    def update(self):
        self.animate()





