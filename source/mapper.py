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

# quick map method; takes a filename argument and returns a dictionary of map sprites
def quickmap(filename):
    map_dictionary = json.loads(open(filename).read())
    rows = map_dictionary["height"]
    columns = map_dictionary["width"]
    tileheight = map_dictionary["tileheight"]
    tilewidth = map_dictionary["tilewidth"]
    map_rect = (columns*tilewidth, rows*tileheight)

    layers = map_dictionary["layers"]
    tilesets = map_dictionary["tilesets"]
    all_tiles = gather_images_from_set(tilesets)

    collision, background, foreground = populate_sprite_lists(layers, all_tiles, tileheight, tilewidth)
    quickmap_dictionary = {
        'map_rect': map_rect,
        'collision': collision,
        'background': background,
        'foreground': foreground,
        'tileheight': tileheight,
        'tilewidth': tilewidth
    }
    return quickmap_dictionary

def gather_images_from_set(tileset):
    all_tiles = {}
    img = tileset[0]["image"]
    tile_id = tileset[0]["firstgid"]
    ih = tileset[0]["imageheight"]
    iw = tileset[0]["imagewidth"]
    th = tileset[0]["tileheight"]
    tw = tileset[0]["tilewidth"]
    set_surf = pygame.image.load('maps/' + img)
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






