from vizdoom_object_data import *
from vizdoom_player_action import * 

class Agent:
    def __init__(self, game):
        self.game = game
        # self.aimActioner = AimActioner(game)
        # self.aimActioner = PosFixationActioner(game, (300, 300))
        self.aimActioner = AimActioner(game)
        self.attackActioner = AttackActioner(game)
        self.moveActioner = RepetitiveMoveActioner(game)
        self.weaponChangeActioner = WeaponChangeActioner(game)
    
    def do_action(self):
        state = StateData2(self.game)


        action_order_sheet = AbstractActioner.make_empty_action_order_sheet()
        self.aimActioner.add_action(state, action_order_sheet)
        self.attackActioner.add_action(state, action_order_sheet)
        self.moveActioner.add_action(state, action_order_sheet)
        self.weaponChangeActioner.add_action(state, action_order_sheet)

        doom_action = AbstractActioner.make_into_doom_action(action_order_sheet)
        
        self.game.make_action(doom_action)

    