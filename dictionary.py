# Created by a human
# when:
#8/19/2015
#2:11 PM
#
#
#--------------------------------------------------------------------
class MapDict(object):
    def __init__(self):
        pass

    def new_map(self, tiles): # produces a new map with the number of tiles as an argument
        world = []
        for i in range(0, tiles):
            world.append([])
        return world

    def hash_key(self, world, key):           # given a key this creates a number and
        return hash(key) % len(world)   # converts it to an index for the world's tiles

    def get_tile(self, world, key):         #given a key, finds tile
        tile_id = self.hash_key(world, key)
        return world[tile_id]

# returns index, key and value of a slot in tiles
    def get_slot(self, world, key, default = None):
        tile = self.get_tile(world, key)
        for i, kv, in enumerate(tile):
            k, v = kv
            if key == k:
                return i, k, v

        return -1, key, default

    # gets the value of a tile for a given key
    def get(self, world, key, default=None):
        i,k,v = self.get_slot(world, key, default=default)
        return v

    def set(self, world, key, value):
        tile = self.get_tile(world, key)
        i,k,v = self.get_slot(world, key)
        if i >= 0:
            tile[i] = (key, value) # if the key exists, replace it
        else:
            tile.append((key, value))# otherwise, append to create it

    def remove(self, world, key):
        tile = self.get_tile(world, key)
        for i in xrange(len(tile)):
            k, v = tile[i]
            if key == k:
                del tile[i]
                break

    def world_list(self, world):
        for tile in world:
            if tile:
                for k, v in tile:
                    print k, v

