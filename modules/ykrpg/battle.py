from .command import *
from .player import *
from .enemy import *
from .entity import *
import copy


class Battle:
    def __init__(self, playerid, enemy_kazu=1):
        self.players = {str(playerid): {"obj": Player(playerid), "total_damage": 0}}
        self.enemies = [self.enemy_chooser(f'敵{i+1}') for i in range(enemy_kazu)]
    
    def attack(self, playerid, enemy_index):
    
        if not (player := self.players.get(str(playerid))):
            self.players[str(playerid)] = {"obj": Player(playerid), "total_damage": 0}
            player = self.players[str(playerid)]
    
        try:
            target = self.enemies[enemy_index]
        except IndexError:
            print("IndexError")
            return None
        
        if not player["obj"].alive:
            return None
    
        player_damage = player["obj"].attack_to(target)
        player["total_damage"] += player_damage
        
        enemy_damages = []
        killer = None
        for e in self.enemies:
            if e.alive:
                enemy_damage = e.attack_to(player["obj"])
                enemy_damages.append([e, enemy_damage])
                if not player["obj"].alive:
                    killer = e
                    break

        result = self.turn_end(playerid)
        return {"damage": {"attack": player_damage, "receive": enemy_damages}, "obj": {"attacker": player["obj"], "victim": target}, "killer": killer, "kill": not target.alive, "result": result}
    
    def guard(self, playerid):
        if not (player := self.players.get(str(playerid))):
            self.players[str(playerid)] = {"obj": Player(playerid), "total_damage": 0}
            player = self.players[str(playerid)]
        
        player.guard(1)
        enemy_damages = [[e.attack_to(player["obj"]), e] for e in self.enemies]
        
        result = self.turn_end(playerid)
        return {"damage": {"attack": 0, "receive": enemy_damages}, "obj": player, "dead": player["obj"].alive, "result": result}
    
    def turn_end(self, playerid):
        guard = self.players[str(playerid)]["obj"].guard
        self.players[str(playerid)]["obj"].guard = max(0, guard - 1)
    
        for e in self.enemies:
            if e.alive:
                return False
        else:
            return True
    
    def gameover(self):
        pass
    
    def enemy_chooser(self, name):
        return Enemy(name)
    