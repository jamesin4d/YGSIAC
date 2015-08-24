# Created by a human
# when:
#8/24/2015
#6:45 AM
#
#--------------------------------------------------------------------
import json
from items import *
from enemies import *

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
    entities_list = []

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

    def build_room(self):
        tw = self.tilewidth
        th = self.tileheight
        for l in self.layers:
            collide = False
            left = False
            right = False
            enemy = False
            item = False

            if "properties" in l:
                p = l["properties"]
                if "collision" in p:
                    collide = True
                elif "exitL" in p:
                    left = True
                elif "exitR" in p:
                    right = True
                elif "enemy" in p:
                    enemy = True
                elif "item" in p:
                    item = True
            data = l["data"]
            index = 0
            for y in range(0, l["height"]):
                for x in range(0, l["width"]):
                    id_key = data[index]
                    if id_key != 0:
                        if collide:
                            solid = Solid()
                            solid.rect = pygame.Rect(x*tw, y*th, 26, 26)
                            solid.image = self.all_tiles[id_key]
                            self.entities_list.append(solid)
                        if left:
                            exitL = Exit()
                            exitL.rect = pygame.Rect(x*tw, y*th, tw, th)
                            exitL.image = self.all_tiles[id_key]
                            self.entities_list.append(exitL)
                        if right:
                            exitR = Exit()
                            exitR.rect = pygame.Rect(x*tw, y*th, tw, th)
                            exitR.image = self.all_tiles[id_key]
                            self.entities_list.append(exitR)
                        if enemy:
                            img = self.all_tiles[id_key]
                            e = self.gather_data(x*tw, y*th, id_key, img)
                            enem = self.sort_type(e)
                            self.entities_list.append(enem)
                        if item:
                            img = self.all_tiles[id_key]
                            i = self.gather_data(x*tw, y*th, id_key, img)
                            it = self.sort_type(i)
                            self.entities_list.append(it)
                        tile = Tile()
                        tile.rect = pygame.Rect(x*tw, y*th, tw, th)
                        tile.image = self.all_tiles[id_key]
                        self.entities_list.append(tile)
                    index += 1
        return self.entities_list


    @staticmethod
    def gather_data(x, y, idkey, image):
        return x, y, idkey, image
    # the staticmethod allows the use of this method without a 'self' argument,
    @staticmethod
    def sort_type(what):
        x = what[0]
        y = what[1]
        idkey = what[2]
        image = what[3]
        if idkey == 89:
            item = Sign()
            item.image = image
            item.rect = item.image.get_rect()
            item.rect.x = x
            item.rect.y = y
            item.idkey = idkey
            return item
        if idkey == 28:
            enemy = Walker()
            enemy.rect.x = x
            enemy.rect.y = y
            enemy.idkey = idkey
            return enemy


    def pause(self):
        self.paused = True

    def unpause(self):
        self.paused = False
        self.done = False
        self.next = None