#!/usr/bin/python3

#####################################################################
# This script presents how to use Doom's native demo mechanism to
# record multiplayer game and replay it with perfect accuracy.
#####################################################################

# WARNING:
# Due to the bug in build-in bots recording game with bots will result in the desynchronization of the recording.

from multiprocessing import Process
import os
from random import choice
import vizdoom as vzd


def replay_as_player2():
    game = vzd.DoomGame()
    game.load_config(os.path.join('../../../scenarios', "deathmatch_multi.cfg"))
    # At this moment ViZDoom will crash if there is no starting point - this is workaround for multiplayer map.
    game.add_game_args("-host 1 -deathmatch")

    game.init()

    # Replays episode recorded by player 1 from perspective of player2.
    game.replay_episode("player2.lmp", 2)

    while not game.is_episode_finished():
        game.advance_action()
        print(game.get_available_game_variables())
    print("Game finished!")
    print("Player1 frags:", game.get_game_variable(vzd.GameVariable.PLAYER1_FRAGCOUNT))
    print("Player2 frags:", game.get_game_variable(vzd.GameVariable.PLAYER2_FRAGCOUNT))
    game.close()

replay_as_player2()