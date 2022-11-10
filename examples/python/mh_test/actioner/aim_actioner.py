import vizdoom as vzd
import math
from deathmatch import *
from vizdoom_object_data import *
from actioner.actioner import * 

import random

class AimActioner(AbstractActioner):
    def __init__(self, game: vzd.DoomGame):
        super().__init__(game)
        self.randomPosFixationActioner = RandomPosFixationAction_V1(game)
        self.enomyAimActioner = EnomyAimActioner(game)

    def add_action(self, stateData: StateData2, action_order_sheet: PlayerAction):

        target_id = stateData.get_closest_enemy_label_id()
        
        if target_id is None:
            self.randomPosFixationActioner.add_action(stateData, action_order_sheet)
        else:
            self.enomyAimActioner.add_action(stateData, action_order_sheet)        

class PosFixationActioner(AbstractActioner):
    def __init__(self, game: vzd.DoomGame, target_pos:tuple):
        super().__init__(game)
        self.target_pos = target_pos

    def add_action(self, stateData: StateData2, action_order_sheet: PlayerAction):
        (x, y) = stateData.get_palyer_location()
        (tx, ty) = self.target_pos
        r_x, r_y = tx-x, ty-y
        angle = stateData.get_player().angle
        
        theta = math.atan((r_y)/(r_x))
        
        if (r_x<0):
            theta += math.pi

        theta = theta*180/math.pi
        if theta < 0:
            theta += 360

        rotate = theta - angle        

        # print("pos = ", int(x), int(y), "theta = ", theta, "rotate: ", rotate, "cur : ", angle)

        # print("pos = ", x, y, "theta = ", theta, "cur : ", angle)
        action_order_sheet[PlayerAction.rotateX] = -rotate/20

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
            MapPos.get_pos(Section.BOTTOM_PESSAGE, XPartition.RIGHT, YPartition.MIDDLE)
        ]
        super().__init__(game, pos_list, 0.1)

class EnomyAimActioner(AbstractActioner):
    # 보이는 가장 가까운 적을 응시
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
