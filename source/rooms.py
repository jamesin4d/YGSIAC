# Created by a human
# when:
# 9/7/2015
# 8:06 AM
# WHY DIDN'T I REALIZE THIS SOONER?!?!
# Such a simple fix to a problem that's been bothering me since I
# started this fucking game!
#--------------------------------------------------------------------
from enemies import *
from items import *

# Generic parent class for a Room
class Room:
    map_file = None # has a map_file attribute
    enemy_list = None # enemy_list attribute
    item_list = None # item_list attribute
    def __init__(self):
        self.enemy_list = []
        self.item_list = []

# Name each specific room something unique, these generic names are
# for testing purposes
class RoomOne(Room):
    def __init__(self):
        Room.__init__(self) # call parent class
        self.map_file = 'maps/roomone.json' # give this room a map_file
        # then array out Enemies and Items
        # [0] = type of enemy/item
        # [1] = rect.x position
        # [2] = rect.y position
        enemies = [
            [Security(), 500, 100]
        ]
        # for each arrayed item:
        for e in enemies:
            enemy = e[0]
            enemy.set_position(e[1],e[2])
            self.enemy_list.append(enemy) # add it to the list

class RoomTwo(Room):
    def __init__(self):
        Room.__init__(self)
        self.map_file = "maps/roomtwo.json"

        enemies = [
            [Security(), 300, 200],
            [Blob(), 500, 300]
        ]
        # for each arrayed item:
        for e in enemies:
            enemy = e[0]
            enemy.set_position(e[1],e[2])
            self.enemy_list.append(enemy)

class RoomThree(Room):
    def __init__(self):
        Room.__init__(self)
        self.map_file = "maps/roomthree.json"

class RoomFour(Room):
    def __init__(self):
        Room.__init__(self)
        self.map_file = "maps/roomfour.json"

class RoomFive(Room):
    def __init__(self):
        Room.__init__(self)
        self.map_file = "maps/roomfive.json"