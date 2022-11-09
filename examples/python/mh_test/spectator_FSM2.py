#!/usr/bin/env python3

#####################################################################
# This script presents SPECTATOR mode. In SPECTATOR mode you play and
# your agent can learn from it.
# Configuration is loaded from "../../scenarios/<SCENARIO_NAME>.cfg" file.
# 
# To see the scenario description go to "../../scenarios/README.md"
#####################################################################

from argparse import ArgumentParser
from gc import is_finalized
from inspect import modulesbyfile
from msilib.schema import MoveFile
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
import cv2
from ai_agent import *

from draw_map import *

# scenarios_path = '../../../scenarios'
# game.load_config(os.path.join(scenarios_path, "deathmatch_multi.cfg"))

# DEFAULT_CONFIG = os.path.join(vzd.scenarios_path, "deathmatch.cfg")
DEFAULT_CONFIG = os.path.join('../../../scenarios', "deathmatch.cfg")

from vizdoom_object_state_analysis import *


list = [(10000 for i in range(2000)) for i in range(2000)]



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

    # game.set_screen_resolution(vzd.ScreenResolution.RES_1920X1080)
    game.set_screen_resolution(vzd.ScreenResolution.RES_640X480)
    
    # Enables spectator mode, so you can play. Sounds strange but it is the agent who is supposed to watch not you.
    game.set_window_visible(True)

    game.set_objects_info_enabled(True)
    game.set_sectors_info_enabled(True)
    game.set_labels_buffer_enabled(True)
    game.set_automap_buffer_enabled(True)
    game.set_depth_buffer_enabled(True)

    # game.add_available_game_variable(vzd.GameVariable.POSITION_X)
    # game.add_available_game_variable(vzd.GameVariable.POSITION_Y)
    # game.add_available_game_variable(vzd.GameVariable.POSITION_Z)

    # game.set_mode(vzd.Mode.SPECTATOR) # 동작을 직접 넣을 거면 실행 x

    game.init()
    game.new_episode()
    agent = Agent(game)

    while not game.is_episode_finished():   
        print(StateData2(game.get_state()).get_weapon_possess())
        print(StateData2(game.get_state()).get_weapon_ammo())
        agent.do_action()
        # empty = AbstractActioner.make_empty_action_order_sheet()
        # empty[PlayerAction.weapone6] = 1
        # empty = AbstractActioner.make_into_doom_action(empty)
        # game.make_action(empty)

        # empty = AbstractActioner.make_empty_action_order_sheet()
        # actioner.add_action(stateData, empty)
        # game.make_action(AbstractActioner.make_into_doom_action(empty)) 
        # name = ["Top", "Right", "Cector", "Right", "botton", "left", "centor", "left"]
        # print(name[actioner.idx], actioner.is_finished(stateData))
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