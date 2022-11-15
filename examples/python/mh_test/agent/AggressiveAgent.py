from agent.agent import *
from vizdoom_object_data import *
from actioner.moving_actioner import *
from actioner.aim_actioner import *
from actioner.weaopn_actioner import * 

class AggressiveAgent(AbstractAgent):
    def __init__(self, game: vzd.DoomGame):
        super().__init__(game)
        self.aimActioner = AimActioner(game)
        # self.attackActioner = AttackActioner(game)
        self.moveActioner = AggressiveMovementActioner(game)
        self.weaponChangeActioner = WeaponChangeActioner(game)
        

    def do_action(self):
        state = StateData2(self.game)

        action_order_sheet = AbstractActioner.make_empty_action_order_sheet()
        self.aimActioner.add_action(state, action_order_sheet)
        self.moveActioner.add_action(state, action_order_sheet)
        self.weaponChangeActioner.add_action(state, action_order_sheet)
        doom_action = AbstractActioner.make_into_doom_action(action_order_sheet)
        self.game.make_action(doom_action)
    
        

class AggressiveMovementActioner(AbstractActioner):
    # 무기존, 힐팩존 반복 방문
    def __init__(self, game):
        super().__init__(game)
        self.actioner = FarmingWeaponZone(game)

    def add_action(self, stateData: StateData2, action_order_sheet: PlayerAction):
        if self.actioner.is_finished(stateData):
            self.actioner = StayCenter(self.game)
        
        self.actioner.add_action(stateData, action_order_sheet)
        

FarmingHealpackZone