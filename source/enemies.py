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
    def __init__(self):
        Base.__init__(self)
        self.target = None
        self.barriers = None
        self.state = None
        self.dx = ()
        self.dy = ()
        self.target_in_range = False

    def target_distance(self):
        target_position = self.target.get_position()
        position = self.get_position()
        tp = target_position
        sp = position
        dx = tp[0] - sp[0]
        dy = tp[1] - sp[1]
        diff = (dx, dy)
        self.dx = dx
        self.dy = dy
        range_x = False
        range_y = False
        if 150 > diff[0] > -150:
            range_x = True
        if 150 > diff[1] > -150:
            range_y = True

        if range_x and range_y:
            self.target_in_range = True
        else: self.target_in_range = False
        return diff


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

    def roam(self):
        pass





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
        self.get_frames('img/security.png')
        Enemy.__init__(self)
        self.health = random.randint(5,10)
        self.max_health = 12.0
        self.bullets = []
        self.shot_timer = random.randint(10,20)
        self.movement_rate = 2

    def update(self):
        self.animate()
        self.target_distance()
        self.aim(self.target)

        if self.target_in_range:
            self.shot_timer -= 1
            if self.shot_timer < 0:
                self.shot_timer = random.randint(10,20)
                self.bullets.append(EnemyBullet(self.rect.center, self.angle))
            if self.health > 5:
                self.pursue_target()
            else:
                random.choice((self.flee_target(),self.flee_directly()))


class Blob(Enemy):
    def __init__(self):
        self.get_frames('img/finnyblub.png')
        Enemy.__init__(self)
        self.health = 10
        self.max_health = 10

    def update(self):
        self.animate()




