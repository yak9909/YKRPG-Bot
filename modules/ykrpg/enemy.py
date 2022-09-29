import random
from .entity import *


class Enemy(Entity):
    def __init__(self, name):
        super().__init__()
        
        self.name = name
        
        self.health = [40, 40]
        self.attack = 8
        self.defence = 0
        self.speed = 0

