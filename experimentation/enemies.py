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
# of enemy. the Enemy class will have the path finding algorithm
# built into it so that all enemies inherit these instructions
class Enemy(Base):
    def __init__(self):
        Base.__init__(self)
        self.start = self.get_position()
        self.target = None
        self.end = self.target.get_position()
        self.move_type = None
        self.moves = adjacent[self.move_type]
        self.heuristic = heuristics[self.move_type]

    def path_finding(self, barriers):
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
            if check not in (self.barriers|self.close_set):
                neighbors.add(check)
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

class Walker(Enemy):
    health = random.randint(40,60)
    max_health = 60.0
    def __init__(self):
        Enemy.__init__(self)
        self.get_frames('img/security.png')