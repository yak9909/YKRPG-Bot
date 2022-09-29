import random
from .entity import *


class Player(Entity):
    def __init__(self, playerid):
        super().__init__()
        
        self.id = playerid
        
        self.health = [100, 100]
        self.attack = 15
        self.defence = 0
        self.speed = 0

