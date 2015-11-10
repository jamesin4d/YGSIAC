# Created by a human
# when:
# 11/9/2015
# 5:51 PM
# monkey number one million with a typewriter
#
# --------------------------------------------------------------------
from entities import Base

class Nimbot(Base):
    def __init__(self):
        Base.__init__(self)
        self.frames = self.get_frames('img/player/nimbot.png',192,32,16,32)
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.anim_duration = 7
        self.anim_counter = 0
        self.current_frame = 0

    def animate(self):
        if self.anim_counter < self.anim_duration:
            self.anim_counter += 1
        if self.anim_counter == self.anim_duration:
            self.current_frame += 1
            self.anim_counter = 0
        if self.current_frame >= len(self.frames):
            self.current_frame = 0
        self.image = self.frames[self.current_frame]

    def update(self):
        #print 'count:', self.anim_counter
        #print 'current', self.current_frame
        self.animate()