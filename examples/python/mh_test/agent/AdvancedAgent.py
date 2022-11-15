from agent.agent import *
from state.vizdoom_state import *
from actioner.moving_actioner import *
from actioner.aim_actioner import *
from actioner.weaopn_actioner import * 

class AdvancedAgent(AbstractAgent):
    def __init__(self, game):
        self.game = game
        # self.aimActioner = AimActioner(game)
        # self.aimActioner = PosFixationActioner(game, (300, 300))
        self.aimActioner = AimActioner(game)
        # self.attackActioner = AttackActioner(game)
        self.moveActioner = WeaponZoneHealpackZoneCycliedVisitAction(game)
        self.weaponChangeActioner = WeaponChangeActioner(game)
    

    def add_action(self, stateData: StateAnalyzer, action_order_sheet: PlayerAction):
        self.aimActioner.add_action(state, action_order_sheet)
        self.moveActioner.add_action(state, action_order_sheet)
        self.weaponChangeActioner.add_action(state, action_order_sheet) 

class WeaponZoneHealpackZoneCycliedVisitAction(CycledActioner):
    # 무기존, 힐팩존 반복 방문
    def __init__(self, game):
        moveActionerList = [
        # 무기 모두 먹기
            FarmingWeaponZone(game),
            FarmingHealpackZone(game),
            VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.MIDDLE, YPartition.MIDDLE)),
            FarmingHealpackZone(game),
            VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.MIDDLE, YPartition.MIDDLE)),
            FarmingHealpackZone(game),
            VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.MIDDLE, YPartition.MIDDLE)),
            FarmingWeaponZone(game),
            FarmingHealpackZone(game),
            VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.MIDDLE, YPartition.MIDDLE)),
            FarmingHealpackZone(game),
            VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.MIDDLE, YPartition.MIDDLE)),
            FarmingHealpackZone(game),
            VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.MIDDLE, YPartition.MIDDLE)),

        ]
        super().__init__(game, moveActionerList)

