"""

if 체력 < 100:
 힐팩 존 가서 한 바퀴

else:
  힐팩존에 머물거나 또는
  힐팩 존 근처에서 전투
  확률적 
"""

from agent.agent import *
from state.vizdoom_state import *
from actioner.moving_actioner import *
from actioner.aim_actioner import *
from actioner.weaopn_actioner import * 

class MovementActioner(AbstractActioner):
    """
    체력 100이면 힐팩 존 내부나 근처에 머물고
    아니면 힐팩존 돌기
    또 확률적으로 건너편 힐팩존으로 건너가기
    """

    def __init__(self, game):
        super().__init__(game)
        pass 

    def add_action(self, stateData: StateAnalyzer, action_order_sheet: PlayerAction):
        pass

class 

