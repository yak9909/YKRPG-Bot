import json
import os
import yktools
import shutil


class Mob:
    def __init__(self, hp, attack, defence, speed):
        self.hp = {"now": hp, "max": hp}
        self.attack = attack
        self.defence = defence
        self.speed = speed

    def get_hp(self):
        return self.hp

    def get_atk(self):
        return self.attack

    def get_def(self):
        return self.defence

    def get_spd(self):
        return self.speed


class Player:
    def __init__(self, userid):
        self.id = userid
        self.path = f"data/players/{self.id}.json"
        self.data = self.get_data()
        self.status = Mob(self.data["hp"], self.data["attack"], self.data["defence"], self.data["speed"])
        pass

    def create_data(self):
        shutil.copy("data/player.json", self.path)
        return json.load(open(self.path, mode="r+", encoding="utf-8"))

    def get_data(self):
        return json.load(yktools.read_file(self.path)) if os.path.exists(self.path) else self.create_data()
