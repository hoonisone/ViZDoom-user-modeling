# 플레이어의 log 데이터에서 전체 오브젝트들의 움직임을 plt로 그려줌

import json
import time
import matplotlib as plt
import matplotlib.pyplot as plt
import json
from time import *
from vizdoom_enum.vizdoom_object_name import *

MAP_FILE_NAME = "deathmatch_map_sector.json"
LOG_FILE_NAME = "log.json"

with open(MAP_FILE_NAME, "r") as f:
    map_data = json.load(f)

with open(LOG_FILE_NAME, "r") as f:
    data = json.load(f)

label_name_list = {
    "Player":player_name_list, 
    "Enemy":enemy_name_list,
    "Armor":armor_name_list,
    "Heal":heal_name_list,
    "Weapon":weapon_name_list,
    "Ammo":ammo_name_list,
    "Particle":particle_name_list
}
label_color = {
    "Player":"blue", 
    "Enemy":"red",
    "Armor":"green",
    "Heal":"green",
    "Weapon":"black",
    "Ammo":"black",
    "Particle":"orange"
}
label_marker = {
    "Player":"o", 
    "Enemy":"o",
    "Armor":"*",
    "Heal":"+",
    "Weapon":"D",
    "Ammo":".",
    "Particle":"x"
}

for frame in data:

    # 맵 그리기
    for s in map_data:
        if s == []: continue
        for l in s:
            if l == []: continue
            plt.plot(l[:2], l[2:], color='black', linewidth=2)

    # object 좌표 수집
    label_point_list = {
        "Player":[[], []], 
        "Enemy":[[], []],
        "Armor":[[], []],
        "Heal":[[], []],
        "Weapon":[[], []],
        "Ammo":[[], []],
        "Particle":[[], []]
    }
    for o in frame["objects"]:
        for label in label_list:
            if o["name"] in label_name_list[label]:
                label_point_list[label][0].append(o["lx"])
                label_point_list[label][1].append(o["ly"])
                break

    for label in label_list:
        print(label_point_list[label])
        plt.plot(label_point_list[label][0], label_point_list[label][1], color=label_color[label], marker = label_marker[label], linewidth=0)

    # pos_list = [[], [], []] # 나, 적, 아이템
    # for o in frame["objects"]:
    #     if o["name"] == "DoomPlayer":
    #         pos_list[0].append([o["lx"], o["ly"]])
    #     elif o["name"] in enemy_name_list:
    #         pos_list[1].append([o["lx"], o["ly"]])
    #     else:
    #         pos_list[2].append([o["lx"], o["ly"]])

    # colors = ["green", "red", "blue"]
    # for i in range(3):
    #     for pos in pos_list[i]:
    #         plt.plot(pos[0], pos[1], color=colors[i], marker='o')

    plt.draw()
    plt.pause(0.02)
    plt.cla()

    # for s in sectors:
    #     if s == []: continue
    #     for l in s:
    #         if l == []: continue
    #         plt.plot(l[:2], l[2:], color='black', linewidth=2)

# if time() - t > 0:
#     t = time()
#     pos_list = [[], []]
#     for o in state.objects:


    



