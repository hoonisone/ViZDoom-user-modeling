from enum import Enum
from typing import ClassVar

label_list = ["Player", "Enemy", "Armor", "Heal", "Weapon", "Ammo", "Particle"]


player_name_list = ["DoomPlayer"]
enemy_name_list = ["Demon", "Zombieman", "ChaingunGuy", "ShotgunGuy", "HellKnight", "MarineChainsawVzd"]
armor_name_list = ["BlueArmor", "GreenArmor", "ArmorBonus"] 
heal_name_list = ["Medikit", "HealthBonus", "Stimpack"]
weapon_name_list = ["SuperShotgun", "PlasmaRifle", "RocketLauncher", "Chainsaw", "Chaingun"]
ammo_name_list = ["CellPack", "RocketBox", "ShellBox", "ClipBox"]
particle_name_list = ["BulletPuff", "PlasmaBall", "Rocket", "BaronBall"]

object_name_dict = {}
object_name_dict["BlueArmor"] = 1
object_name_dict["Medikit"] = 2
object_name_dict["DoomPlayer"] = 3
object_name_dict["TeleportFog"] = 4
object_name_dict["HellKnight"] = 5              # 겁나 쎈 프레데터(플라즈마 쏨)
object_name_dict["SuperShotgun"] = 6
object_name_dict["MarineChainsawVzd"] = 7
object_name_dict["CellPack"] = 8
object_name_dict["Demon"] = 9                   # 분홍 지렁이
object_name_dict["GreenArmor"] = 10
object_name_dict["PlasmaRifle"] = 11
object_name_dict["BaronBall"] = 12
object_name_dict["RocketBox"] = 13
object_name_dict["ChaingunGuy"] = 14
object_name_dict["ShotgunGuy"] = 15
object_name_dict["RocketLauncher"] = 16
object_name_dict["Chainsaw"] = 17
object_name_dict["ArmorBonus"] = 18
object_name_dict["HealthBonus"] = 19
object_name_dict["Zombieman"] = 20
object_name_dict["Chaingun"] = 21
object_name_dict["Stimpack"] = 22
object_name_dict["ShellBox"] = 23
object_name_dict["ClipBox"] = 24
object_name_dict["BulletPuff"] = 25
object_name_dict["PlasmaBall"] = 26
object_name_dict["Blood"] = 26
object_name_dict["Rocket"] = 27



class DoomObject(Enum):
    BlueArmor = 1
    Medikit = 2
    DoomPlayer = 3
    TeleportFog = 4
    HellKnight = 5
    SuperShotgun = 6
    MarineChainsawVzd = 7
    CellPack = 8
    Demon = 9
    GreenArmor = 10
    PlasmaRifle = 11
    BaronBall = 12
    RocketBox = 13
    ChaingunGuy = 14
    ShotgunGuy = 15
    RocketLauncher = 16
    Chainsaw = 17
    ArmorBonus = 18
    HealthBonus = 19
    Zombieman = 20
    Chaingun = 21
    Stimpack = 22
    ShellBox = 23
    ClipBox = 24
    BulletPuff = 25
    PlasmaBall = 26
    Blood = 26
    Rocket = 27

    

    @classmethod
    def ToEnum(self, str_val):
        return DoomObject(object_name_dict[str_val])

#     def is_enemy(self):
#         print(self.value)
#         print(self.enemy_name_list[0])
#         # return self.value in self.enemy_name_list

# print(DoomObject.enemy_name_list[0])
# print(DoomObject(1).is_enemy())