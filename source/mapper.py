# Created by a human
# when:
# 8/19/2015
# 6:37 AM
#
#
# --------------------------------------------------------------------
import json
import pygame
from entities import Tile, Solid

class Level:
    map_file = None
    enemy_list = None
    item_list = None
    def __init__(self):
        self.enemy_list = []
        self.item_list = []

class RoomOne(Level):
    def __init__(self):
        Level.__init__(self)
        self.map_file = 'maps/roomone.json'

class RoomTwo(Level):
    def __init__(self):
        Level.__init__(self)
        self.map_file = "maps/roomtwo.json"


# Mapper class *NOW WITH COMMENTS*
#-------------------------------------------------------------------------
class Mapper(object):
    mapdict = None
    layers = None
    tilesets = None
    mapheight = 0
    mapwidth = 0
    tile_id = 1
    collisionList = None
    background = None
    all_tiles = None
    def __init__(self):
        self.done = False
        self.next = None
        self.paused = False
        self.tilewidth = 0
        self.tileheight = 0

    def open_map(self, x):
        open_map = open(x).read()
        self.mapdict = json.loads(open_map)
        self.layers = self.mapdict["layers"]
        self.tilesets = self.mapdict["tilesets"]
        self.mapheight = self.layers[0]["height"]
        self.mapwidth = self.layers[0]["width"]
        self.tile_id = 1
# this makes everything usable again for when another new_inst is used
    def reinit(self):
        self.all_tiles = None
        self.collisionList = None
        self.background = None
        # fills the all_tiles dictionary
        self.tile_sets()
        # populates the lists with sprites
        self.build_it()
        return
# populates the all_tiles dictionary
    def tile_sets(self):
        self.all_tiles = {}
        for tileset in self.tilesets:
            self.tileheight = tileset['tileheight']
            self.tilewidth = tileset['tilewidth']
            tilesurface = pygame.image.load("maps/" + tileset["image"])
            tilesurface.set_colorkey((255,255,255))
            for y in range(0, tileset["imageheight"], tileset["tileheight"]):
                for x in range(0, tileset["imagewidth"], tileset["tilewidth"]):
                    rect = pygame.Rect(x, y, tileset["tilewidth"], tileset["tileheight"])
                    tile = tilesurface.subsurface(rect)
                    self.all_tiles[self.tile_id] = tile
                    self.tile_id += 1
        return self.all_tiles, self.tileheight, self.tilewidth

# -populates the layers lists and produces collide sprites
    def build_it(self):
        self.collisionList = []
        self.background = []
        tw = self.tilewidth
        th = self.tileheight
        for layer in self.layers:
            collide = False # flag for a collidable sprite
            if "properties" in layer:
                properties = layer["properties"]
                if "collision" in properties:
                    collide = True
            # the data is the layers tile data, such as
            # which tile was used, where it goes in the level
            data = layer["data"]
            index = 0
            for y in range(0, layer["height"]):
                for x in range(0, layer["width"]):
                    id_key = data[index]
                    if id_key != 0:
                        #print id_key
                        if collide:
                            tile = Solid()
                            tile.rect = pygame.Rect(x*tw, y*th, tw, th)
                            tile.image = self.all_tiles[id_key]
                            self.collisionList.append(tile)
                        tile = Tile()
                        tile.rect = pygame.Rect(x*tw, y*th, tw, th)
                        tile.image = self.all_tiles[id_key]
                        self.background.append(tile)
                    index += 1
        return self.collisionList, self.background


