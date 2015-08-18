# Created by a human
# when:
#8/17/2015
#3:53 PM
# f(n) = g(n) + h(n)
#
"""
def update(self,Surf):
        self.add_barriers()
        if self.mode == "RUN":
            if not self.Solver:
                self.time_start = pg.time.get_ticks()
                self.Solver = solver.Star(self.start_cell,self.goal_cell,self.piece_type,self.barriers)
            if self.animate:
                self.Solver.evaluate()
            else:
                while not self.Solver.solution:
                    self.Solver.evaluate()
            if self.Solver.solution:
                self.found_solution()
        if self.mode != "RUN" or self.animate:
            self.draw(Surf)
"""

import pygame as pg


adjacent = {
    'direct' : [(1,0),(-1,0),(0,1),(0,-1)],
    'diagonal' : [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)],
    'knight' : [(1,-2),(1,2),(-1,-2),(-1,2),(2,1),(2,-1),(-2,1),(-2,-1)]}

def direct(x, y):
    return x+y # optimum distance heuristic for direct nodes
def diagonal(x,y):
    return max(x,y) # odh for diagonals and directs
def knight(x,y):
    return max((x//2+x%2),(y//2+y%2)) #knight distance heuristic
heuristics = {
    'direct': direct,
    'diagonal' : diagonal,
    'knight' : knight}


class Guide(object):
    def __init__(self,start, end, move_type, obstacles):
        self.start, self.end = start, end
        self.moves = adjacent[move_type]
        self.heuristic = heuristics[move_type]
        self.obstacles = obstacles
        self.setup()

    def setup(self):
        self.close_set = {self.start} #set of cells to evaluate
        self.open_set = set()
        self.came_from = {}
        self.gx = {self.start:0}
        self.hx = {}
        self.fx = {}
        self.current = self.start
        self.current = self.followPath()
        self.solution = []
        self.solved = False

    def neighborhood(self):
        neighbors = set() #howdiddly hey there, neighbor!
        for (i,j) in self.moves:
            check = (self.current[0]+i, self.current[1]+j)
            if check not in (self.obstacles|self.close_set):
                neighbors.add(check)
        return neighbors

    def followPath(self):
        # this function ensures the current path stays
        # when multiple neighbors have the same
        # heuristic value
        next_cell = None
        for cell in self.neighborhood():
            hmm_gx = self.gx[self.current]+1
            if cell not in self.open_set:
                self.open_set.add(cell)
                good = True
            elif cell in self.gx and hmm_gx < self.gx[cell]:
                good = True
            else:
                good = False
            if good:
                x, y = abs(self.end[0]-cell[0]),abs(self.end[1]-cell[1])
                self.came_from[cell] = self.current
                self.gx[cell] = hmm_gx
                self.hx[cell] = self.heuristic(x,y)
                self.fx[cell] = self.gx[cell]+self.hx[cell]
                if not next_cell or self.fx[cell] < self.fx[next_cell]:
                    next_cell = cell
        return next_cell

    def path(self,cell):
        if cell in self.came_from: #recursively reconstructs the
            self.solution.append(cell) #path taken
            self.path(self.came_from[cell])


    def evaluate(self):
        if self.open_set and not self.solved:
            for cell in self.open_set:
                if (self.current not in self.open_set) or (self.fx[cell]<self.fx[self.current]):
                    self.current = cell
                if self.current == self.end:
                    self.path(self.current)
                    self.solved = True
                self.open_set.discard(self.current)
                self.close_set.add(self.current)
                self.current = self.followPath()
        elif not self.solution:
            self.solution = "no solution"