# 녹화 파일 (lmp)에서 log 데이터를 뽑아줌

import os
import json
import numpy as np
import vizdoom as vzd
import matplotlib as plt
import matplotlib.pyplot as plt

from time import *
from time import sleep
from datetime import datetime, timedelta
from agent.banlencedAgent import *
from agent.RunnerAgent import *
from agent.HiderAgent import *
from log.vizdoom_log_util import *

RECORD_FILE_NAME = "agent-aimer-1.lmp"
LOG_FILE_NAME = "log.json"

heads = ['time', 'timestamp', 'ATTACK', 'SPEED', 'STRAFE', 'MOVE_RIGHT', 'MOVE_LEFT', 'MOVE_BACKWARD', 'MOVE_FORWARD', 'TURN_RIGHT', 'TURN_LEFT', 'USE', 'SELECT_WEAPON1', 'SELECT_WEAPON2', 'SELECT_WEAPON3', 'SELECT_WEAPON4', 'SELECT_WEAPON5', 'SELECT_WEAPON6', 'SELECT_NEXT_WEAPON', 'SELECT_PREV_WEAPON', 'LOOK_UP_DOWN_DELTA', 'TURN_LEFT_RIGHT_DELTA', 'MOVE_LEFT_RIGHT_DELTA', 'KILLCOUNT', 'HEALTH', 'ARMOR', 'SELECTED_WEAPON', 'SELECTED_WEAPON_AMMO']
log_data = []

if __name__ == '__main__':
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
    game.replay_episode(RECORD_FILE_NAME)

    t = 0
    while not game.is_episode_finished():
        game.advance_action()

        state = game.get_state()
        now_time = str(datetime.utcnow() + timedelta(hours=9))
        elp_time = time()-t

        last_action = game.get_last_action()
        variables = state.game_variables
        var = np.concatenate(([now_time], [elp_time], last_action, variables), axis=0)
        basic = {}
        for j, name in enumerate(heads):
            basic[name] = var[j]

        state_data = get_state_log(state)
        state_data["basic"] = basic
        log_data.append(state_data)


    log_data = json.dumps(log_data)
    with open(LOG_FILE_NAME, "w") as f:
        f.write(log_data)

    game.close()
