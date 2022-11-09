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
import vizdoom as vzd
from PIL import Image
import keyboard
from vizdoom_object_data import *
from vizdoom_player_action import * 
import cv2
from PIL import Image
# DEFAULT_CONFIG = os.path.join(vzd.scenarios_path, "deathmatch.cfg")
DEFAULT_CONFIG = os.path.join('../../../scenarios', "deathmatch.cfg")

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

    game.set_objects_info_enabled(True)
    game.set_sectors_info_enabled(True)
    game.set_labels_buffer_enabled(True)
    game.set_automap_buffer_enabled(True)




    game.set_screen_resolution(vzd.ScreenResolution.RES_1920X1080)
    # Enables spectator mode, so you can play. Sounds strange but it is the agent who is supposed to watch not you.
    game.set_window_visible(True)

    game.set_mode(vzd.Mode.SPECTATOR)
    
    game.init()

    game.new_episode()

    print()
    # while not game.is_episode_finished():
        # print(StateData2(game.get_state()).get_weapon_possess())
        
        # print(game.get_state().game_variables)
        # game.advance_action() # 이거 있어야 조작 가능
        # pass
    
    accessMap = AccessMap(game, (1, 1))
    # heightMap = HeightMap(accessMap, (660, 1250))
    # print(heightMap.map[190])
    Image.fromarray(accessMap.map*255).show()
    
    
    game.close()



"""
game.get_state().screen_buffer가 현 시점의 
"""
