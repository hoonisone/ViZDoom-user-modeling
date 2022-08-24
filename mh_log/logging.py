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
from time import sleep
import vizdoom as vzd
import keyboard
import json
from vizdoom_log_util import *
DEFAULT_CONFIG = os.path.join(vzd.scenarios_path, "deathmatch.cfg")

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

    game.set_screen_resolution(vzd.ScreenResolution.RES_640X480)
    game.set_mode(vzd.Mode.SPECTATOR)

    # Enables spectator mode, so you can play. Sounds strange but it is the agent who is supposed to watch not you.
    game.set_window_visible(True)
    # game.set_mode(vzd.Mode.SPECTATOR)///
    game.set_objects_info_enabled(True)
    game.set_sectors_info_enabled(True)
    game.set_labels_buffer_enabled(True)
    game.set_automap_buffer_enabled(True)


    game.init()



    game.new_episode()

    log_data = []
    image = []
    while not game.is_episode_finished():
        state = game.get_state()
        # print(type(state.objects[1]))
        # s = json.dumps(state.objects[1])
        
        log_data.append(get_state_log(state))
        # image.append(state.screen_buffer)
        game.advance_action()


        if keyboard.is_pressed("Enter"):
            game.close()
            break
        
    log_data = json.dumps(log_data)
    with open("log.txt", "w") as f:
        f.write(log_data)
    
    print("Episode finished!")
    print("Total reward:", game.get_total_reward())
    print("************************")
    sleep(2.0)

