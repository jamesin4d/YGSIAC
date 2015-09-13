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
    equipment = {
        'head' : None,
        'body' : None,
        'weapon' : None,
        'feet' : None,
        'drop' : None
    }
    head = equipment['head']
    body = equipment['body']
    weapon = equipment['weapon']
    feet = equipment['feet']
    drop = equipment['drop']

    def __init__(self):
        Base.__init__(self)
        self.target = None
        self.barriers = None
        self.state = None
        self.dx = ()
        self.dy = ()
        self.target_in_range = False
        self.target_x_range = False
        self.target_y_range = False
        self.collide_right = False
        self.collide_left = False
        self.collide_top = False
        self.collide_bottom = False

    def check_target(self):
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


    def check_collisions(self, objects):
        self.collide_right = False
        self.collide_left = False
        self.rect.x += self.xvelocity
        for o in objects:
            if pygame.sprite.collide_rect(self, o):
                if isinstance(o, Solid):
                    if self.xvelocity < 0:
                        self.rect.left = o.rect.right
                        self.collide_left = True
                    if self.xvelocity > 0:
                        self.rect.right = o.rect.left
                        self.collide_right = True
        self.collide_top = False
        self.collide_bottom = False
        self.rect.y += self.yvelocity
        for o in objects:
            if pygame.sprite.collide_rect(self, o):
                if isinstance(o, Solid):
                    if self.yvelocity < 0:
                        self.rect.top = o.rect.bottom
                        self.collide_top = True
                    if self.yvelocity > 0:
                        self.rect.bottom = o.rect.top
                        self.collide_bottom = True

    def check_collide_state(self):
        if self.collide_right:
            self.move_x(-3)
        elif self.collide_left:
            self.move_x(3)
        if self.collide_top:
            self.move_y(3)
        elif self.collide_bottom:
            self.onGround = True
            self.move_y(0)



    def roam(self):
        self.move(-3,0)

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
    def __init__(self):
        self.get_frames('img/guy.png')
        Enemy.__init__(self)
        self.health = random.randint(15,20)
        self.max_health = 20.0
        self.bullets = []
        self.shot_timer = random.randint(10,20)


    def check_state(self):
        self.check_collide_state()
        if self.target_in_range and not (self.aggressive and self.alerted):
            self.aggression += .5
            self.alerts += 2
            if self.alerts > 100:
                self.alerted = True
                self.alerts = 100
            if self.aggression > 50 and self.alerted:
                self.aggression += 1
            if self.aggression > 100:
                self.aggressive = True
                self.aggression = 100



    def update(self):
        self.animate()
        self.roam()
        self.check_self()
        self.check_target()
        self.aim(self.target)
        self.check_state()


class Turret(Enemy):
    def __init__(self):
        self.get_frames('img/turret.png')
        Enemy.__init__(self)
        self.health = 10
        self.max_health = 10
        self.bullets = []

    def update(self):
        self.animate()
        self.check_target()
        self.aim(self.target)





