import os
import vizdoom as vzd
from agent.banlencedAgent import *
from agent.RunnerAgent import *
from agent.HiderAgent import *
import pandas as pd
import datetime as dt
from log.vizdoom_log_util import *
from argparse import ArgumentParser
import os
from time import sleep
import vizdoom as vzd
import keyboard
import json
from time import *
import numpy as np
from datetime import datetime, timedelta

LOG_PATH = "agent_deathmatch_log.csv"
COLUMNS = ["id", "name", "episode", "agent", "start_time", "end_time", "kill", "dead"]

# log 파일 불러오기 또는 생성
if os.path.isfile(LOG_PATH):
    log_df = pd.read_csv(LOG_PATH, encoding='cp949')
else:
    log_df = pd.DataFrame(columns=COLUMNS)

# id 정보 생성 및 입력
# id = 0 if len(log_df["id"]) == 0 else max(log_df["id"])+1

agent_generator_list = [
    lambda : DefensiveAgent(game),
    lambda : AggressiveAgent(game),
    lambda : AimerAgent(game),
    lambda : HiderAgent(game),
    lambda : RunnerAgent(game),
    lambda : DefensiveAgent(game),
    lambda : AggressiveAgent(game),
    lambda : AimerAgent(game),
    lambda : HiderAgent(game),
    lambda : RunnerAgent(game),
]
enemy_list = [
    "defensive",
    "aggressive",
    "aimer",
    "hider",
    "runner"
]


# episode = int(input("episode: "))
name = "enemy"




# start = int(input("start: "))
id = 0
heads = ['time', 'timestamp', 'ATTACK', 'SPEED', 'STRAFE', 'MOVE_RIGHT', 'MOVE_LEFT', 'MOVE_BACKWARD', 'MOVE_FORWARD', 'TURN_RIGHT', 'TURN_LEFT', 'USE', 'SELECT_WEAPON1', 'SELECT_WEAPON2', 'SELECT_WEAPON3', 'SELECT_WEAPON4', 'SELECT_WEAPON5', 'SELECT_WEAPON6', 'SELECT_NEXT_WEAPON', 'SELECT_PREV_WEAPON', 'LOOK_UP_DOWN_DELTA', 'TURN_LEFT_RIGHT_DELTA', 'MOVE_LEFT_RIGHT_DELTA', 'KILLCOUNT', 'HEALTH', 'ARMOR', 'SELECTED_WEAPON', 'SELECTED_WEAPON_AMMO']
episode = int(input("episode"))
for a in range(1):
    for i in range(10, 20):
        log_data = []
        acc_kill = 0
        acc_death = 0
        kill = 0
        death = 0

        enemy = enemy_list[episode]
        print("step: ", id, "agent: ", "enemy")
        t = time()
        start_time = dt.datetime.now()

        game = vzd.DoomGame()
        game.load_config(os.path.join('../../../scenarios', "deathmatch.cfg"))
        game.set_window_visible(True)
        game.set_objects_info_enabled(True)
        game.set_sectors_info_enabled(True)
        game.set_labels_buffer_enabled(True)
        
        game.add_game_args("-record agent-%s-%d.lmp"%(enemy_list[episode], i))
        # game.add_game_args(  
        #             # This machine will function as a host for a multiplayer game with this many players (including this machine). 
        #             # It will wait for other machines to connect using the -join parameter and then start the game when everyone is connected.
        #             "-deathmatch "             # Deathmatch rules are used for the game.
        #             # "+sv_forcerespawn 1 "      # Players will respawn automatically after they die.
        #             "+sv_respawnprotect 1 "    # Players will be invulnerable for two second after spawning.
        #             "+sv_spawnfarthest 1 "     # Players will be spawned as far as possible from any other players.
        #             "+viz_respawn_delay 2 "   # Sets delay between respawns (in seconds, default is 0).
        #             "+viz_nocheat 0")          # Disables depth and labels buffer and the ability to use commands that could interfere with multiplayer game.
        game.init()

        agent = agent_generator_list[episode]()

        while not game.is_episode_finished():
            agent.do_action()
            state = StateAnalyzer(game)
            kill = max(kill, state.get_kill_count())       

            if game.is_player_dead():
                death = 1
                break

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

            print(time()-t)
            if time()-t > 60:
                break


        log_data = json.dumps(log_data)
        with open("log-%s-%d.json"%(enemy_list[episode], i), "w") as f:
            f.write(log_data)
            

        end_time = dt.datetime.now()
        eposode_log = [id, name, episode, enemy, start_time, end_time, kill, death]
        log_df.loc[len(log_df)] = eposode_log
        game.close()
        log_df.to_csv(LOG_PATH, index=False, encoding='cp949')