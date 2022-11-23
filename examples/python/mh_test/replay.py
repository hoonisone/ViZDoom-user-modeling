#!/usr/bin/env python3

#####################################################################
# This script presents how to use Doom's native demo mechanism to
# replay episodes with perfect accuracy.
#####################################################################

import os
from random import choice
import vizdoom as vzd
import matplotlib as plt
import matplotlib.pyplot as plt
import json

import threading
from time import *
from IPython import display
from multiprocessing import Process, Value, Queue
import multiprocessing

# manager = multiprocessing.Manager()
# pos_list = manager.list()

# pos_list.append([])
# pos_list.append([])

def draw(q, sectors):
    t = 0
    while True:
        if time()-t < 0.03:
            continue
        t = time()

        
        q.put("exit")
        flag = False
        while True:

            item = q.get()
            if item == None:
                flag = True
                break
            elif item == "exit":
                break
            else:
                data = item

        if flag == True:
            continue

        print(data)
        pos_list = json.loads(data)

        for s in sectors:
            if s == []: continue
            for l in s:
                if l == []: continue
                plt.plot(l[:2], l[2:], color='black', linewidth=2)


        for pos in pos_list[0]:
            plt.plot(pos[0], pos[1], color='green', marker='o')
        for pos in pos_list[1]:
            plt.plot(pos[0], pos[1], color='red', marker='o')

        plt.draw()
        plt.pause(0.001)
        plt.cla()

if __name__ == '__main__':
    q = Queue()
    game = vzd.DoomGame()

    # New render settings for replay
    game.set_screen_resolution(vzd.ScreenResolution.RES_800X600)
    game.set_render_hud(True)

    game.set_mode(vzd.Mode.SPECTATOR)
    game.load_config(os.path.join('../../../scenarios', "deathmatch.cfg"))
    game.set_screen_resolution(vzd.ScreenResolution.RES_640X480)
    game.set_window_visible(True)
    game.set_objects_info_enabled(True)
    game.set_sectors_info_enabled(True)
    game.set_labels_buffer_enabled(True)
    game.init()
    # Replays episodes stored in given file. Sending game command will interrupt playback.
    game.replay_episode("agent-aggressive-0.lmp")



    with open("deathmatch_map_sector.json", "r") as st_json:
        sectors = json.load(st_json)


    # t = threading.Thread(target = draw, args=(p, game, sectors))
    # t.daemon = True
    # t.start()

    manager = multiprocessing.Manager()
    data = manager.dict()
    

    # p = Process(target = draw, args=(q, sectors, ))
    # p.daemon = True
    # p.start()
    
    sleep(1)

    t = 0
    while not game.is_episode_finished():
        state = game.get_state()
        game.advance_action()

        if time() - t > 0:
            t = time()
            pos_list = [[], []]
            for o in state.objects:

                # Plot object on map
                if o.name == "DoomPlayer":
                    pos_list[0].append([o.position_x, o.position_y])
                    # plt.plot(o.position_x, o.position_y, color='green', marker='o')
                else:
                    pos_list[1].append([o.position_x, o.position_y])
                    # plt.plot(o.position_x, o.position_y, color='red', marker='o')
            
            for s in sectors:
                if s == []: continue
                for l in s:
                    if l == []: continue
                    plt.plot(l[:2], l[2:], color='black', linewidth=2)


            for pos in pos_list[0]:
                plt.plot(pos[0], pos[1], color='green', marker='o')
            for pos in pos_list[1]:
                plt.plot(pos[0], pos[1], color='red', marker='o')

            plt.draw()
            plt.pause(0.001)
            plt.cla()

            data = json.dumps(pos_list)
            q.put(data)

    game.close()
