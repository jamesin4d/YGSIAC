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
    player_pos_left = None
    player_pos_right = None
    def __init__(self):
        self.enemy_list = []
        self.item_list = []
        self.player_pos_left = ()
        self.player_pos_right = ()


# Name each specific room something unique, these generic names are
# for testing purposes
class StartRoom(Room):
    def __init__(self):
        Room.__init__(self) # call parent class
        self.player_pos_left = (75,75)
        self.player_pos_right = (740, 550)
        self.map_file = 'maps/cae.json'
        cell_width = 16
        cell_height = 16
        enemies = [
            [Rat(31*cell_width, 9*cell_height,27*cell_width, 38*cell_width)]

        ]
        items = [
            [Candle(75,152)],
            [Candle(150,152)],
            [Candle(225,152)],
            [Candle(300,152)],
            [Candle(500,100)],
            [Candle(500,250)],
            [Candle(600,300)],
            [Candle(650,544)],
            [Candle(500,544)],
            [Candle(768,544)],

        ]
        # for each arrayed item:
        for e in enemies:
            enemy = e[0]
            self.enemy_list.append(enemy)
        for i in items:
            item = i[0]
            self.item_list.append(item)

class RoomTwoTheCave(Room):
    def __init__(self):
        Room.__init__(self)
        self.map_file = "maps/cave.json"
        self.player_pos_left = (15, 580)
        self.player_pos_right = (776,368)
        enemies = [
        ]

        items = [
            [Candle(80,110)],
            [Candle(200,100)],
            [Candle(345,125)],
            [Candle(500,100)],
            [Candle(450,250)],
            [Candle(600,250)],
            [Candle(650,600)],
            [Candle(50,550)],
            [Candle(150,530)],
            [Candle(200,500)],
            [Candle(275,550)],


        ]

        # for each arrayed item:
        for e in enemies:
            enemy = e[0]
            self.enemy_list.append(enemy)

        for i in items:
            item = i[0]
            self.item_list.append(item)

class ThirdRoom(Room):
    def __init__(self):
        Room.__init__(self)
        self.map_file = "maps/third.json"
        self.player_pos_left = (15, 368)
        enemies = []