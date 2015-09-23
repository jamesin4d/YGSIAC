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
        enemies = [
            [Rat(300, 200, 150, 450)],
            [Bat(500,60,250,600)],
            [Rat(300, 450, 300, 700)],
            [Rat(600, 50, 225, 620)],


        ]
        # for each arrayed item:
        for e in enemies:
            enemy = e[0]
            self.enemy_list.append(enemy)



class RoomTwoTheCave(Room):
    def __init__(self):
        Room.__init__(self)
        self.map_file = "maps/cave.json"
        self.player_pos_left = (15, 60)
        enemies = [
            [Security(300, 200, 250, 350)],
        ]
        # for each arrayed item:
        for e in enemies:
            enemy = e[0]

            self.enemy_list.append(enemy)

