# Created by a human
# when:
# 8/19/2015
# 6:37 AM
#
#
# --------------------------------------------------------------------
import json
from items import *
from enemies import *


class Sorter(object):
    def __init__(self):
        self.type_dict = {}

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


# Mapper class *NOW WITH COMMENTS*
#-------------------------------------------------------------------------
class Mapper(object):
    def __init__(self):
        self.tilewidth = 0
        self.tileheight = 0
        self.map_list = [
        'maps/start.json',
        'maps/startsecond.json',
        'maps/startthird.json',
        'maps/startteleporter.json']

    def new_inst(self, x):
        open_map = open(self.map_list[x]).read()
        self.mapdict = json.loads(open_map)
        self.layers = self.mapdict["layers"]
        self.tilesets = self.mapdict["tilesets"]
        self.mapheight = self.layers[0]["height"]
        self.mapwidth = self.layers[0]["width"]
        self.tile_id = 1
# this makes everything usable again for when another new_inst is used
    def re_init(self):
        self.all_tiles = None
        self.exitL = None
        self.exitR = None
        self.enemyList = None
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
        return self.all_tiles, self.tileheight, self.tilewidth

# -populates the layers lists and produces collide sprites
    def build_it(self):
        sorter = Sorter()
        # these lists hold all the sprites in the currently rendered room
        self.exitL = []
        self.exitR = []
        self.enemyList = []
        self.collisionList = []
        self.background = []
        self.foreground = []
        tw = self.tilewidth
        th = self.tileheight

        for layer in self.layers:
            collide = False # flag for a collidable sprite
            left = False # flag for the left side room exit tiles
            right = False # flag for the right side exit
            enemy = False # flag for the enemy
            item = False # flag for item in foreground

# every flag produces a different type of sprite and puts that sprite into
# the above empty lists using the layer data gathered below.
            if "properties" in layer:
                properties = layer["properties"]
                if "collision" in properties:
                    collide = True
                elif "exitL" in properties:
                    left = True
                elif "exitR" in properties:
                    right = True
                elif "enemy" in properties:
                    enemy = True
                elif "item" in properties:
                    item = True
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
                    # the solids get a 26x26 rect so the player sinks into them a bit
                            tile = Solid()
                            tile.rect = pygame.Rect(x*tw, y*th, 26, 26)
                            tile.image = self.all_tiles[id_key]
                            self.collisionList.append(tile)
                        if left:
                            L = Exit()
                            L.rect = pygame.Rect(x*tw, y*th, tw, th)
                            L.image = self.all_tiles[id_key]
                            self.exitL.append(L)
                        if right:
                            R = Exit()
                            R.rect = pygame.Rect(x*tw, y*th, tw, th)
                            R.image = self.all_tiles[id_key]
                            self.exitR.append(R)
                        if enemy:
                            print id_key
                            img = self.all_tiles[id_key]
                            en = sorter.gather_data(x*tw, y*th, id_key, img)
                            enem = sorter.sort_type(en)
                            #self.collisionList.append(enem)
                            self.enemyList.append(enem)
                        if item:
                            img = self.all_tiles[id_key]
                            it = sorter.gather_data(x*tw, y*th, id_key, img)
                            item = sorter.sort_type(it)
                            self.collisionList.append(item)
                            #self.foreground.append(item)
                        tile = Tile()
                        tile.rect = pygame.Rect(x*tw, y*th, tw, th)
                        tile.image = self.all_tiles[id_key]
                        self.background.append(tile)
                    index += 1
        return self.exitL, self.exitR, self.collisionList, self.enemyList, self.background, self.foreground



