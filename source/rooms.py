# Created by a human
# when:
#8/24/2015
#6:45 AM
#
#--------------------------------------------------------------------
import json
import pygame

# a finite state machine for switching between 'rooms' in game
class World(object):
    def __init__(self):
        self.current_room = Room()
        self.rooms = []

    def run(self):
        self.rooms = [self.current_room]
        while self.rooms:
            self.current_room = self.rooms.pop()
            if self.current_room.paused:
                self.current_room.unpause()
            next_room, paused = self.current_room.mainloop()
            if self.current_room.kill_previous and self.rooms:
                self.rooms.pop()
            if paused:
                self.rooms.append(self.current_room)
            if next_room:
                self.rooms.append(next_room)


class Room(object):
    tilewidth = 0
    tileheight = 0
    map_file = None
    map_dictionary = None
    layers = None
    tilesets = None
    roomheight = 0
    roomwidth = 0
    tile_id = 1
    all_tiles = {}
    left_exit = []
    right_exit = []
    collision_list = []
    enemy_list = []
    item_list = []
    def __init__(self):
        self.done = False
        self.next = None
        self.kill_previous = False
        self.paused = False
        self.screen = pygame.display.get_surface()

    def main_start(self):
        open_file = open(self.map_file).read()
        self.map_dictionary = json.loads(open_file)
        self.layers = self.map_dictionary["layers"]
        self.tilesets = self.map_dictionary["tilesets"]
        self.roomheight = self.layers[0]["height"]
        self.roomwidth = self.layers[0]["width"]

        for ts in self.tilesets:
            self.tileheight = ts["tileheight"]
            self.tilewidth = ts["tilewidth"]
            tilesurface = pygame.image.load("maps/" + ts["image"])
            tilesurface.set_colorkey((255,255,255))
            for y in range(0, ts["imageheight"], ts["tileheight"]):
                for x in range(0, ts["imagewidth"], ts["tilewidth"]):
                    r = pygame.Rect(x, y, ts["tilewidth"], ts["tileheight"])
                    tile = tilesurface.subsurface(r)
                    self.all_tiles[self.tile_id] = tile
                    self.tile_id += 1
        return self.all_tiles, self.tilewidth, self.tileheight

    def pause(self):
        self.paused = True

    def unpause(self):
        self.paused = False
        self.done = False
        self.next = None