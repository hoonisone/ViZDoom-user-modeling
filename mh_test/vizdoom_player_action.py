
from enum import IntEnum
from abc import abstractmethod

from multiprocessing.reduction import steal_handle
import secrets
from stringprep import map_table_b2
from telnetlib import SE
from typing import overload
from unittest import getTestCaseNames
from vizdoom_player_action import * 
from draw_map import *
from vizdoom_object_data import *
import math
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
    weapone1 = 9
    weapone2 = 10
    weapone3 = 11
    weapone4 = 12
    weapone5 = 13
    weapone6 = 14
    f = 15
    e = 16
    rotateY = 17
    rotateX = 18

def make_action(action_dict):
    action = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for key in action_dict.keys():
        action[key] = action_dict[key]
    return action




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

class AbstractAction:
    @ abstractmethod
    def do(self): # 한 스텝 수행 후 종료 여부 반환
        pass

    def do_all(self) -> bool: # 액션의 전체 과정을 수행
        while True:
            if self.do():
                break

class RotateTo(AbstractAction):
    def __init__(self, game, angle):
        self.game = game
        self.angle = angle

    def do(self):
        self.game.make_action(make_action({
                PlayerAction.rotateX: StateData(self.game.get_state()).player.object.angle-self.angle
        }))
        return True

class SmoothRotateTo(AbstractAction):
    def __init__(self, game, angle):
        self.game = game
        self.angle = angle

    def do(self):
        player_angle = get_player(self.game).angle
        
        if abs(player_angle - self.angle) < 5: # 원하는 각도와 별 차이 없으면
            return True

        player_angle = (player_angle%360)-180
        target_angle = (self.angle%360)-180

        angle_dist = target_angle - player_angle
        
        if angle_dist < 0: # 반시계 방향으로 돌 것인가?
            how_to_rotate = -min(3, abs(angle_dist))
        else:
            how_to_rotate = min(3, abs(angle_dist))

        self.game.make_action(make_action({
                PlayerAction.rotateX: -how_to_rotate
        }))


        return False

class Section(IntEnum):
    Center = 0,
    Top = 1,
    Right = 2,
    Left = 3,
    Bottom = 4


class MoveTo(AbstractAction):
    
    access_map = None

    def __init__(self, game, directionMap, target_pos): 
        self.game = game
        self.map = directionMap
        self.target_pos = target_pos

    def do(self) -> bool:
        player = get_player(self.game)
        x = int(player.position_x)
        y = int(player.position_y)

        if self.map[(y,x)] < 10:
            return True        
            
        # RotateTo(self.game, 0).do_all() # 각도를 0으로            
        x_plus = (self.map[(y,x+1)] < self.map[(y,x)])
        x_minus = (self.map[(y,x-1)] < self.map[(y,x)]) and not x_plus 

        y_plus = self.map[(y+1,x)] < self.map[(y,x)]        
        y_minus = self.map[(y-1,x)] < self.map[(y,x)] and not y_plus

        xd = 1 if x_plus else (-1 if x_minus else 0)
        yd = 1 if y_plus else (-1 if y_minus else 0)
        # destination_angle = self.get_angle_from_direction(xd, yd)


        destination_angle = get_angle_from_player_to_direction(x, y, self.target_pos[0], self.target_pos[1]) # 글로벌 좌표공간에서 플레이어 위치와 목적지가 이루는 각도
        direct_destination_angle = self.get_angle_from_direction(xd, yd) # height map에 따른 움직여야 하는 방향
        # print(destination_angle)

        player_angle = player.angle
        
        # player_angle = StateData(self.game.get_state()).player.object.angle/
        
        relative_angle = ((direct_destination_angle-player_angle) + 360)%360 # 플레이어 기준에서 어느 방향으로 움직여야 하는가?
        # print(x, y, self.target_pos[0], self.target_pos[1], relative_angle)/
        # print(destination_angle)
        # print(relative_angle)
        direction = self.get_direction_from_angle(relative_angle)

        

        right = True if direction[0] == 1 else False
        left  = True if direction[0] == -1 else False

        front = True if direction[1] == 1 else False # xy좌표평면과 컴퓨터가 인식하는 y는 방향이 반대
        back  = True if direction[1] == -1 else False
        
        # print(self.get_angle_from_direction())


        angle = 0
        if keyboard.is_pressed("a"):    
            angle = -5
        elif keyboard.is_pressed("d"):
            angle = 5

        self.game.make_action(make_action({
            PlayerAction.Run: True,
            PlayerAction.MoveFront: front,
            PlayerAction.MoveBack: back,
            PlayerAction.MoveRight: right,
            PlayerAction.MoveLeft: left,
            PlayerAction.rotateX: angle
        }))

        # SmoothRotateTo(self.game, destination_angle).do()/

        print("x:%3d, y:%3d, dx:%3d, dy:%3d"%(x, y, self.target_pos[0], self.target_pos[1]))
        # print(destination_angle- get_player(self.game).angle)
        return False

    def get_angle_from_direction(self, x, y):
        # x, y방향으로 움직이는 여부를 가지고 이동 방향을 구한다.
        direction_list = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)] # (x, y) angle 0 부터 45도 단위로 증가

        cur_d = (x, y)
        for i, d in enumerate(direction_list):
            if cur_d == d:
                return i * 45
        
    def get_direction_from_angle(self, angle): # 플레이어 기준으로 angle방향으로 이동하기 위한 (좌우, 앞뒤) 이동 여부를 반환
        direction_list = [(0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1)]
        angle = round(angle/45)%8
        return direction_list[angle]


class MoveToSection(AbstractAction):

    map_dict = {}

    def __init__(self, game, section: Section):
        
        access_map = AccessMap(game)
        self.target_pos = MoveToSection.get_target_pos(section)
        direction_map = MoveToSection.get_direction_map(access_map, self.target_pos)
        self.moveTo = MoveTo(game, direction_map, self.target_pos)
        

    @staticmethod
    def get_direction_map(accessMap, target_pos):
        if target_pos not in MoveToSection.map_dict:    
            MoveToSection.map_dict[target_pos] = HeightMap(accessMap, target_pos)
        return MoveToSection.map_dict[target_pos]

    @staticmethod
    def get_target_pos(section): # (x, y)
        if section == Section.Center:
            return (600, 600)
        if section == Section.Top:
            return (600, 1200)
        if section == Section.Bottom:
            return (600, -100)
        if section == Section.Right:
            return (1200, 600)
        if section == Section.Left:
            return (-100, 600)

    def do(self):
        
        return self.moveTo.do()


