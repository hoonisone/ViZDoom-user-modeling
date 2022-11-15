from state.vizdoom_state import *
from actioner.moving_actioner import *
from actioner.aim_actioner import *
from actioner.weaopn_actioner import * 
from actioner.attackActioner import *

class AbstractAgent(AbstractActioner):
    def __init__(self, game):
        super().__init__(game)
    

class HealpackFarmingAgent(AbstractAgent):
    """
    * 중앙에서 힐팩 존 근처로 가서 들어간 뒤 한 바퀴 돌고 나오는 에이전트
    """
    def __init__(self, game):
        super().__init__(game)
        self.attack_actioner = AttackActioner(game)
        self.aim_actioner = AimActioner(game)
        self.movement_actioner = CycledActioner(game, [lambda game : FarmingHealpackZone(game)]) # 힐팩 존 반복 방문 
        self.weapon_actioner = WeaponChangeActioner(game)
    
    def add_action(self, state: StateAnalyzer, action_order_sheet: PlayerAction):
        self.attack_actioner.add_action(state, action_order_sheet)
        self.aim_actioner.add_action(state, action_order_sheet)
        self.movement_actioner.add_action(state, action_order_sheet)
        self.weapon_actioner.add_action(state, action_order_sheet)

    def is_finished(self, state: StateAnalyzer) -> bool:
        return self.movement_actioner.is_finished(state)

class WeaponFarmingAgent(AbstractAgent):
    """
    * 중앙에서 무기 존 근처로 가서 들어간 뒤 한 바퀴 돌고 나오는 에이전트
    """
    def __init__(self, game):
        super().__init__(game)
        self.attack_actioner = AttackActioner(game)
        self.aim_actioner = AimActioner(game)
        self.movement_actioner = FarmingWeaponZone(game) # 힐팩 존 한 바퀴 돌고 나오기 
        self.weapon_actioner = WeaponChangeActioner(game)
    
    def add_action(self, state: StateAnalyzer, action_order_sheet: PlayerAction):
        self.attack_actioner.add_action(state, action_order_sheet)
        self.aim_actioner.add_action(state, action_order_sheet)
        self.movement_actioner.add_action(state, action_order_sheet)
        self.weapon_actioner.add_action(state, action_order_sheet)

    def is_finished(self, state: StateAnalyzer) -> bool:
        return self.movement_actioner.is_finished(state)

class CenterStayAgent(AbstractActioner):
    """
    * 중앙에서 배회하는 에이전트
    """
    def __init__(self, game):
        super().__init__(game)
        self.attack_actioner = AttackActioner(game)
        self.aim_actioner = AimActioner(game)
        self.movement_actioner = StayCenter(game) # 힐팩 존 한 바퀴 돌고 나오기 
        self.weapon_actioner = WeaponChangeActioner(game)
    
    def add_action(self, state: StateAnalyzer, action_order_sheet: PlayerAction):
        self.attack_actioner.add_action(state, action_order_sheet)
        self.aim_actioner.add_action(state, action_order_sheet)
        self.movement_actioner.add_action(state, action_order_sheet)
        self.weapon_actioner.add_action(state, action_order_sheet)

    def is_finished(self, state: StateAnalyzer) -> bool:
        return self.movement_actioner.is_finished(state)



# class TrackerAgent(AbstractActioner):
#     """
#     * 중앙에서 배회하는 에이전트=
#     """
#     def __init__(self, game):
#         super().__init__(game)
#         self.aim_actioner = AimActioner(game)
#         self.movement_actioner = FarmingWeaponZone(game) # 힐팩 존 한 바퀴 돌고 나오기 
#         self.weapon_actioner = WeaponChangeActioner(game)
    
#     def add_action(self, state: StateAnalyzer, action_order_sheet: PlayerAction):
#         self.aim_actioner.add_action(state, action_order_sheet)
#         self.movement_actioner.add_action(state, action_order_sheet)
#         self.weapon_actioner.add_action(state, action_order_sheet)

#     def is_finished(self, state: StateAnalyzer) -> bool:
#         self.movement_actioner.is_finished(state)




