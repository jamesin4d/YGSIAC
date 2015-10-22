# Created by a human
# when:
#10/10/2015
#5:38 AM
#
#
#--------------------------------------------------------------------


import json

# this small method is just a hook to dump the obj's attributes into a dictionary
def jdefault(obj): # the dictionary is then dumped onto a .json
    return obj.__dict__ # returns dick

class Save(object):
    def __init__(self, health, room, location, ammo):
        self.health = health
        self.room = room
        self.room_location = location
        self.ammunition = ammo

    def load_progress(self, player):
        save_file = open('player.json').read()
        opened_save = json.loads(save_file)
        if 'ammunition' in opened_save:
            ammo = opened_save['ammunition']
            self.ammunition = ammo
        if 'health' in opened_save:
            health = opened_save['health']
            self.health = health
        if 'current_location' in opened_save:
            current_location = opened_save['current_location']
            player.set_position((current_location[0], current_location[1]))

    def save_progress(self):
        with open('player.json','w') as outfile:
            json.dump(self, default=jdefault, fp=outfile,indent=4)