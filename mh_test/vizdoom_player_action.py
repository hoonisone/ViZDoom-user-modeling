
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
                RotateTo(self.game, 0).do_all() # 각도를 0으로            
                right = self.map[(y-1,x)] < self.map[(y,x)]
                left = self.map[(y+1,x)] < self.map[(y,x)] and not right
                front = (self.map[(y,x+1)] < self.map[(y,x)])
                back = (self.map[(y,x-1)] < self.map[(y,x)]) and not front

                self.game.make_action(make_action({
                    PlayerAction.Run: True,
                    PlayerAction.MoveFront: front,
                    PlayerAction.MoveBack: back,
                    PlayerAction.MoveRight: right,
                    PlayerAction.MoveLeft: left
                }))
                return False

class MoveToSection(AbstractAction):

    map_dict = {}

    def __init__(self, game, section: Section):
        
        access_map = AccessMap(game)
        access_map.show()
        direction_map = MoveToSection.get_direction_map(access_map, section)
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
