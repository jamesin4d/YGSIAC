# Created by a human
# when:
#8/22/2015
#11:14 AM
#

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

# f(n) = g(n) + h(n)  <- A* path finding algorithm where f(n) is equal to the movement cost, g(n)
# plus the estimated cost, h(n).
# the movement cost is something like 10 for a direct N,S,E,W move, 14 for a diagonal
# the estimated cost is what it would cost to go from the cell to the end point ignoring barriers
# example: move 3 North, move 6 East, end = estimated cost
# so below is my attempt at implementing the A* algorithm with the PathFinder object
class PathFinder(object):
    # constructor method, give it a start, end, move_type, barrier argument
    def __init__(self, start, end, move_type, barriers):
        self.start, self.end = start, end
        self.moves = adjacent[move_type]
        self.heuristic = heuristics[move_type]
        self.barriers = barriers
        self.setup()

    def setup(self):
        self.closed_set = {self.start}
        self.open = set()
        self.came_from = {}
        self.g = {self.start:0}
        self.h = {}
        self.f = {}
        self.current = self.start
        self.current = self.follow_path()
        self.solution = []
        self.solved = False

# ___________
# |__|___|__|
# |__|_X_|__|
# |__|___|__|
# so if X is the cell that is being used as 'start', i.e. where the NPC is, it will check each
# cell around it given the coordinates from self.moves; (i, j) are just x, y coordinates
    def get_neighbors(self):
        neighbors = set()
        for (i, j) in self.moves:
            check = (self.current[0]+i, self.current[1]+j)
            if check not in (self.barriers|self.closed_set): # if the cell checked isn't a barrier then add it to neighbors
                neighbors.add(check)
        return neighbors

#
    def follow_path(self):
        next_cell = None
        for cell in self.get_neighbors():
            possible_g = self.g[self.current]+1 # possible g(n) cell, checks
            if cell not in self.open: # if the cell is in the open list
                self.open.add(cell) # if it's not then add it
                possible = True     # possible g(n) cell remains true
            elif cell in self.g and possible_g < self.g[cell]: # or if the cell is in self.g and the return number is less that the [cell]
                possible = True     # possible g(n) remains true
            else:
                possible = False
            if possible:
                # x and y are equal to the absolute value of end(x) - cell(x), end(y) - cell(y)
                x, y = abs(self.end[0] - cell[0]), abs(self.end[1] - cell[1])
                self.came_from[cell] = self.current # i think this adds self.current to self.came_from
                # g(n) for this cell is the possible g(n) value for the cell
                self.g[cell] = possible_g
                # calculate the heuristic value for the given cell
                self.h[cell] = self.heuristic(x, y)
                # self.f(n) = g(n) + h(n)
                self.f[cell] = self.g[cell]+self.h[cell]
                if not next_cell or self.f[cell] < self.f[next_cell]:
                    next_cell = cell
        return next_cell

# this recursively builds the path for the solution list
    def path(self, cell):
        if cell in self.came_from:
            self.solution.append(cell)
            self.path(self.came_from[cell])


    def evaluate(self):
        if self.open and not self.solved:
            for cell in self.open:
                if (self.current not in self.open) or (self.f[cell] < self.f[self.current]):
                    self.current = cell
                if self.current == self.end:
                    self.path(self.current)
                    self.solved = True
                self.open.discard(self.current)
                self.closed_set.add(self.current)
                self.current = self.follow_path()
        elif not self.solution:
            self.solution = "no path solution found"
