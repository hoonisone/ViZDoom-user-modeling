from agent.agent import *
from vizdoom_object_data import *
from actioner.moving_actioner import *
from actioner.aim_actioner import *
from actioner.weaopn_actioner import * 

class PerfectAgent(AbstractAgent):
    def __init__(self, game: vzd.DoomGame):
        super().__init__(game)
        self.aimActioner = AlwaysAimClosestEnomyActioner(game)
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
        

class StayCenter(RandomActioner):
    actioner_list = [
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.LEFT , YPartition.TOP),),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.LEFT , YPartition.TOP)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.LEFT , YPartition.TOP)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.LEFT , YPartition.MIDDLE)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.LEFT , YPartition.MIDDLE)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.LEFT , YPartition.MIDDLE)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.LEFT , YPartition.BOTTOM)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.LEFT , YPartition.BOTTOM)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.LEFT , YPartition.BOTTOM)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.MIDDLE , YPartition.TOP)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.MIDDLE , YPartition.TOP)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.MIDDLE , YPartition.TOP)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.MIDDLE , YPartition.MIDDLE)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.MIDDLE , YPartition.MIDDLE)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.MIDDLE , YPartition.MIDDLE)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.MIDDLE , YPartition.BOTTOM)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.MIDDLE , YPartition.BOTTOM)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.MIDDLE , YPartition.BOTTOM)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.RIGHT , YPartition.TOP)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.RIGHT , YPartition.TOP)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.RIGHT , YPartition.TOP)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.RIGHT , YPartition.MIDDLE)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.RIGHT , YPartition.MIDDLE)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.RIGHT , YPartition.MIDDLE)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.RIGHT , YPartition.BOTTOM)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.RIGHT , YPartition.BOTTOM)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.RIGHT , YPartition.BOTTOM)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER2, XPartition.LEFT , YPartition.TOP)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER2, XPartition.LEFT , YPartition.TOP)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER2, XPartition.LEFT , YPartition.TOP)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER2, XPartition.LEFT , YPartition.MIDDLE)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER2, XPartition.LEFT , YPartition.MIDDLE)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER2, XPartition.LEFT , YPartition.MIDDLE)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER2, XPartition.LEFT , YPartition.BOTTOM)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER2, XPartition.LEFT , YPartition.BOTTOM)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER2, XPartition.LEFT , YPartition.BOTTOM)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER2, XPartition.MIDDLE , YPartition.TOP)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER2, XPartition.MIDDLE , YPartition.TOP)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER2, XPartition.MIDDLE , YPartition.TOP)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER2, XPartition.MIDDLE , YPartition.MIDDLE)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER2, XPartition.MIDDLE , YPartition.MIDDLE)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER2, XPartition.MIDDLE , YPartition.MIDDLE)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER2, XPartition.MIDDLE , YPartition.BOTTOM)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER2, XPartition.MIDDLE , YPartition.BOTTOM)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER2, XPartition.MIDDLE , YPartition.BOTTOM)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER2, XPartition.RIGHT , YPartition.TOP)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER2, XPartition.RIGHT , YPartition.TOP)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER2, XPartition.RIGHT , YPartition.TOP)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER2, XPartition.RIGHT , YPartition.MIDDLE)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER2, XPartition.RIGHT , YPartition.MIDDLE)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER2, XPartition.RIGHT , YPartition.MIDDLE)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER2, XPartition.RIGHT , YPartition.BOTTOM)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER2, XPartition.RIGHT , YPartition.BOTTOM)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER2, XPartition.RIGHT , YPartition.BOTTOM)),
    ]

    def __init__(self, game):
        super().__init__(game, StayCenter.actioner_list)


class AlwaysAimClosestEnomyActioner(AbstractActioner):
    def __init__(self, game: vzd.DoomGame):
        super().__init__(game)
        self.visibleClosestEnomyAimActioner = VisibleEnomyAimActioner(game)
        self.closestEnomyAimActioner = AlwaysFixationClosestEnomyActioner(game)

    def add_action(self, stateData: StateData2, action_order_sheet: PlayerAction):
        target_id = stateData.get_visible_closest_enemy_label_id()

        if target_id is not None:
            self.visibleClosestEnomyAimActioner.add_action(stateData, action_order_sheet)  
            return

        self.closestEnomyAimActioner.add_action(stateData, action_order_sheet)
        return

class AlwaysFixationClosestEnomyActioner(PosFixationActioner):
    def __init__(self, game: vzd.DoomGame):
        self.defalt_pos = MapPos.get_pos(Section.CENTER1, XPartition.MIDDLE, YPartition.MIDDLE)
        super().__init__(game, self.defalt_pos, 2)

    def add_action(self, stateData: StateData2, action_order_sheet: PlayerAction):
        self.target_pos = self.defalt_pos

        closest_enemy_label_id = stateData.get_closest_enemy_object_id()
        if closest_enemy_label_id != None:
            closest_enemy = stateData.get_object(closest_enemy_label_id)
            if closest_enemy != None:
                self.target_pos = (closest_enemy.position_x, closest_enemy.position_y)
        
        
        super().add_action(stateData, action_order_sheet)