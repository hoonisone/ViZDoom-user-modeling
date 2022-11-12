from agent.agent import *
from vizdoom_object_data import *
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
    
    def do_action(self):
        state = StateData2(self.game)


        action_order_sheet = AbstractActioner.make_empty_action_order_sheet()
        self.aimActioner.add_action(state, action_order_sheet)
        # self.attackActioner.add_action(state, action_order_sheet)
        self.moveActioner.add_action(state, action_order_sheet)
        self.weaponChangeActioner.add_action(state, action_order_sheet)

        doom_action = AbstractActioner.make_into_doom_action(action_order_sheet)
        
        self.game.make_action(doom_action)

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

        # class MoveToSectionActioner(VisitActioner):

#     def __init__(self, game, section:Section, x_part:XPartition, y_part:YPartition):
#         super().__init__(game, MoveToSectionActioner.get_target_pos(section, x_part, y_part))


        # return (y, x) 