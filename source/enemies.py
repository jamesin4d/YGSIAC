# Created by a human
# when:
#8/22/2015
#6:19 AM
#
#
#--------------------------------------------------------------------
from entities import *
# f(n) = g(n) + h(n)

# ---------------------------------------------------------------------------------------------------
# this dictionary describes the move types available to the NPC
# using (x, y) coordinates for the grid that makes up the room
adjacent = {
    'direct' : [(32,0),(-32,0),(0,32),(0,-32)],
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
# of enemy. the Enemy class will have the path finding algorithm
# built into it so that all enemies inherit these instructions
class Enemy(Base):
    def __init__(self):
        Base.__init__(self)

        self.moves = adjacent[self.move_type]
        self.heuristic = heuristics[self.move_type]

    def path_finding(self, target, barriers):
        self.start = self.get_position()
        self.target = target
        self.end = self.target.get_position()
        self.barriers = barriers
        self.close_set = {self.start}
        self.open_set = set()
        self.came_from = {}
        self.g = {self.start:0}
        self.h = {}
        self.f = {}
        self.current = self.start
        self.current = self.follow_path()
        self.path_solution = []
        self.path_solved = False

    def get_neighbors(self):
        neighbors = set()
        for (i, j) in self.moves:
            check = (self.current[0]+i, self.current[1]+j)
            if check not in self.barriers or self.close_set:
                neighbors.add(check)
                #print neighbors
        return neighbors

    def follow_path(self):
        next_cell = None
        for cell in self.get_neighbors():
            possible = self.g[self.current] + 1
            if cell not in self.open_set:
                self.open_set.add(cell)
                pos = True
            elif cell in self.g and possible < self.g[cell]:
                pos = True
            else:
                pos = False
            if pos:
                x, y = abs(self.end[0] - cell[0]), abs(self.end[1]-cell[1])
                self.came_from[cell] = self.current
                self.g[cell] = possible
                self.h[cell] = self.heuristic(x,y)
                self.f[cell] = self.g[cell] + self.h[cell]
                if not next_cell or self.f[cell] < self.f[next_cell]:
                    next_cell = cell
        return next_cell

    # recursively builds the path
    def reconstruct_path(self, cell):
        if cell in self.came_from:
            self.path_solution.append(cell)
            self.reconstruct_path(self.came_from[cell])

    def evaluate_path(self):
        if self.open_set and not self.path_solved:
            for cell in self.open_set:
                if (self.current not in self.open_set) or (self.f[cell] < self.f[self.current]):
                    self.current = cell
                if self.current == self.end:
                    self.reconstruct_path(self.current)
                    self.path_solved = True
                self.open_set.discard(self.current)
                self.close_set.add(self.current)
                self.current = self.follow_path()
        elif not self.path_solution:
            self.path_solution = 'No path found'


class Walker(Enemy):
    move_type = 'direct'
    barriers = None
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
        tp = self.target.get_position()
        sp = self.get_position()
        dx = tp[0] - sp[0]
        dy = tp[1] - sp[1]
        self.path_finding(self.target, self.barriers)
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

        if dx < 0:
            self.move_x(-2)
        elif dx > 0:
            self.move_x(2)
        if dy < 0:
            self.move_y(-2)
        elif dy > 0:
            self.move_y(2)
        if dx == 0:
            self.move_x(0)
        if dy == 0:
            self.move_y(0)
       # print dx, dy


