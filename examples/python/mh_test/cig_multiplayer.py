import os
import vizdoom as vzd
from agent.banlencedAgent import *
from agent.RunnerAgent import *
from agent.HiderAgent import *
import pandas as pd
import datetime as dt

game = vzd.DoomGame()
game.load_config(os.path.join('../../../scenarios', "deathmatch_multi.cfg"))
game.add_game_args("-join 127.0.0.1 -port 5029")
game.add_game_args("+name AI +colorset 0")
game.add_game_args("-record player1.lmp")
game.set_mode(vzd.Mode.ASYNC_PLAYER)

game.set_objects_info_enabled(True)
game.set_sectors_info_enabled(True)
game.set_labels_buffer_enabled(True)




LOG_PATH = "play_enemy_log.csv"
COLUMNS = ["id", "name", "episode", "agent", "start_time", "end_time", "kill", "dead"]

# log 파일 불러오기 또는 생성
if os.path.isfile(LOG_PATH):
    log_df = pd.read_csv(LOG_PATH, encoding='cp949')
else:
    log_df = pd.DataFrame(columns=COLUMNS)

# id 정보 생성 및 입력
id = 0 if len(log_df["id"]) == 0 else max(log_df["id"])+1
name = "enemy"

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
    "hider",
    "runner",
    "defensive",
    "defensive",
    "aggressive",
    "hider",
    "runner",
    "defensive",
]

for episode, enemy in enumerate(enemy_list):
    acc_kill = 0
    acc_death = 0
    kill = 0
    death = 0
    
    start_time = dt.datetime.now()
    
    game.init()
    agent = agent_generator_list[episode]()
    
    while not game.is_episode_finished():
        # game.advance_action()
        agent.do_action()
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