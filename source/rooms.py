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
from mapper import *
from camera import *

# Generic parent class for a Room
class Room:
    map_file = None # has a map_file attribute
    map_dictionary = None
    map_rect = None
    collision = None
    background = None
    foreground = None
    tileheight = None
    tilewidth = None
    enemy_list = None # enemy_list attribute
    item_list = None # item_list attribute

    player_pos_left = None
    player_pos_right = None
    player = None

    camera = None
    next_room = None
    previous_room = None
    goto_previous = False
    goto_next = False
    def __init__(self):
        self.enemy_list = []
        self.item_list = []
        self.player_pos_left = ()
        self.player_pos_right = ()
        self.screen = pygame.display.get_surface()

    def get_map_info(self):
        self.map_dictionary = quickmap(self.map_file)
        md = self.map_dictionary
        self.map_rect = md["map_rect"]
        self.collision = md['collision']
        self.background = md['background']
        self.foreground = md['foreground']
        self.tileheight = md['tileheight']
        self.tilewidth = md['tilewidth']
        self.camera = Camera(complex_camera, self.map_rect)
        
    def check_collisions(self):
        self.camera.update(self.player)
        self.player.update(self.collision)
        for e in self.enemy_list:
            e.update(self.collision)
        for i in self.item_list:
            i.update(self.collision)
            if i.dead:self.item_list.remove(i)



        if self.player.rect.x > self.map_rect[0]:
            self.goto_next_room()
        if self.player.rect.x < 0:
            self.goto_previous_room()

    def update_screen(self):
        for b in self.background:
            self.screen.blit(b.image, self.camera.apply(b))
        for f in self.foreground:
            self.screen.blit(f.image, self.camera.apply(f))
        for c in self.collision:
            self.screen.blit(c.image, self.camera.apply(c))
        for i in self.item_list:
            self.screen.blit(i.image, self.camera.apply(i))
        for e in self.enemy_list:
            self.screen.blit(e.image, self.camera.apply(e))

        if not self.player.knife_attack.finished:
            self.screen.blit(self.player.knife_attack.image, self.camera.apply(self.player.knife_attack))

        self.screen.blit(self.player.image, self.camera.apply(self.player))
        self.screen.blit(self.player.friend.image, self.camera.apply(self.player.friend))


    def goto_next_room(self):
        self.goto_next = True
        self.screen.fill((0,0,0))
        return self.next_room
    def goto_previous_room(self):
        self.goto_previous = True
        self.screen.fill((0,0,0))
        return self.previous_room


# Name each specific room something unique, these generic names are
# for testing purposes
class StartRoom(Room):
    def __init__(self):
        Room.__init__(self) # call parent class

        self.map_file = 'maps/testlevel.json'
        self.get_map_info()
        self.player_pos_left = (80,16)
        self.player_pos_right = (36*self.tilewidth, 16*self.tileheight)

