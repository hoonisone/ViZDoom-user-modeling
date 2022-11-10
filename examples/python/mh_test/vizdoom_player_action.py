
from email.charset import add_alias
from abc import abstractmethod

# from multiprocessing.reduction import steal_handle
# from operator import le
# from stringprep import map_table_b2
# from telnetlib import SE
# from tkinter import N
# from typing import Annotated, overload
# from unittest import getTestCaseNames
from vizdoom_player_action import * 
from draw_map import *
from vizdoom_object_data import *
import math
from time import time
import vizdoom as vzd
import random

from deathmatch import *
class PlayerAction(IntEnum):
    Atack = 0
    Run = 1
    b = 2

    MoveRight = 3
    MoveLeft = 4
    MoveBack = 5
    MoveFront = 6
    TurnRight = 7
    TurnLeft = 8
    Use = 9

    weapone1 = 10
    weapone2 = 11
    weapone3 = 12
    weapone4 = 13
    weapone5 = 14
    weapone6 = 15

    SELECT_NEXT_WEAPON = 16
    SELECT_PREV_WEAPON = 17

    pitch = 18
    rotateX = 19
    rotateY = 20
# class DeathmatchAction:
#     def set_angle(stateData, angle):
#         action = make_action({
#             PlayerAction.rotateX: stateData.player.object.angle-angle
#         })
#         return (action, True)

#     def MoveTo(stateData, pos):
#         make_action({
#             # PlayerAction.Atack:True,
#             PlayerAction.MoveLeft: (map[y+1,x] < map[y,x]),
#             PlayerAction.MoveRight: (map[y-1,x] < map[y,x]),
#             PlayerAction.MoveBack: (map[y,x-1] < map[y,x]),
#             PlayerAction.MoveFront: (map[y,x+1] < map[y,x]),
#         })
#         pass



    # def get_map(section)
    #     if section == "Top":
    #         make_direction_map(access, ((500+1200)//8, (500+500)//8))
    #     else

class AbstractActioner:

    def __init__(self, game:vzd.DoomGame):
        self.game = game

    def make_action(self, stateData:StateData2 = None, action_order_sheet:dict = None): # Actioner가 담당하는 동작의 한 step에 해당하는 action을 생성한다.
        if stateData is None:
            stateData = StateData2(self.game.get_state())

        if action_order_sheet is None:
            action_order_sheet = AbstractActioner.make_empty_action_order_sheet()
        
        self.add_action(stateData, action_order_sheet)
        return action_order_sheet

    @ abstractmethod
    def add_action(self, stateData:StateData2, action_order_sheet:PlayerAction): # 특정 액션을 추가하는 기능을 상속 객체가 정의해야 한다.
        pass

    @ abstractmethod
    def is_finished(self, stateData: StateData2) -> bool:
        return False

    @classmethod
    def make_empty_action_order_sheet(self): # action 누적을 위한 자료구조
        return {
            PlayerAction.Atack : 0,
            PlayerAction.Run : 0,
            PlayerAction.b : 0,

            PlayerAction.MoveRight : 0,
            PlayerAction.MoveLeft : 0,
            PlayerAction.MoveBack : 0,
            PlayerAction.MoveFront : 0,
            PlayerAction.TurnRight : 0,
            PlayerAction.TurnLeft : 0,
            PlayerAction.Use : 0,

            PlayerAction.weapone1 : 0,
            PlayerAction.weapone2 : 0,
            PlayerAction.weapone3 : 0,
            PlayerAction.weapone4 : 0,
            PlayerAction.weapone5 : 0,
            PlayerAction.weapone6 : 0,


            PlayerAction.SELECT_NEXT_WEAPON : 0,
            PlayerAction.SELECT_PREV_WEAPON : 0,

            PlayerAction.pitch : 0,
            PlayerAction.rotateX : 0,
            PlayerAction.rotateY : 0,
        }

    @classmethod
    def make_into_doom_action(self, action_dict): # action_order를 doom 전용 action으로 표현
        action = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        # action = [0 for i in range(len(action_dict.keys()))]
        for key in action_dict.keys():
            action[key] = action_dict[key]
        return action

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
        action_order_sheet[PlayerAction.rotateX] = -rotate/10

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
        super().__init__(game, pos_list, 0.01)

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
            # print("True")
            action_order_sheet[PlayerAction.Atack] = 1
            return
        # print("False")


class MoveToActioner(AbstractActioner):
    
    access_map = None

    def __init__(self, game: vzd.DoomGame, directionMap, target_pos): 
        super().__init__(game)
        self.map = directionMap
        self.target_pos = target_pos

    def add_action(self, stateData: StateData2, action_order_sheet: PlayerAction):

        player = stateData.get_object(stateData.get_player_id())
        x = int(player.position_x)
        y = int(player.position_y)

        # print("position", x, y)

        if self.map[(y,x)] < 10:
            return
            
        # RotateTo(self.game, 0).do_all() # 각도를 0으로        
         
            
        x_plus = (self.map[(y,x+1)] < self.map[(y,x)])
        x_minus = (self.map[(y,x-1)] < self.map[(y,x)]) and not x_plus 

        y_plus = self.map[(y+1,x)] < self.map[(y,x)]        
        y_minus = self.map[(y-1,x)] < self.map[(y,x)] and not y_plus

        xd = 1 if x_plus else (-1 if x_minus else 0)
        yd = 1 if y_plus else (-1 if y_minus else 0)

        min_height = 100000000
        for _dy in range(-1, 2):
            for _dx in range(-1, 2):
                if self.map[(y+_dy,x+_dx)] < min_height:
                    min_height = self.map[(y+_dy,x+_dx)]
                    dx = _dx
                    dy = _dy
        # destination_angle = self.get_angle_from_direction(xd, yd)


        destination_angle = get_angle_from_player_to_direction(x, y, self.target_pos[0], self.target_pos[1]) # 글로벌 좌표공간에서 플레이어 위치와 목적지가 이루는 각도
        direct_destination_angle = self.get_angle_from_direction(xd, yd) # height map에 따른 움직여야 하는 방향
        # print(destination_angle)

        player_angle = player.angle
        
        # player_angle = StateData(self.game.get_state()).player.object.angle/
        # print(direct_destination_angle, player_angle)
        relative_angle = ((direct_destination_angle-player_angle) + 360)%360 # 플레이어 기준에서 어느 방향으로 움직여야 하는가?
        direction = self.get_direction_from_angle(relative_angle)

        

        right = True if direction[0] == 1 else False
        left  = True if direction[0] == -1 else False

        front = True if direction[1] == 1 else False # xy좌표평면과 컴퓨터가 인식하는 y는 방향이 반대
        back  = True if direction[1] == -1 else False
        
        # if random.random() < 0.1:
        #     temp = right
        #     right = left
        #     left = temp

        # if random.random() < 0.1:
        #     temp = front
        #     front = back
        #     back = temp

        action_order_sheet[PlayerAction.Run] = True
        action_order_sheet[PlayerAction.MoveFront] = front
        action_order_sheet[PlayerAction.MoveBack] = back
        action_order_sheet[PlayerAction.MoveRight] = right
        action_order_sheet[PlayerAction.MoveLeft] = left


        map_pos = self.map.access_map.get_map_pos((x, y))
        # print("************")
        # print("Front: " + str(front) + ", right: " + str(right) )
        # print("Back: " + str(back) + ", left: " + str(left) )


        # print("************")
        # for y in range(-1, 2):
        #     for x in range(-1, 2):
        #         print(self.map.map[map_pos[0]+y, map_pos[0]+x], end=", ")
        #     print("")

        
        # print("************")
        # print(str(dx) + ", " + str(dy)+"\n")

        # for dy in range(-1, 2):
        #     for dx in range(-1, 2):
        #         print(self.map[y+dy, x+dx], end=", ")
        #     print("\n")

        

        # print("************")

                

        # self.game.make_action(make_into_doom_action({
        #     PlayerAction.Run: True,
        #     PlayerAction.MoveFront: front,
        #     PlayerAction.MoveBack: back,
        #     PlayerAction.MoveRight: right,
        #     PlayerAction.MoveLeft: left,
        #     # PlayerAction.rotateX: angle
        # }))

        # SmoothRotateTo(self.game, destination_angle).do()/

        # print("x:%3d, y:%3d, dx:%3d, dy:%3d"%(x, y, self.target_pos[0], self.target_pos[1]))
        # print(destination_angle- get_player(self.game).angle)


    def get_angle_from_direction(self, x, y):
        # x, y방향으로 움직이는 여부를 가지고 이동 방향을 구한다.
        direction_list = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)] # (x, y) angle 0 부터 45도 단위로 증가

        cur_d = (x, y)
        for i, d in enumerate(direction_list):
            if cur_d == d:
                return i * 45
        return 0

        
    def get_direction_from_angle(self, angle): # 플레이어 기준으로 angle방향으로 이동하기 위한 (좌우, 앞뒤) 이동 여부를 반환
        direction_list = [(0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1)]
        angle = round(angle/45)%8
        return direction_list[angle]


    def is_finished(self, stateData: StateData2) -> bool:
        player = stateData.get_object(stateData.get_player_id())
        x = int(player.position_x)
        y = int(player.position_y)
        

        # print("height:", self.map[(y,x)])
        
        # print("height:")
        # for dy in range(-5, 5):
        #     for dx in range(-5, 5):
        #         print(self.map[(y+dy*5, x+dx*5)], end=", ")

        #     print()
        
        
        return self.map[(y,x)] < 20
        

class MoveToPositionActioner(MoveToActioner):

    access_map = None
    direction_map_dict = {}

    def __init__(self, game: vzd.DoomGame, position ):

        if MoveToPositionActioner.access_map is None:
            MoveToPositionActioner.access_map = AccessMap(game)

        if position not in MoveToPositionActioner.direction_map_dict:
            MoveToPositionActioner.direction_map_dict[position] = HeightMap(MoveToPositionActioner.access_map, position)

        super().__init__(game, MoveToPositionActioner.direction_map_dict[position], position)

class MoveToSectionActioner(MoveToPositionActioner):

    def __init__(self, game, section:Section, x_part:XPartition, y_part:YPartition):
        super().__init__(game, MoveToSectionActioner.get_target_pos(section, x_part, y_part))


        # return (y, x) 

class RepetitiveMoveActioner(AbstractActioner):
    def __init__(self, game):
        self.idx = 0
        self.moveActionerList = [
            # 무기 모두 먹기
            MoveToPositionActioner(game, MapPos.get_pos(Section.TOP_PESSAGE, XPartition.MIDDLE , YPartition.MIDDLE)),
            MoveToPositionActioner(game, MapPos.get_pos(Section.TOP, XPartition.MIDDLE , YPartition.BOTTOM)),
            MoveToPositionActioner(game, MapPos.get_pos(Section.TOP, XPartition.RIGHT, YPartition.BOTTOM)),
            MoveToPositionActioner(game, MapPos.get_pos(Section.TOP, XPartition.RIGHT, YPartition.TOP)),
            MoveToPositionActioner(game, MapPos.get_pos(Section.TOP, XPartition.LEFT, YPartition.TOP)),
            MoveToPositionActioner(game, MapPos.get_pos(Section.TOP, XPartition.LEFT, YPartition.BOTTOM)),
            MoveToPositionActioner(game, MapPos.get_pos(Section.TOP, XPartition.MIDDLE, YPartition.BOTTOM)),
            MoveToPositionActioner(game, MapPos.get_pos(Section.TOP_PESSAGE, XPartition.MIDDLE, YPartition.MIDDLE)),

            # 힐팩 모두 먹기
            MoveToPositionActioner(game, MapPos.get_pos(Section.LEFT_PASSAGE, XPartition.MIDDLE, YPartition.TOP)),
            MoveToPositionActioner(game, MapPos.get_pos(Section.LEFT, XPartition.RIGHT, YPartition.TOP)),
            MoveToPositionActioner(game, MapPos.get_pos(Section.LEFT, XPartition.LEFT, YPartition.TOP)),
            MoveToPositionActioner(game, MapPos.get_pos(Section.LEFT, XPartition.LEFT, YPartition.BOTTOM)),
            MoveToPositionActioner(game, MapPos.get_pos(Section.LEFT, XPartition.RIGHT, YPartition.BOTTOM)),
            MoveToPositionActioner(game, MapPos.get_pos(Section.LEFT, XPartition.RIGHT, YPartition.TOP)),

            # 힐팩 존에 왔다 갔다 머물기

            MoveToPositionActioner(game, MapPos.get_pos(Section.LEFT, XPartition.LEFT, YPartition.BOTTOM)),
            MoveToPositionActioner(game, MapPos.get_pos(Section.LEFT_PASSAGE, XPartition.MIDDLE, YPartition.BOTTOM)),
            MoveToPositionActioner(game, MapPos.get_pos(Section.CENTER2, XPartition.LEFT, YPartition.BOTTOM)),
            MoveToPositionActioner(game, MapPos.get_pos(Section.LEFT_PASSAGE, XPartition.MIDDLE, YPartition.BOTTOM)),
            MoveToPositionActioner(game, MapPos.get_pos(Section.LEFT, XPartition.LEFT, YPartition.BOTTOM)),

            MoveToPositionActioner(game, MapPos.get_pos(Section.LEFT, XPartition.LEFT, YPartition.MIDDLE)),
            MoveToPositionActioner(game, MapPos.get_pos(Section.LEFT_PASSAGE, XPartition.MIDDLE, YPartition.MIDDLE)),
            MoveToPositionActioner(game, MapPos.get_pos(Section.CENTER2, XPartition.LEFT, YPartition.MIDDLE)),
            MoveToPositionActioner(game, MapPos.get_pos(Section.LEFT_PASSAGE, XPartition.MIDDLE, YPartition.MIDDLE)),
            MoveToPositionActioner(game, MapPos.get_pos(Section.LEFT, XPartition.LEFT, YPartition.MIDDLE)),
            
            MoveToPositionActioner(game, MapPos.get_pos(Section.LEFT, XPartition.LEFT, YPartition.TOP)),
            MoveToPositionActioner(game, MapPos.get_pos(Section.LEFT_PASSAGE, XPartition.MIDDLE, YPartition.TOP)),
            MoveToPositionActioner(game, MapPos.get_pos(Section.CENTER2, XPartition.LEFT, YPartition.TOP)),
            MoveToPositionActioner(game, MapPos.get_pos(Section.LEFT_PASSAGE, XPartition.MIDDLE, YPartition.TOP)),
            MoveToPositionActioner(game, MapPos.get_pos(Section.LEFT, XPartition.LEFT, YPartition.TOP)),

            # 가운데 통로로 빠져나가기
            MoveToPositionActioner(game, MapPos.get_pos(Section.LEFT, XPartition.LEFT, YPartition.MIDDLE)),
            MoveToPositionActioner(game, MapPos.get_pos(Section.LEFT_PASSAGE, XPartition.MIDDLE, YPartition.MIDDLE)),
            MoveToPositionActioner(game, MapPos.get_pos(Section.CENTER2, XPartition.LEFT, YPartition.MIDDLE)),
        ]

    
    def add_action(self, stateData:StateData2 = None, action_order_sheet:dict = None): # Actioner가 담당하는 동작의 한 step에 해당하는 action을 생성한다.
        # print("move action", "idx: ", self.idx)

        if self.moveActionerList[self.idx].is_finished(stateData):
            self.idx = (self.idx + 1) % len(self.moveActionerList)
            # print("changed", "idx: ", self.idx)
        
        # name = ["Top", "Right", "Cector", "Right", "botton", "left", "centor", "left"]
        # print(self.idx, self.is_finished(stateData))

        self.moveActionerList[self.idx].add_action(stateData, action_order_sheet)


class WeaponChangeActioner(AbstractActioner):
    def __init__(self, game:vzd.DoomGame):
        super().__init__(game)

    def add_action(self, stateData: StateData2, action_order_sheet: PlayerAction):
        # return super().add_action(stateData, action_order_sheet)
        # print(stateData.state.game_variables[4])
        # p = random.random()
        
        if int(time()) % 5 == 0:

            weapon = [
                PlayerAction.weapone1,
                PlayerAction.weapone1,
                PlayerAction.weapone2,
                PlayerAction.weapone3,
                PlayerAction.weapone4,
                PlayerAction.weapone5,
                PlayerAction.weapone6,
            ]
            possess = stateData.get_weapon_possess()
            ammo = stateData.get_weapon_ammo()
            for i in [6, 4, 2, 3, 5, 1]:
                if 0 < possess[i] and 0 < ammo[i]:
                    empty = AbstractActioner.make_empty_action_order_sheet()
                    empty[PlayerAction.weapone6] = 1
                    empty = AbstractActioner.make_into_doom_action(empty)
                    self.game.make_action(empty)
                    action_order_sheet[weapon[i]] = 1
                    return

            action_order_sheet[PlayerAction.weapone1] = 1
        

        # if p < 0.5:

        # if random.
        # if random.random() < 0.01:
        #     action_order_sheet[PlayerAction.SELECT_NEXT_WEAPON] = 1