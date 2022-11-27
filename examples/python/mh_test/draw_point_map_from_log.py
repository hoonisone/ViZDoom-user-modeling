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

for frame in data:

    # 맵 그리기
    for s in map_data:
        if s == []: continue
        for l in s:
            if l == []: continue
            plt.plot(l[:2], l[2:], color='black', linewidth=2)

    # object 좌표 수집
    pos_list = [[], [], []] # 나, 적, 아이템
    for o in frame["objects"]:
        if o["name"] == "DoomPlayer":
            pos_list[0].append([o["lx"], o["ly"]])
        elif o["name"] in enemy_name_list:
            pos_list[1].append([o["lx"], o["ly"]])
        else:
            pos_list[2].append([o["lx"], o["ly"]])

    colors = ["green", "red", "blue"]
    for i in range(3):
        for pos in pos_list[i]:
            plt.plot(pos[0], pos[1], color=colors[i], marker='o')

    plt.draw()
    plt.pause(0.001)
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


    



