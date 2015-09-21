# Created by a human
# when:
#8/22/2015
#6:19 AM
#
#
#--------------------------------------------------------------------
from entities import *

# ---------------------------------------------------------------------------------------------------
# so the idea here is: subclass the Base class so that we have an
# Enemy type, then use the Enemy class as a parent to the different types
# of enemy. the parent enemy class will have a 'behavioural tree' of methods
# for the child class to inherit from, deciding what to do based on state
# ------------------------------------------------------------------------
class Enemy(Base):
    aggressive = False
    aggression = 0

    alerted = False
    alerts = 0

    scared = False
    fear = 0

    idle = False
    boredom = 0

    target_in_range = False
    target_x_range = False
    target_y_range = False
    horizontal_speed = 0
    vertical_speed = 0

    def __init__(self, x, y , left, right):
        Base.__init__(self)
        self.target = None
        self.barriers = None
        self.start_x = None
        self.state = None
        self.dx = ()
        self.dy = ()
        self.boundsL = left
        self.boundsR = right
        self.set_position((x,y))
        self.horizontal_speed = 3


    def check_target(self):
        self.aim(self.target)

        target_position = self.target.get_position()
        position = self.get_position()
        tp = target_position
        sp = position
        dx = tp[0] - sp[0]
        dy = tp[1] - sp[1]
        diff = (dx, dy)
        self.dx = dx
        self.dy = dy
        if 150 > diff[0] > -150:
            self.target_x_range = True
        if 150 > diff[1] > -150:
            self.target_y_range = True
        if self.target_x_range and self.target_y_range:
            self.target_in_range = True
        else: self.target_in_range = False
        return diff

    def walk_left(self):
        return self.move_x(-self.horizontal_speed)

    def walk_right(self):
        return self.move_x(self.horizontal_speed)

    def get_started(self):
        if self.xvelocity == 0:
            self.xvelocity += 2
            if self.xvelocity > self.horizontal_speed:
                self.xvelocity = self.horizontal_speed

    def roam(self):
        self.get_started()
        if self.rect.x >= self.boundsR:
            self.walk_left()
        if self.rect.x <= self.boundsL:
            self.walk_right()


    def pursue_directly(self):
        if self.dx != 0:
            if self.dx < -10:
                self.move_x(-2)
            elif self.dx > 10:
                self.move_x(2)
        if self.dy != 0:
            if self.dy < -10:
                self.move_y(-2)
            elif self.dy > 10:
                self.move_y(2)

    def pursue_target(self):
        dx = self.dx
        dy = self.dy
        if dx != 0 or dy != 0:
            if dx < -1:
                self.move(-2,0)
            if dx > 1:
                self.move(2,0)
            if dy < -1:
                self.move(0,-2)
            if dy > 1:
                self.move(0,2)

    def flee_target(self):
        dx = self.dx
        dy = self.dy
        if dx != 0 or dy != 0:
            if dx < -1:
                self.move(2,0)
            if dx > 1:
                self.move(-2,0)
            if dy < -1:
                self.move(0,2)
            if dy > 1:
                self.move(0,-2)

    def flee_directly(self):
        if self.dx != 0:
            if self.dx < -10:
                self.move_x(2)
            elif self.dx > 10:
                self.move_x(-2)
        if self.dy != 0:
            if self.dy < -10:
                self.move_y(2)
            elif self.dy > 10:
                self.move_y(-2)

class Security(Enemy):
    def __init__(self, x, y , left, right):
        self.get_frames('img/player/heroLeft.png', 'img/player/heroRight.png', 'img/player/jumpLeft.png', 'img/player/jumpRight.png',
                        'img/player/punchLeft.png', 'img/player/punchRight.png', 'img/player/idleLeft.png', 'img/player/idleRight.png')
        Enemy.__init__(self, x, y , left, right)
        self.health = random.randint(4,6)
        self.max_health = 6.0
        self.bullets = []
        self.shot_timer = random.randint(10,20)
        self.horizontal_speed = 2
        self.gravity = 1

    def update(self, objects):
        self.animate()
        self.move_and_check(objects)
        self.check_target()
        self.roam()








