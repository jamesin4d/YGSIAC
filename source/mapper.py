# Created by a human
# when:
# 8/19/2015
# 6:37 AM
#
#
# --------------------------------------------------------------------
import json
import pygame
from entities import BackgroundTile, SolidBlock

def quickmap(filename):
    map_dictionary = json.loads(open(filename).read())
    rows = map_dictionary["height"]
    columns = map_dictionary["width"]
    tileheight = map_dictionary["tileheight"]
    tilewidth = map_dictionary["tilewidth"]
    world_rect = (columns*tilewidth, rows*tileheight)

    layers = map_dictionary["layers"]
    tilesets = map_dictionary["tilesets"]
    all_tiles = gather_images_from_set(tilesets)

    collision_list, background, foreground = populate_sprite_lists(layers, all_tiles, tileheight, tilewidth)
    return world_rect, collision_list, background, foreground, tileheight, tilewidth

def gather_images_from_set(tileset):
    all_tiles = {}
    img = tileset[0]["image"]
    tile_id = tileset[0]["firstgid"]
    ih = tileset[0]["imageheight"]
    iw = tileset[0]["imagewidth"]
    th = tileset[0]["tileheight"]
    tw = tileset[0]["tilewidth"]
    set_surf = pygame.image.load(img)
    set_surf.set_colorkey((255,255,255))
    for y in range(0,ih,th): #(start:0, range:imageheight, step: tileheight)
        for x in range(0,iw,tw):
            r = pygame.Rect(x,y,tw,th)
            tile = set_surf.subsurface(r)
            all_tiles[tile_id] = tile
            tile_id += 1
    return all_tiles

def populate_sprite_lists(layers, all_tiles, tw, th):
    collision_list = []
    background = []
    foreground = []
    for layer in layers:
        collision = False
        back = False
        fore = False
        if 'properties' in layer:
            properties = layer['properties']
            if 'collision' in properties:
                collision = True
            if 'fore' in properties:
                fore = True
            if 'back' in properties:
                back = True
        data = layer['data']
        index = 0
        for y in range(0, layer['height']):
            for x in range(0, layer['width']):
                id_key = data[index]
                if id_key != 0:
                    if collision:
                        solid = SolidBlock()
                        solid.rect = pygame.Rect(x*tw, y*th, tw, th)
                        solid.image = all_tiles[id_key]
                        collision_list.append(solid)
                    if fore:
                        foreground_tile = BackgroundTile()
                        foreground_tile.rect = pygame.Rect(x*tw, y*th, tw, th)
                        foreground_tile.image = all_tiles[id_key]
                        foreground.append(foreground_tile)
                    if back:
                        tile = BackgroundTile()
                        tile.rect = pygame.Rect(x*tw,y*th,tw,th)
                        tile.image = all_tiles[id_key]
                        background.append(tile)
                index += 1

    print len(collision_list)
    print len(background)
    print len(foreground)
    return collision_list, background, foreground



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
    foreground = None

    all_tiles = None
    map_rect = None
    def __init__(self):
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
        self.foreground = None
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

        self.map_rect = (self.mapwidth*self.tilewidth, self.mapheight*self.tileheight)
        return self.all_tiles, self.tileheight, self.tilewidth, self.map_rect

# -populates the layers lists and produces collide sprites
    def build_it(self):
        self.collisionList = []
        self.background = []
        self.foreground = []
        tw = self.tilewidth
        th = self.tileheight
        for layer in self.layers:
            collide = False # flag for a collidable sprite
            fore = False
            back = False
            if "properties" in layer:
                properties = layer["properties"]
                if "collision" in properties:
                    collide = True
                if "fore" in properties:
                    fore = True
                if "back" in properties:
                    back = True
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
                            tile = SolidBlock()
                            tile.rect = pygame.Rect(x*tw, y*th, tw, th)
                            tile.image = self.all_tiles[id_key]
                            self.collisionList.append(tile)
                        if fore:
                            tile = BackgroundTile()
                            tile.rect = pygame.Rect(x*tw,y*th,tw,th)
                            tile.image = self.all_tiles[id_key]
                            self.foreground.append(tile)
                        if back:
                            tile = BackgroundTile()
                            tile.rect = pygame.Rect(x*tw, y*th, tw, th)
                            tile.image = self.all_tiles[id_key]
                            self.background.append(tile)
                    index += 1
        return self.collisionList, self.background, self.foreground


