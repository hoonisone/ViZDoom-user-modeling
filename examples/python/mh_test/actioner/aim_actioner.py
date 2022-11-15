import vizdoom as vzd
import math
from actioner.deathmatch_pos import *
from state.vizdoom_object_data import *
from actioner.actioner import * 

import random

class AimActioner(AbstractActioner):
    def __init__(self, game: vzd.DoomGame):
        super().__init__(game)
        self.randomPosFixationActioner = RandomPosFixationAction_V1(game)
        self.visibleClosestEnomyAimActioner = VisibleEnomyAimActioner(game)
        self.closestEnomyAimActioner = ClosestEnomyAimActioner(game)

    def add_action(self, stateData: StateData2, action_order_sheet: PlayerAction):
        target_id = stateData.get_visible_closest_enemy_label_id()

        if target_id is not None:
            self.visibleClosestEnomyAimActioner.add_action(stateData, action_order_sheet)  
            return

        target_id = stateData.get_closest_enemy_label_id()
        
        if target_id is not None:
            dist = stateData.get_dist_from_player(target_id)
            if dist < 50:
                self.closestEnomyAimActioner.add_action(stateData, action_order_sheet)
                return

        self.randomPosFixationActioner.add_action(stateData, action_order_sheet)
        return
        
        
  

class PosFixationActioner(AbstractActioner):
    def __init__(self, game: vzd.DoomGame, target_pos:tuple, slow=10):
        super().__init__(game)
        self.target_pos = target_pos
        self.slow = slow

    def add_action(self, stateData: StateData2, action_order_sheet: PlayerAction):
        (x, y) = stateData.get_player_pos()
        (tx, ty) = self.target_pos
        r_x, r_y = tx-x, ty-y
        angle = stateData.get_player().angle
    
        if r_x == 0:
            return

        theta = math.atan((r_y)/(r_x))

        if (r_x<0):
            theta += math.pi

        theta = theta*180/math.pi
        if theta < 0:
            theta += 360

        rotate = theta - angle      
        
        if rotate > 180:
            rotate -= 360  

        if rotate < -180:
            rotate += 360

        # print("pos = ", int(x), int(y), "theta = ", theta, "rotate: ", rotate, "cur : ", angle)

        # print("pos = ", x, y, "theta = ", theta, "cur : ", angle)
        action_order_sheet[PlayerAction.rotateX] = -rotate/self.slow

            # if (r_x>0):
            #     theta = math.pi + theta
            # theta = theta*180/math.pi
            # rotate = theta - self.angle
            # if rotate < 0:
            #     rotate += 360

            # if rotate > 180:
            #     # rotate = 360-rotate
            #     self.action[PlayerAction.TurnLeft]=True
            #     self.action[PlayerAction.Run]=True
            #     if rotate-180<5:
            #         self.action[PlayerAction.TurnLeft]=False
            #         self.action[PlayerAction.Run]=False
            #         self.action[PlayerAction.rotateX] = -25

            # else:
            #     self.action[PlayerAction.TurnRight]=True
            #     self.action[PlayerAction.Run]=True
            #     if 180-rotate<5:
            #         self.action[PlayerAction.TurnLeft]=False
            #         self.action[PlayerAction.Run]=False
            #         self.action[PlayerAction.rotateX] = 25

class RandomPosFixationAction(AbstractActioner):
    def __init__(self, game: vzd.DoomGame, target_pos_list:list, change_p:float):
        super().__init__(game)
        self.target_pos_list = target_pos_list
        self.change_p = change_p
        self.change_sub_actioner()

    def add_action(self, stateData: StateData2, action_order_sheet: PlayerAction):
        if random.random() < self.change_p:
            self.change_sub_actioner()
        self.sub_actioner.add_action(stateData, action_order_sheet)    

    def change_sub_actioner(self):
        pos = self.target_pos_list[random.randrange(len(self.target_pos_list))]
        self.sub_actioner = PosFixationActioner(self.game, pos)



class RandomPosFixationAction_V1(RandomPosFixationAction):
    def __init__(self, game: vzd.DoomGame):
        pos_list = [
            MapPos.get_pos(Section.TOP_PESSAGE, XPartition.LEFT, YPartition.MIDDLE),
            MapPos.get_pos(Section.TOP_PESSAGE, XPartition.MIDDLE, YPartition.MIDDLE),
            MapPos.get_pos(Section.TOP_PESSAGE, XPartition.RIGHT, YPartition.MIDDLE),

            MapPos.get_pos(Section.BOTTOM_PESSAGE, XPartition.LEFT, YPartition.MIDDLE),
            MapPos.get_pos(Section.BOTTOM_PESSAGE, XPartition.MIDDLE, YPartition.MIDDLE),
            MapPos.get_pos(Section.BOTTOM_PESSAGE, XPartition.RIGHT, YPartition.MIDDLE),
            MapPos.get_pos(Section.CENTER2, XPartition.LEFT, YPartition.TOP),
            MapPos.get_pos(Section.CENTER2, XPartition.LEFT, YPartition.MIDDLE),
            MapPos.get_pos(Section.CENTER2, XPartition.LEFT, YPartition.BOTTOM),
            MapPos.get_pos(Section.CENTER2, XPartition.MIDDLE, YPartition.TOP),
            MapPos.get_pos(Section.CENTER2, XPartition.MIDDLE, YPartition.MIDDLE),
            MapPos.get_pos(Section.CENTER2, XPartition.MIDDLE, YPartition.BOTTOM),
            MapPos.get_pos(Section.CENTER2, XPartition.RIGHT, YPartition.TOP),
            MapPos.get_pos(Section.CENTER2, XPartition.RIGHT, YPartition.MIDDLE),
            MapPos.get_pos(Section.CENTER2, XPartition.RIGHT, YPartition.BOTTOM),
        ]
        super().__init__(game, pos_list, 0.01)

class VisibleEnomyAimActioner(AbstractActioner):
    # 보이는 가장 가까운 적을 응시
    def __init__(self, game: vzd.DoomGame):
        super().__init__(game)

    def add_action(self, stateData: StateData2, action_order_sheet: PlayerAction):
        target_id = stateData.get_visible_closest_enemy_label_id()
        if target_id is None:
            return

        dist = stateData.get_x_pixel_dist(target_id)
        if dist is None:
            return 

        if len(stateData.enemy_label_id_list) >= 4:
            action_order_sheet[PlayerAction.rotateX] = 50 * dist/(self.game.get_screen_width()/2)/2 + math.sin(time()*5)*10
            action_order_sheet[PlayerAction.Atack] = 1
        else:
            action_order_sheet[PlayerAction.rotateX] = 50 * dist/(self.game.get_screen_width()/2)/2 + math.sin(time()*10)
            if stateData.is_in_shotting_effective_zone(target_id):
                action_order_sheet[PlayerAction.Atack] = 1

class ClosestEnomyAimActioner(AbstractActioner):
    # 그냥 가장 가까운 적을 응시
    def __init__(self, game: vzd.DoomGame):
        super().__init__(game)

    def add_action(self, stateData: StateData2, action_order_sheet: PlayerAction):
        target_id = stateData.get_closest_enemy_label_id()
        if target_id is None:
            return

        dist = stateData.get_x_pixel_dist(target_id)
        if dist is None:
            return 

        if len(stateData.enemy_label_id_list) >= 4:
            action_order_sheet[PlayerAction.rotateX] = 50 * dist/(self.game.get_screen_width()/2)/2 + math.sin(time()*5)*10
        else:
            action_order_sheet[PlayerAction.rotateX] = 50 * dist/(self.game.get_screen_width()/2)/2 + math.sin(time()*10)

class AttackActioner(AbstractActioner):
    def __init__(self, game: vzd.DoomGame):
        super().__init__(game)

    def add_action(self, stateData: StateData2, action_order_sheet: PlayerAction):
        if len(stateData.get_enemy_label_id_list()) >= 4:
            action_order_sheet[PlayerAction.Atack] = 1
            return

        target_id = stateData.get_closest_enemy_label_id()
        if target_id is None:
            return

        if stateData.is_in_shotting_effective_zone(target_id):
            action_order_sheet[PlayerAction.Atack] = 1
            return

