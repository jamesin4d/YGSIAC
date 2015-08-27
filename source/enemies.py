# Created by a human
# when:
#8/22/2015
#6:19 AM
#
#
#--------------------------------------------------------------------
from entities import *
from utilities import Timer
# f(n) = g(n) + h(n)

# ---------------------------------------------------------------------------------------------------
# this dictionary describes the move types available to the NPC
# using (x, y) coordinates for the grid that makes up the room
adjacent = {
    'direct' : [(1,0),(-1,0),(0,1),(0,-1)],
    'diagonal': [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)],
    'knight' : [(1,-2),(1,2),(-1,-2),(-1,2),(2,1),(2,-1),(-2,1),(-2,-1)] }

# these methods return the optimum movement heuristic for their respective move type
def direct(x,y):
    return x+y

def diagonal(x,y):
    return max(x,y)

def knight(x,y):
    return max((x//2+x%2), (y//2+y%2))

# heuristic defining dictionary linking 'move_type' to move_type()
heuristics = {
    'direct' : direct,
    'diagonal' : diagonal,
    'knight' : knight}

# ---------------------------------------------------------------------------------------------------
# so the idea here is: subclass the Base class so that we have an
# Enemy type, then use the Enemy class as a parent to the different types
# of enemy. the parent enemy class will have a 'behavioural tree' of methods
# for the child class to inherit from, deciding what to do based on state
# ------------------------------------------------------------------------
class Enemy(Base):

    def __init__(self):
        Base.__init__(self)
        self.target = None
        self.barriers = None
        self.moves = adjacent[self.move_type]
        self.heuristic = heuristics[self.move_type]
        self.start = self.get_position()
        self.dx = ()
        self.dy = ()
    def distance_to_target(self):
        # get the positions
        target_position = self.target.get_position()
        position = self.get_position()
        tp = target_position
        sp = position
        # dx = target.x - self.x
        dx = tp[0] - sp[0]
        # dy = target.y - self.y
        dy = tp[1] - sp[1]
        self.dx = dx
        self.dy = dy

    def pursue_target(self):
        self.distance_to_target()
        # move x-vector towards target
        if self.dx < 0:
            self.move_x(-2)
        elif self.dx > 0:
            self.move_x(2)
        # move y-vector towards target
        if self.dy < 0:
            self.move_y(-2)
        elif self.dy > 0:
            self.move_y(2)
        # if there's no difference, stop
        if self.dx == 0:
            self.move_x(0)
        elif self.dy == 0:
            self.move_y(0)

    def flee_target(self):
        # this method does the opposite of the above method
        self.distance_to_target()
        if self.dx < 0:
            self.move_x(2)
        elif self.dx > 0:
            self.move_x(-2)
        if self.dy < 0:
            self.move_y(2)
        elif self.dy > 0:
            self.move_y(-2)
        if self.dx == 0:
            self.stop()
        elif self.dy == 0:
            self.stop()

    def stop(self):
        self.move_x(0)
        self.move_y(0)








class Walker(Enemy):
    move_type = 'direct'
    def __init__(self):
        self.get_frames('img/security.png')
        Enemy.__init__(self)
        self.health = random.randint(40,60)
        self.max_health = 60.0


    def check_collisions(self, objects):
        self.rect.x += self.xvelocity
        for o in objects:
            if pygame.sprite.collide_rect(self, o):
                if isinstance(o, Solid):
                    if self.xvelocity < 0:
                        self.rect.left = o.rect.right
                    if self.xvelocity > 0:
                        self.rect.right = o.rect.left
        self.rect.y += self.yvelocity
        for o in objects:
            if pygame.sprite.collide_rect(self, o):
                if isinstance(o, Solid):
                    if self.yvelocity < 0:
                        self.rect.top = o.rect.bottom
                    if self.yvelocity > 0:
                        self.rect.bottom = o.rect.top
    def update(self):
        if self.health > 20:
            self.pursue_target()
        else:
            self.flee_target()
        if self.xvelocity < 0:
            self.direction = 'left'
        elif self.xvelocity > 0:
            self.direction = 'right'
        if self.yvelocity < 0:
            self.direction = 'up'
        elif self.yvelocity > 0:
            self.direction = 'down'

        if self.direction == 'left':
            frame = (self.rect.x//20) % len(self.walking_frames_left)
            self.image = self.walking_frames_left[frame]
        elif self.direction == 'right':
            frame = (self.rect.x//20) % len(self.walking_frames_right)
            self.image = self.walking_frames_right[frame]
        elif self.direction == 'up':
            frame = (self.rect.y//20) % len(self.walking_frames_up)
            self.image = self.walking_frames_up[frame]
        elif self.direction == 'down':
            frame = (self.rect.y//20) % len(self.walking_frames_down)
            self.image = self.walking_frames_down[frame]



