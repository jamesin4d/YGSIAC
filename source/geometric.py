# Created by a human
# when:
#9/1/2015
#10:37 PM
# this module will house some vector maths, as well as a quadtree
# for collision detection
#--------------------------------------------------------------------
import math
import itertools
from pygame import Rect

def get_line(start, end):
    # Setup initial conditions
    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1
    is_steep = abs(dy) > abs(dx)

    # Rotate line
    if is_steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    # Swap start and end points if necessary and store swap state
    swapped = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        swapped = True
    # Recalculate differentials
    dx = x2 - x1
    dy = y2 - y1
    # Calculate error
    error = int(dx / 2.0)
    ystep = 1 if y1 < y2 else -1
    # Iterate over bounding box generating points between start and end
    y = y1
    points = []
    for x in range(x1, x2 + 1):
        coord = (y, x) if is_steep else (x, y)
        points.append(coord)
        error -= abs(dy)
        if error < 0:
            y += ystep
            error += dx
    # Reverse the list if the coordinates were swapped
    if swapped:
        points.reverse()
    return points

class Vector:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __repr__(self): # returns a description of the object
        return "Vector (%s, %s)"%(self.x, self.y)

    def copy(self):
        return Vector(self.x, self.y)

    def dot(self, other):
        return self.x*other.x, self.y*other.y

    def __add__(self, other):
        return Vector(self.x+other.x, self.y+other.y)

    def __neg__(self):
        return Vector(-self.x, -self.y)

    def __sub__(self, other):
        return -other + self

    def __mul__(self, scalar):
        return Vector(self.x*scalar, self.y*scalar)
    __rmul__ = __mul__

    def __div__(self, scaler):
        return 1.0/scaler*self


    def angle(self):
        return math.degrees(math.atan2(self.y, self.x))

    def rotate(self, ang):
        ang = self.angle()+ang
        mag = self.magnitude()
        x = math.cos(math.radians(ang)) * mag
        y = math.sin(math.radians(ang)) * mag
        return Vector(x, y)

    def magnitude(self):
        return math.sqrt(self.x*self.x + self.y*self.y)

    def normalize(self):
        inverse_magnitude = 1.0/self.magnitude()
        return Vector(self.x*inverse_magnitude, self.y*inverse_magnitude)

    def perpendicular(self):
        return Vector(-self.y, self.x)

class Projection:

    def __init__(self, min, max):
        self.min, self.max = min, max

    def intersection(self, other):
        if self.max > other.min and other.max > self.min:
            return self.max-other.min
        return 0


class Quad(object):
    __slots__ = ['items', 'cx', 'cy', 'nw', 'sw', 'ne','se']
    def __init__(self, items, depth = 4, bounds = None):
        self.nw, self.sw, self.ne, self.se = None
        depth -= 1
        if depth == 0 or not items:
            self.items = items
            return

        if bounds:
            bounds = Rect(bounds)
        else:
            bounds = Rect(items[0]).unionall(items[1:])

        cx = self.cx = bounds.centerx
        cy = self.cy = bounds.centery
        self.items = []
        nw_items = []
        ne_items = []
        se_items = []
        sw_items = []
        for i in items:
            in_nw = i.left <= cx and i.top <= cy
            in_sw = i.left <= cx and i.bottom >= cy
            in_ne = i.right >= cx and i.top <= cy
            in_se = i.right >= cx and i.bottom >= cy
            if in_nw and in_ne and in_se and in_sw:
                self.items.append(i)
            else:
                if in_nw: nw_items.append(i)
                if in_ne: ne_items.append(i)
                if in_se: se_items.append(i)
                if in_sw: sw_items.append(i)
        if nw_items:
            self.nw = Quad(nw_items, depth, (bounds.left, bounds.top, cx,cy))
        if ne_items:
            self.ne = Quad(ne_items, depth, (cx, bounds.top, bounds.right, cy))
        if sw_items:
            self.sw = Quad(sw_items, depth, (bounds.left, cy, cx, bounds.bottom))
        if se_items:
            self.se = Quad(se_items, depth, (cx, cy, bounds.right, bounds.bottom))

    def __iter__(self):
        return itertools.chain(self.items, self.nw, self.ne, self.se, self.sw)

    def hit(self, rect):
        hits = set(tuple(self.items[i]) for i in rect.collidelistall(self.items))
        if self.nw and rect.left <= self.cx and rect.top <= self.cy:
            hits |= self.nw.hit(rect)
        if self.sw and rect.left <= self.cx and rect.bottom >= self.cy:
            hits |= self.sw.hit(rect)
        if self.ne and rect.right >= self.cx and rect.top <= self.cy:
            hits |= self.ne.hit(rect)
        if self.se and rect.right >= self.cx and rect.bottom >= self.cy:
            hits |= self.se.hit(rect)
        return hits
