from entityKing import *
#"""
# the entities kingdom --
# here lives the innanimate objects of the game world
#
#"""



# mapper class produces a variable equal to: sort_data(return)
def sort_item_data(x, y, id_k, image):
    return x, y, id_k, image

# sort_data is then passed as the 'what' argument here
def sort_item_type(what):
    id_key = what[2] #the id_key is unique for every tile
    if id_key == 82:
        item = PeaShoot()
        item.image = what[3]
        item.rect = pygame.Rect(what[0], what[1], 32, 32)
        return item

#--------------------------------------------------------------------------
class Tile(Master):
    def __init__(self):
        Master.__init__(self)

class Solid(Master):
    def __init__(self):
        Master.__init__(self)

class Exit(Master):
    def __init__(self):
        Master.__init__(self)
#------------------------------------------------------------------------------------------
# the heathen classes, soon they too will bow to Master
#------------------------------------------------------------------------------------------
class Bullet(pygame.sprite.Sprite):
    def __init__(self, loc, angle):
        pygame.sprite.Sprite.__init__(self)
        image = pygame.image.load("img/bullet2.png")
        self.original_image = image
        self.angle = -math.radians(angle-136)
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.image.set_colorkey((255,255,255))
        self.rect = self.image.get_rect(center=loc)
        self.move = [self.rect.x, self.rect.y]
        self.speed_mod = 10
        self.speed = (self.speed_mod*math.cos(self.angle),
                      self.speed_mod*math.sin(self.angle))
        self.done = False

    def update(self):
        self.move[0] += self.speed[0]
        self.move[1] += self.speed[1]
        self.rect.topleft = self.move

    def remove(self, screen_rect):
        if not self.rect.colliderect(screen_rect):
            self.kill()

class Item(Master):
    def __init__(self):
        Master.__init__(self)
#----------------------------------------------------
# player starter weapon
# id_key: 82-----------------------------------------
class PeaShoot(Item):
    id_key = 82
    damage = random.randint(7,10)
    def __init__(self):
        Item.__init__(self)



















