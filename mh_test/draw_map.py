import numpy as np
import keyboard
from PIL import Image
import matplotlib.pyplot as plt

def draw_wall(map, origin, x1, y1, x2, y2):

    if x1 == x2:
        x = int(origin[0]+x1)
        from_y = int(origin[1] + min(y1, y2))
        to_y   = int(origin[1] + max(y1, y2))
        for y in range(from_y, to_y+1):
            map[y, x] = 0
    else:
        y = int(origin[1]+y1)
        from_x = int(origin[0] + min(x1, x2))
        to_x =   int(origin[0] + max(x1, x2))
        for x in range(from_x, to_x+1):
            map[y, x] = 0


def make_direction_map(access, target):
    map = np.ones(shape=access.shape)*10000

    work_list = []
    work_list.append((target[0], target[1], 1))

    while(len(work_list) != 0):
        x, y, l = work_list[0]
        work_list.pop(0)
        if not ((0 <= x and x < map.shape[0]) and (0 <= y and y <map.shape[1])):
            continue
        elif access[y, x] == 0:
            continue
        elif map[y, x] <= l:
            continue
        else:
            map[y, x] = l
            work_list.append((x+1, y, l+1))
            work_list.append((x-1, y, l+1))
            work_list.append((x, y+1, l+1))
            work_list.append((x, y-1, l+1))

    return map

        

def max_pooling(arr):
    x, y = arr.shape
    new_x, new_y = x//2, y//2
    arr = np.min(arr.reshape(new_x, 2, new_y, 2), axis = (1, 3))
    return arr

def get_map(state):
    for o in state.objects:
        if o.name == "DoomPlayer":
            plt.plot(o.position_x, o.position_y, color='green', marker='o')
        else:
            plt.plot(o.position_x, o.position_y, color='red', marker='o')

    for s in state.sectors:
        for l in s.lines:
            if l.is_blocking:
                plt.plot([l.x1, l.x2], [l.y1, l.y2], color='black', linewidth=2)

    return plt