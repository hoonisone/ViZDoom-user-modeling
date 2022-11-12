
from email.charset import add_alias
from abc import abstractmethod
from deathmatch import *

from draw_map import *
from vizdoom_object_data import *
from time import time
import vizdoom as vzd
import random


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

    @ abstractmethod
    def init(self) -> None:
        pass

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

class RandomActioner(AbstractActioner):
    def __init__(self, game: vzd.DoomGame, actioner_list:list):
        super().__init__(game)
        self.actioner_list = actioner_list
        self.actinoer = None
        self.set_new_actioner()

    def set_new_actioner(self):
        idx = random.randrange(len(self.actioner_list))
        self.actinoer = self.actioner_list[idx](self.game)

    def add_action(self, stateData: StateData2, action_order_sheet: PlayerAction):
        if self.actinoer.is_finished(stateData):
            self.set_new_actioner()
        self.actinoer.add_action(stateData, action_order_sheet)



class SequentialActioner(AbstractActioner):
    def __init__(self, game: vzd.DoomGame, actioner_list:list):
        super().__init__(game)
        self.actioner_list = actioner_list
        self.idx = -1
        self.sub_actioner = None
        self._is_finished = False
        self.set_next_actioner()

    def set_next_actioner(self):
        self.idx += 1
        if self.idx == len(self.actioner_list):
            self._is_finished = True
            return

        self.sub_actioner = self.actioner_list[self.idx]

    def add_action(self, stateData: StateData2, action_order_sheet: PlayerAction):
        if self._is_finished: # 수행할 게 없음
            return

        if self.sub_actioner.is_finished(stateData):
            self.set_next_actioner()
        
        self.sub_actioner.add_action(stateData, action_order_sheet)

    def is_finished(self, stateData: StateData2) -> bool:
        return self._is_finished

    def init(self) -> None:
        for actioner in self.actioner_list:
            actioner.init()

        self.idx = -1
        self.sub_actioner = None
        self._is_finished = False
        self.set_next_actioner()
        return super().init()
        
class CycledActioner(AbstractActioner):
    def __init__(self, game:vzd.DoomGame, actioner_list:list):
        super().__init__(game)  
        self.sequentialVisitActioner = SequentialActioner(self.game, actioner_list)

    def add_action(self, stateData: StateData2, action_order_sheet: PlayerAction):
        if self.sequentialVisitActioner.is_finished(stateData): # 끝나면 다시시작
            self.sequentialVisitActioner.init()

        self.sequentialVisitActioner.add_action(stateData, action_order_sheet)

