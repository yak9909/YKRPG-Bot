import random
import asyncio


class Entity:
    def __init__(self, health=0, attack=0, defence=0, speed=0):
        self.health = [health, health]
        self.attack = attack
        self.defence = defence
        self.speed = speed
        
        self.alive = True
        self.guard = 0
        self.command = None
    
    def receive(self, damage):
        damage_adjust = round(max(1, damage - self.defence*(1.35 if self.guard > 0 else 1)))
        self.health[0] = max(0, self.health[0] - damage_adjust)
        
        if self.health[0] <= 0:
            self.alive = False
        
        return self.alive
    
    def attack_to(self, obj):
        damage = self.damage_calc()
        obj.receive(damage)
        return damage
    
    def skill_to(self, obj):
        pass
    
    def use_item(self, item):
        pass
    
    def guard(self, turn):
        self.guard = turn
    
    def damage_calc(self):
        damage_min = max(1, round(self.attack/1.2))
        damage_max = self.attack
        damage = random.randint(damage_min, damage_max)

        return damage
