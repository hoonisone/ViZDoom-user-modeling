from state.vizdoom_state import *
from actioner.moving_actioner import *
from actioner.aim_actioner import *
from actioner.weaopn_actioner import * 
from actioner.attackActioner import *
from agent.agent import *
import random
from actioner.HideActioner import *

class HiderAgent(AbstractAgent):
    """
    * 중앙에서 힐팩 존 근처로 가서 들어간 뒤 한 바퀴 돌고 나오는 에이전트
    """
    def __init__(self, game):
        super().__init__(game)
        self.attack_actioner = AttackActioner(game)
        self.aim_actioner = AimActioner(game)
        # self.movement_actioner = ThoroughlyVisitAllSector(game) # 힐팩 존 반복 방문 
        self.movement_actioner = HideMovementActioner(game)
        self.weapon_actioner = WeaponChangeActioner(game)
    
    def add_action(self, state: StateAnalyzer, action_order_sheet: PlayerAction):
        self.attack_actioner.add_action(state, action_order_sheet)
        self.aim_actioner.add_action(state, action_order_sheet)
        self.movement_actioner.add_action(state, action_order_sheet)
        self.weapon_actioner.add_action(state, action_order_sheet)

    def is_finished(self, state: StateAnalyzer) -> bool:
        return self.movement_actioner.is_finished(state)



class HideMovementActioner(AbstractActioner):
    def __init__(self, game):
        super().__init__(game)
        self.hider_list = [
            lambda game : HideTopSector(game),
            lambda game : HideBottomSector(game),
            lambda game : HideLeftSector(game),
            lambda game : HideRightSector(game),
        ]
        self.hiding = True
        self.actioner = self.get_new_actioner()

    def get_new_actioner(self):
        return self.hider_list[random.randrange(len(self.hider_list))](self.game)

    def add_action(self, stateData: StateAnalyzer, action_order_sheet: PlayerAction) -> None:
        if self.hiding:
            self.actioner.add_action(stateData, action_order_sheet)
            if self.actioner.is_finished(stateData) and stateData.is_enemy_exist_in_screen():
                self.actioner = VisitActioner(self.game, MapPos.get_pos(Section.CENTER1, XPartition.MIDDLE, YPartition.MIDDLE))
                self.hiding = False
        else:
            self.actioner.add_action(stateData, action_order_sheet)
            if self.actioner.is_finished(stateData):
                self.actioner = self.get_new_actioner()
                self.hiding = True
            