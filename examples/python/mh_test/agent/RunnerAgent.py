from state.vizdoom_state import *
from actioner.moving_actioner import *
from actioner.aim_actioner import *
from actioner.weaopn_actioner import * 
from actioner.attackActioner import *
from agent.agent import *
import random

class RunnerAgent(AbstractAgent):
    """
    * 중앙에서 힐팩 존 근처로 가서 들어간 뒤 한 바퀴 돌고 나오는 에이전트
    """
    def __init__(self, game):
        super().__init__(game)
        self.attack_actioner = AttackActioner(game, cool_time=1)
        self.aim_actioner = AimActioner(game)
        # self.movement_actioner = ThoroughlyVisitAllSector(game) # 힐팩 존 반복 방문 
        self.movement_actioner = RoughlyVisitAllSector(game)
        self.weapon_actioner = WeaponChangeActioner(game)
    
    def add_action(self, state: StateAnalyzer, action_order_sheet: PlayerAction):
        self.attack_actioner.add_action(state, action_order_sheet)
        self.aim_actioner.add_action(state, action_order_sheet)
        self.movement_actioner.add_action(state, action_order_sheet)
        self.weapon_actioner.add_action(state, action_order_sheet)

    def is_finished(self, state: StateAnalyzer) -> bool:
        return self.movement_actioner.is_finished(state)

class ThoroughlyVisitAllSector(CycledActioner):
    def __init__(self, game):
        actioner_generator_list = [
        lambda game : VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.LEFT , YPartition.TOP)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.TOP_PESSAGE, XPartition.LEFT , YPartition.MIDDLE)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.TOP, XPartition.LEFT, YPartition.BOTTOM)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.TOP, XPartition.RIGHT, YPartition.BOTTOM)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.TOP, XPartition.RIGHT, YPartition.TOP)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.TOP, XPartition.LEFT, YPartition.TOP)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.TOP, XPartition.LEFT, YPartition.BOTTOM)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.TOP_PESSAGE, XPartition.LEFT , YPartition.MIDDLE)),

        lambda game : VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.LEFT , YPartition.TOP)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.LEFT_PESSAGE, XPartition.MIDDLE , YPartition.TOP)), # 입구로 가서
        lambda game : VisitActioner(game, MapPos.get_pos(Section.LEFT, XPartition.RIGHT, YPartition.TOP)),          # 돌고
        lambda game : VisitActioner(game, MapPos.get_pos(Section.LEFT, XPartition.LEFT, YPartition.TOP)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.LEFT, XPartition.LEFT, YPartition.BOTTOM)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.LEFT, XPartition.RIGHT, YPartition.BOTTOM)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.LEFT_PESSAGE, XPartition.MIDDLE , YPartition.BOTTOM)), # 동일 입구로 가기
        lambda game : VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.LEFT , YPartition.BOTTOM)),

        lambda game : VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.LEFT , YPartition.BOTTOM)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.BOTTOM_PESSAGE, XPartition.LEFT , YPartition.MIDDLE)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.BOTTOM, XPartition.LEFT, YPartition.TOP)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.BOTTOM, XPartition.LEFT, YPartition.BOTTOM)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.BOTTOM, XPartition.RIGHT, YPartition.BOTTOM)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.BOTTOM, XPartition.RIGHT, YPartition.TOP)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.BOTTOM_PESSAGE, XPartition.RIGHT , YPartition.MIDDLE)),

        lambda game : VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.RIGHT , YPartition.BOTTOM)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.RIGHT_PESSAGE, XPartition.MIDDLE , YPartition.BOTTOM)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.RIGHT, XPartition.LEFT, YPartition.BOTTOM)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.RIGHT, XPartition.RIGHT, YPartition.BOTTOM)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.RIGHT, XPartition.RIGHT, YPartition.TOP)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.RIGHT, XPartition.LEFT, YPartition.TOP)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.RIGHT_PESSAGE, XPartition.MIDDLE, YPartition.TOP)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.RIGHT , YPartition.TOP)),
        ]
        super().__init__(game, actioner_generator_list)

class ThoroughlyVisitAllSector(CycledActioner):
    def __init__(self, game):
        actioner_generator_list = [
        lambda game : VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.LEFT , YPartition.TOP)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.TOP_PESSAGE, XPartition.LEFT , YPartition.MIDDLE)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.TOP, XPartition.LEFT, YPartition.BOTTOM)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.TOP, XPartition.RIGHT, YPartition.BOTTOM)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.TOP, XPartition.RIGHT, YPartition.TOP)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.TOP, XPartition.LEFT, YPartition.TOP)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.TOP, XPartition.LEFT, YPartition.BOTTOM)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.TOP_PESSAGE, XPartition.LEFT , YPartition.MIDDLE)),

        lambda game : VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.LEFT , YPartition.TOP)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.LEFT_PESSAGE, XPartition.MIDDLE , YPartition.TOP)), # 입구로 가서
        lambda game : VisitActioner(game, MapPos.get_pos(Section.LEFT, XPartition.RIGHT, YPartition.TOP)),          # 돌고
        lambda game : VisitActioner(game, MapPos.get_pos(Section.LEFT, XPartition.LEFT, YPartition.TOP)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.LEFT, XPartition.LEFT, YPartition.BOTTOM)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.LEFT, XPartition.RIGHT, YPartition.BOTTOM)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.LEFT_PESSAGE, XPartition.MIDDLE , YPartition.BOTTOM)), # 동일 입구로 가기
        lambda game : VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.LEFT , YPartition.BOTTOM)),

        lambda game : VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.LEFT , YPartition.BOTTOM)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.BOTTOM_PESSAGE, XPartition.LEFT , YPartition.MIDDLE)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.BOTTOM, XPartition.LEFT, YPartition.TOP)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.BOTTOM, XPartition.LEFT, YPartition.BOTTOM)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.BOTTOM, XPartition.RIGHT, YPartition.BOTTOM)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.BOTTOM, XPartition.RIGHT, YPartition.TOP)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.BOTTOM_PESSAGE, XPartition.RIGHT , YPartition.MIDDLE)),

        lambda game : VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.RIGHT , YPartition.BOTTOM)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.RIGHT_PESSAGE, XPartition.MIDDLE , YPartition.BOTTOM)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.RIGHT, XPartition.LEFT, YPartition.BOTTOM)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.RIGHT, XPartition.RIGHT, YPartition.BOTTOM)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.RIGHT, XPartition.RIGHT, YPartition.TOP)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.RIGHT, XPartition.LEFT, YPartition.TOP)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.RIGHT_PESSAGE, XPartition.MIDDLE, YPartition.TOP)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.RIGHT , YPartition.TOP)),
        ]
        super().__init__(game, actioner_generator_list)

class RoughlyVisitAllSector(CycledActioner):
    def __init__(self, game):
        actioner_generator_list = [
            lambda game : VisitTopSector(game),
            lambda game : VisitRightSector(game),
            lambda game : VisitBottomSector(game),
            lambda game : VisitLeftSector(game),
        ]
        super().__init__(game, [lambda game : actioner_generator_list[random.randrange(4)](game)])