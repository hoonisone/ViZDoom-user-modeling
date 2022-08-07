#!/usr/bin/env python3

#####################################################################
# This script presents SPECTATOR mode. In SPECTATOR mode you play and
# your agent can learn from it.
# Configuration is loaded from "../../scenarios/<SCENARIO_NAME>.cfg" file.
# 
# To see the scenario description go to "../../scenarios/README.md"
#####################################################################

from argparse import ArgumentParser
import os
from pydoc import ispackage
from time import sleep
from turtle import st
from matplotlib.axis import Tick
import vizdoom as vzd
from PIL import Image
from random import choice
import keyboard
import matplotlib.pyplot as plt
import numpy as np
from vizdoom_object_data import *
from vizdoom_player_action import * 

from draw_map import *

DEFAULT_CONFIG = os.path.join(vzd.scenarios_path, "deathmatch.cfg")

from vizdoom_object_state_analysis import *


list = [(10000 for i in range(2000)) for i in range(2000)]

def IsThereTargetInMySight(state, name):
    for label in state.labels:
        if label.object_name == name:
            return True
    return False

def GetAllObjectIdListInView(state, name):
    id_list = []
    for label in state.labels:
        if label.object_name == name:
            id_list.append(label.object_id)
    return id_list

def GetClosestObjectId(state, id_list):
    min_dist = 1000000
    min_id = None
    # for id in id_list:
    #     if label.object_name == name:
    #         return label.x + label.width/2
    print(state.objects)
    return None


def OrganizeObjectInfor(objects):
    dict = {}
    for o in state.objects: # 동작 가능 - 존재하는 모든 오브젝트의 정보 반환
        if o.name not in dict:
            dict[o.name] = 0
        dict[o.name] += 1
    return dict

###############################################

action1 = make_action({
    PlayerAction.Atack:False,
    PlayerAction.rotateX: 5
})

action2 = make_action({
    PlayerAction.Atack:True,
    PlayerAction.rotateX: 5
})

action3 = make_action({
    PlayerAction.Atack:True,
    PlayerAction.MoveFront:True,
    PlayerAction.rotateX: 3
})

action4 = make_action({
    PlayerAction.Atack:True,
    PlayerAction.MoveFront:True,
    PlayerAction.rotateX: -3
})



if __name__ == "__main__":
    parser = ArgumentParser("ViZDoom example showing how to use SPECTATOR mode.")
    parser.add_argument(dest="config",
                        default=DEFAULT_CONFIG,
                        nargs="?",
                        help="Path to the configuration file of the scenario."
                             " Please see "
                             "../../scenarios/*cfg for more scenarios.")
    args = parser.parse_args()
    game = vzd.DoomGame()

    # Choose scenario config file you wish to watch.
    # Don't load two configs cause the second will overrite the first one.
    # Multiple config files are ok but combining these ones doesn't make much sense.

    game.load_config(args.config)

    # Enables freelook in engine
    game.add_game_args("+freelook 1")

    game.set_screen_resolution(vzd.ScreenResolution.RES_1920X1080)
    # Enables spectator mode, so you can play. Sounds strange but it is the agent who is supposed to watch not you.
    game.set_window_visible(True)
    


    game.set_objects_info_enabled(True)
    game.set_sectors_info_enabled(True)
    game.set_labels_buffer_enabled(True)

    game.clear_available_game_variables()
    game.add_available_game_variable(vzd.GameVariable.POSITION_X)
    game.add_available_game_variable(vzd.GameVariable.POSITION_Y)
    game.add_available_game_variable(vzd.GameVariable.POSITION_Z)

    # game.set_mode(vzd.Mode.SPECTATOR) # 동작을 직접 넣을 거면 실행 x

    actions = [[True, False, False], [False, True, False], [False, False, True]]

    game.init()

    game.new_episode()





    state = game.get_state()
    # get_map(state).show()
    
    map = np.ones(shape=(2000, 2000))*10000
    access = np.ones(shape=(2000, 2000))*255

    for s in state.sectors:
        for l in s.lines:
            if l.is_blocking:
                draw_wall(access, (500, 500), l.x1, l.y1, l.x2, l.y2)

    access = max_pooling(access)
    access = max_pooling(access)
    access = max_pooling(access)
    # print(access.shape)

    # pil_image=Image.fromarray(access)
    # pil_image.show()

    map = make_direction_map(access, ((500+1200)//8, (500+500)//8))

    # pil_image=Image.fromarray(map)
    # pil_image.show()
    

    while not game.is_episode_finished():
        state = game.get_state()
        game.advance_action() # 이거 있어야 조작 가능
        stateData = StateData(state)        

        x = int((500 + stateData.player.pos[0])//8)
        y = int((500 + stateData.player.pos[1])//8)

        game.make_action(make_action({}))
        print("angle", stateData.player.object.angle)
        print(math.fabs(math.fabs(stateData.player.object.angle-180)-180))
        if math.fabs(math.fabs(stateData.player.object.angle-180)-180) > 0.5:
            if stateData.player.object.angle  < 0.3:
                game.make_action(make_action({
                PlayerAction.rotateX: 0.1
                }))
            elif stateData.player.object.angle  < 1:
                game.make_action(make_action({
                PlayerAction.rotateX: 0.3
                }))
            elif stateData.player.object.angle  < 5:
                game.make_action(make_action({
                PlayerAction.rotateX: 0.8
                }))
            elif stateData.player.object.angle  < 30:
                game.make_action(make_action({
                PlayerAction.rotateX: 3
                }))
            elif stateData.player.object.angle  < 180:
                game.make_action(make_action({
                PlayerAction.rotateX: 10
                }))
            elif stateData.player.object.angle  > 359.7:
                game.make_action(make_action({
                PlayerAction.rotateX: -0.1
                }))
            elif stateData.player.object.angle  > 359:
                game.make_action(make_action({
                PlayerAction.rotateX: -0.3
                }))
            elif stateData.player.object.angle  > 355:
                game.make_action(make_action({
                PlayerAction.rotateX: -0.8
                }))
            elif stateData.player.object.angle  > 330:
                game.make_action(make_action({
                PlayerAction.rotateX: -3
                }))
            else:
                game.make_action(make_action({
                PlayerAction.rotateX: -10
                }))
        else:
            game.make_action(make_action({
                # PlayerAction.Atack:True,
                PlayerAction.MoveLeft: (map[y+1,x] < map[y,x]),
                PlayerAction.MoveRight: (map[y-1,x] < map[y,x]),
                PlayerAction.MoveBack: (map[y,x-1] < map[y,x]),
                PlayerAction.MoveFront: (map[y,x+1] < map[y,x]),
            }))
        print(stateData.player.pos)
        objects = stateData.get_object_date_list(visible=True)
        objects = extract_enemy(objects)
        target = get_closest_object(objects)

        print(map[y, x+1], map[y, x-1], map[y+1, x], map[y, x], map[y-1, x])
        # if (target == None):
        #     r = game.make_action(action1)
        #     # r = game.make_action([False, False, False, False, False, False, False, True, False, False])   
        # else:
        #     print("Target: %s"% target.name)
        #     game.make_action(make_action({
        #         PlayerAction.Atack:True,
        #         # PlayerAction.MoveFront:True,
        #         PlayerAction.rotateX: 55 * get_pos_x(target, stateData.player)/(1920/2),
        #         PlayerAction.MoveRight : True,
        #         PlayerAction.Run: True,
        #         PlayerAction.MoveBack : True
        #     }))
        #     print(55 * get_pos_x(target, stateData.player)/(1920/2))
            
            # if is_in_shot_range(target, stateData.player):
            #     r = game.make_action(action2)
            # elif is_right(target, stateData.player):
            #     r = game.make_action(action3)
            # elif is_left(target, stateData.player):
            #     r = game.make_action(action4)

        # print(game.get_last_action())             
        # game.make_action(make_action({
        #     # PlayerAction.Atack:True,
        #     # PlayerAction.MoveFront:True,
        #     PlayerAction.rotateX: 0
        # }))




        if keyboard.is_pressed("Enter"):    
            print("State: %s" % str(state.number))

            get_map(state).show()



            # game.make_action(make_action({
            #     # PlayerAction.Atack:True,
            #     # PlayerAction.MoveFront:True,
            #     PlayerAction.rotateX: 55 * get_pos_x(target, stateData.player)/(1920/2)
            # }))



            # objects = stateData.get_object_date_list(type = ObjectName.Medikit , visible=True)
            # pos_list = []
            # for o in objects:
            #     pos_list.append(o.type)
            # print(len(objects))

            
            
            # print("Total: %d" % len(state.objects))

            # dictInfor = OrganizeObjectInfor(state.objects)
            
            # print(dictInfor)    
            

            #print(IsThereTargetInMySight(state, "Medikit"))
            # print(GetAllObjectIdListInView(state, "Medikit"))

            # all_visible_id = getAllIdByName(state, "Medikit", onlyVisable=True)
            # print(len(all_visible_id))
            # if len(all_visible_id) != 0:
            #     all_visible_obj = getAllObjectsByIdList(state, all_visible_id)
            #     closest_object = getClosestObject(getPos(getPlayer(state)), all_visible_obj)
            #     print(getPos(closest_object))


            # palyer = GetPlayer(state)
            # target_id_list = GetAllIdByName(state, "Medikit")
            # if len(target_id_list) != 0:
            #     target_object = GetObjectById(state, target_id_list[0])
            #     dist = Square_dist(GetPos(player), GetPos(target_object))
            #     print(dist)


            # print sector infor
            # for s in state.sectors:

            #     for l in s.lines:
            #         if l.is_blocking:
            #             plt.plot([l.x1, l.x2], [l.y1, l.y2], color='black', linewidth=2)
                
            #     break

            # # Show map
            # plt.show()

            while keyboard.is_pressed("Enter"):
                continue
        

    game.close()


"""
[objects]
맵에 존재하는 모든 오브젝트의 정보를 얻을 수 있다.
아이템, 적 모두 나옴 (메인 캐릭터 포함)
아이템을 먹거나 적이 생기면 그만큼 줄어들고 늘어나는 것 확인
정보가 정확한지는 굳이 테스트 안함

[sector]
맵의 영역과 바닥과 천장의 높이 값 알 수 있음
영역을 두 좌표를 잇는 선의 집합으로 표현
좌표가 실제 위치 좌표임 => 오브젝트 위치를 좌표 그대로 찍으면 표시 가능
"""