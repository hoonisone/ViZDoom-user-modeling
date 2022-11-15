#!/usr/bin/env python3

#####################################################################
# This script presents how to host a deathmatch game.
#####################################################################

import os
from random import choice
import vizdoom as vzd


game = vzd.DoomGame()

# Use CIG example config or your own.

# game.load_config(os.path.join("./scenarios", "deathmatch.cfg"))
game.load_config(os.path.join(vzd.scenarios_path, "cig.cfg"))
# game.load_config(os.path.join(vzd.scenarios_path, "deathmatch.cfg"))
# game.load_config(os.path.join("../scenarios/", "deathmatch.cfg"))

game.add_game_args("-host 2 "  
                   # This machine will function as a host for a multiplayer game with this many players (including this machine). 
                   # It will wait for other machines to connect using the -join parameter and then start the game when everyone is connected.
                   "-port 5029 "              # Specifies the port (default is 5029).
                   "+viz_connect_timeout 60 " # Specifies the time (in seconds), that the host will wait for other players (default is 60).
                #    "-deathmatch "             # Deathmatch rules are used for the game.
                   "+timelimit 10.0 "         # The game (episode) will end after this many minutes have elapsed.
                   "+sv_forcerespawn 1 "      # Players will respawn automatically after they die.
                   "+sv_noautoaim 1 "         # Autoaim is disabled for all players.
                   "+sv_respawnprotect 1 "    # Players will be invulnerable for two second after spawning.
                   "+sv_spawnfarthest 1 "     # Players will be spawned as far as possible from any other players.
                   "+sv_nocrouch 1 "          # Disables crouching.
                   "+viz_respawn_delay 10 "   # Sets delay between respawns (in seconds, default is 0).
                   "+viz_nocheat 1")          # Disables depth and labels buffer and the ability to use commands that could interfere with multiplayer game.

game.add_game_args("+name Host +colorset 0")
game.set_mode(vzd.Mode.ASYNC_SPECTATOR)


game.init()


while not game.is_episode_finished():
    s = game.get_state()

    game.advance_action() # 이거 있어야 조작 가능

    if game.is_player_dead():
        game.respawn_player()

game.close()
