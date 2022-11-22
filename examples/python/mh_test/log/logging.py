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
import time
from vizdoom_log_util import *
import numpy as np
from datetime import datetime, timedelta

# DEFAULT_CONFIG = os.path.join(vzd.scenarios_path, "deathmatch.cfg")
# DEFAULT_CONFIG = os.path.join("C:\\Users\\GIST\\Desktop\\Experiment\\Sensor-Experiment\\vizdoom-user-modeling\\scenarios", "deathmatch.cfg")

if __name__ == "__main__":
    parser = ArgumentParser("ViZDoom example showing how to use SPECTATOR mode.")
    parser.add_argument(dest="config",
                        # default=DEFAULT_CONFIG,
                        nargs="?",
                        help="Path to the configuration file of the scenario."
                             " Please see "
                             "../../scenarios/*cfg for more scenarios.")
    parser.add_argument("-n", "--name",
                        dest="name",
                        default=None,
                        type=str)
    args = parser.parse_args()


    # assert args.name is not None, 'name please'
    game = vzd.DoomGame()
    game.load_config(os.path.join('../../../../scenarios', "deathmatch.cfg"))

    # Choose scenario config file you wish to watch.
    # Don't load two configs cause the second will overrite the first one.
    # Multiple config files are ok but combining these ones doesn't make much sense.

    # game.load_config(args.config)

    # Enables freelook in engine
    game.add_game_args("+freelook 1")

    game.set_screen_resolution(vzd.ScreenResolution.RES_1280X720)
    game.set_mode(vzd.Mode.SPECTATOR)

    # Enables spectator mode, so you can play. Sounds strange but it is the agent who is supposed to watch not you.
    game.set_window_visible(True)
    # game.set_mode(vzd.Mode.SPECTATOR)///
    game.set_objects_info_enabled(True)
    game.set_sectors_info_enabled(True)
    game.set_labels_buffer_enabled(True)
    game.set_automap_buffer_enabled(True)


    game.init()
    heads = ['time', 'timestamp', 'ATTACK', 'SPEED', 'STRAFE', 'MOVE_RIGHT', 'MOVE_LEFT', 'MOVE_BACKWARD', 'MOVE_FORWARD', 'TURN_RIGHT', 'TURN_LEFT', 'USE', 'SELECT_WEAPON1', 'SELECT_WEAPON2', 'SELECT_WEAPON3', 'SELECT_WEAPON4', 'SELECT_WEAPON5', 'SELECT_WEAPON6', 'SELECT_NEXT_WEAPON', 'SELECT_PREV_WEAPON', 'LOOK_UP_DOWN_DELTA', 'TURN_LEFT_RIGHT_DELTA', 'MOVE_LEFT_RIGHT_DELTA', 'KILLCOUNT', 'HEALTH', 'ARMOR', 'SELECTED_WEAPON', 'SELECTED_WEAPON_AMMO']

    log_data = []
    image = []

    start_time = time.time()

    episodes = 10

    for i in range(episodes):
        print("Episode #" + str(i + 1))

        game.new_episode()

        while not game.is_episode_finished():
            state = game.get_state()

            last_action = game.get_last_action()
            reward = game.get_last_reward()
            variables = state.game_variables
            now_time = str(datetime.utcnow() + timedelta(hours=9))
            now = time.time()

            elp_time = now - start_time
            var = np.concatenate(([now_time], [elp_time], last_action, variables), axis=0)
            basic = {}
            for i, name in enumerate(heads):
                basic[name] = var[i]

            # image.append(state.screen_buffer)

            state_data = get_state_log(state)
            state_data["basic"] = basic
            log_data.append(state_data)

            game.advance_action()

            if keyboard.is_pressed("Enter"):
                game.close()
                break

        log_data = json.dumps(log_data)
        with open("log.json", "w") as f:
            f.write(log_data)

        print("Episode finished!")
        print("Total reward:", game.get_total_reward())
        print("************************")
        sleep(2.0)

