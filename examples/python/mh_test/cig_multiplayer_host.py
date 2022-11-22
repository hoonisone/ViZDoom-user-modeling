#!/usr/bin/env python3

#####################################################################
# This script presents how to host a deathmatch game.
#####################################################################

import os
import vizdoom as vzd
from state.vizdoom_state import *
import pandas as pd
import datetime as dt

game = vzd.DoomGame()
game.load_config(os.path.join('../../../scenarios', "deathmatch_multi.cfg"))

game.set_doom_map("map01")  # Limited deathmatch.
game.add_game_args("-host 2 "  
                # This machine will function as a host for a multiplayer game with this many players (including this machine). 
                # It will wait for other machines to connect using the -join parameter and then start the game when everyone is connected.
                "-port 5029 "              # Specifies the port (default is 5029).
                "+viz_connect_timeout 60 " # Specifies the time (in seconds), that the host will wait for other players (default is 60).
                "-deathmatch "             # Deathmatch rules are used for the game.
                "+timelimit 10.0 "         # The game (episode) will end after this many minutes have elapsed.
                "+sv_forcerespawn 1 "      # Players will respawn automatically after they die.
                "+sv_noautoaim 0 "         # Autoaim is disabled for all players.
                "+sv_respawnprotect 1 "    # Players will be invulnerable for two second after spawning.
                "+sv_spawnfarthest 1 "     # Players will be spawned as far as possible from any other players.
                "+sv_nocrouch 1 "          # Disables crouching.
                "+viz_respawn_delay 2 "   # Sets delay between respawns (in seconds, default is 0).
                "+viz_nocheat 0")          # Disables depth and labels buffer and the ability to use commands that could interfere with multiplayer game.

game.add_game_args("+name Host +colorset 0")
game.set_mode(vzd.Mode.ASYNC_SPECTATOR)


LOG_PATH = "play_log.csv"
COLUMNS = ["id", "name", "episode", "agent", "start_time", "end_time", "kill", "dead"]

# log 파일 불러오기 또는 생성
if os.path.isfile(LOG_PATH):
    log_df = pd.read_csv(LOG_PATH, encoding='cp949')
else:
    log_df = pd.DataFrame(columns=COLUMNS)

# id 정보 생성 및 입력
# id = 0 if len(log_df["id"]) == 0 else max(log_df["id"])+1

id = 0
name = input("name: ")
episode = int(input("episode: "))

enemy_list = [
    "defensive",
    "aggressive",
    "aimer",
    "hider",
    "runner",
    "defensive",
    "aggressive",
    "aimer",
    "hider",
    "runner",
]

enemy = enemy_list[episode]

acc_kill = 0
acc_death = 0
kill = 0
death = 0
game.add_game_args("-record player-%d-%d.lmp"%(id, episode))
game.init()
start_time = dt.datetime.now()

while not game.is_episode_finished():
    game.advance_action()
    state = StateAnalyzer(game)
    
    kill = max(kill, state.get_kill_count())
    death = max(death, state.get_death_count())

    if game.is_player_dead():
        acc_kill += kill
        acc_death += death
        kill = death = 0

        game.respawn_player()
acc_kill += kill
acc_death += death

end_time = dt.datetime.now()
eposode_log = [id, name, episode, enemy, start_time, end_time, acc_kill, acc_death]    
log_df.loc[len(log_df)] = eposode_log
game.close()
log_df.to_csv(LOG_PATH, index=False, encoding='cp949')