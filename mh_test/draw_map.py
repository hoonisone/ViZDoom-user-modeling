from multiprocessing import pool
from os import access
from tkinter.messagebox import NO
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

class AccessMap:

    adjust_pos = (500, 500)
    pooling = (8, 8)
    map = None

    def __init__(self, state):
        self.map = np.ones(shape=(2000, 2000))*255

        for s in state.sectors:
            for l in s.lines:
                if l.is_blocking:
                    draw_wall(self.map, self.adjust_pos, l.x1, l.y1, l.x2, l.y2)

        self.map = max_pooling(self.map)
        self.map = max_pooling(self.map)
        self.map = max_pooling(self.map)

        for y in range(self.map.shape[0]):
            for x in range(self.map.shape[1]):
                if self.map[y, x] == 0:
                    for a in range(-1, 2, 1):
                        for b in range(-1, 2, 1):
                            if (0 <= x+b) and (x+b < self.map.shape[1]) and (0 <= y+a) and (y+a < self.map.shape[0]):
                                self.map[y+a, x+b] = -1

        for y in range(self.map.shape[0]):
            for x in range(self.map.shape[1]):
                if self.map[y, x] == -1:
                    self.map[y, x] = 0


        self.map = self.map

    def show(self):
        pil_image=Image.fromarray(self.map)
        pil_image.show()

class DirectionMap:

    map = None
    adjust_pos = None
    pooling = None

    def __init__(self, access_map, target_pos):

        self.adjust_pos = access_map.adjust_pos
        self.pooling = access_map.pooling
        self.map = np.ones(shape=access_map.map.shape)*10000
        

        work_list = []
        target_x = (target_pos[0]+self.adjust_pos[0])//self.pooling[0]
        target_y = (target_pos[1]+self.adjust_pos[1])//self.pooling[1]
        work_list.append((target_x, target_y, 1))
        
        while(len(work_list) != 0):
            x, y, l = work_list[0]
            
            work_list.pop(0)
            if not ((0 <= x and x < self.map.shape[0]) and (0 <= y and y <self.map.shape[1])):
                continue
            elif access_map.map[y, x] == 0:
                continue
            elif self.map[y, x] <= l:
                continue
            else:
                self.map[y, x] = l
                work_list.append((x+1, y, l+3))
                work_list.append((x-1, y, l+3))
                work_list.append((x, y+1, l+3))
                work_list.append((x, y-1, l+3))

    def __getitem__(self, pos):
        x = (pos[1]+self.adjust_pos[0])//self.pooling[0]
        y = (pos[0]+self.adjust_pos[1])//self.pooling[1]
        d_x = (pos[1]+self.adjust_pos[0])%self.pooling[0]
        d_y = (pos[0]+self.adjust_pos[1])%self.pooling[1]


        dx = (self.map[y, x+1] - self.map[y, x])*(d_x/self.pooling[1])
        dy = (self.map[y+1, x] - self.map[y, x])*(d_y/self.pooling[0])
        # dx = 0
        # dy = 0


        return self.map[y, x] + dx + dy

    def show(self):
        pil_image=Image.fromarray(self.map)
        pil_image.show()

    