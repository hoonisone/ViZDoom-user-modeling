import os
import vizdoom as vzd
from agent.AggressiveAgent import *
from agent.Perfect import *
game = vzd.DoomGame()
scenarios_path = '../../../scenarios'
game.load_config(os.path.join(scenarios_path, "deathmatch_multi.cfg"))
game.add_game_args("-join 127.0.0.1 -port 5029") # Connect to a host for a multiplayer game.

game.add_game_args("+name AI +colorset 0")


game.set_mode(vzd.Mode.ASYNC_PLAYER)

game.set_objects_info_enabled(True)
game.set_sectors_info_enabled(True)
game.set_labels_buffer_enabled(True)


game.init()

agent = AggressiveAgent(game)
# agent = PerfectAgent(game)
while not game.is_episode_finished():
    agent.do_action()
    

    if game.is_player_dead():
        game.respawn_player()


game.close()
