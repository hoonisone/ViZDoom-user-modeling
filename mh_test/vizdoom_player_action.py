
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

class Section(IntEnum):
    Center = 0,
    Top = 1,
    Right = 2,
    Left = 3,
    Bottom = 4


class MoveTo(AbstractAction):
    
    access_map = None

    def __init__(self, game, directionMap): 
        self.game = game
        self.map = directionMap

    def do(self) -> bool:
        while True:
            stateData = StateData(self.game.get_state())
            x = int(stateData.player.pos[0])
            y = int(stateData.player.pos[1])
            
            if self.map[(y,x)] < 10:
                return True
            else:
                # RotateTo(self.game, 0).do_all() # 각도를 0으로            
                right = self.map[(y-1,x)] < self.map[(y,x)]
                left = self.map[(y+1,x)] < self.map[(y,x)] and not right
                front = (self.map[(y,x+1)] < self.map[(y,x)])
                back = (self.map[(y,x-1)] < self.map[(y,x)]) and not front

                xd = 1 if right else (-1 if left else 0)
                yd = 1 if front else (-1 if back else 0)
                destination_angle = self.get_angle_from_direction(xd, yd)
                player_angle = StateData(self.game.get_state()).player.object.angle
                relative_angle = ((destination_angle-player_angle) + 360)%360

                direction = self.get_direction_from_angle(relative_angle)

                right = True if direction[0] == 1 else False
                left = True if direction[0] == -1 else False

                front = True if direction[1] == 1 else False
                back = True if direction[1] == -1 else False
                
                
                # print(self.get_angle_from_direction())

                self.game.make_action(make_action({
                    PlayerAction.Run: True,
                    PlayerAction.MoveFront: front,
                    PlayerAction.MoveBack: back,
                    PlayerAction.MoveRight: right,
                    PlayerAction.MoveLeft: left
                }))
                return False

    def get_angle_from_direction(self, x, y):
        # x, y방향으로 움직이는 여부를 가지고 이동 방향을 구한다.
        direction_list = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)] # (x, y) angle 0 부터 45도 단위로 증가



        cur_d = (x, y)
        for i, d in enumerate(direction_list):
            if cur_d == d:
                return i * 45
        return 0 # 여기까지 올 일은 없지만 일단 작성함

    def get_direction_from_angle(self, angle):
        direction_list = [(1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1)]
        angle = round(angle/45)
        return direction_list[angle]


class MoveToSection(AbstractAction):

    map_dict = {}

    def __init__(self, game, section: Section):
        
        access_map = AccessMap(game)
        direction_map = MoveToSection.get_direction_map(access_map, section)
        direction_map.show()

        self.moveTo = MoveTo(game, direction_map)
        

    @staticmethod
    def get_direction_map(accessMap, section):
        if section not in MoveToSection.map_dict:
            target_pos = MoveToSection.get_target_pos(section)
            MoveToSection.map_dict[section] = HeightMap(accessMap, target_pos)

        return MoveToSection.map_dict[section]

    @staticmethod
    def get_target_pos(section):
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


