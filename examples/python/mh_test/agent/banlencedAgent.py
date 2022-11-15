from state.vizdoom_state import *
from actioner.moving_actioner import *
from actioner.aim_actioner import *
from actioner.weaopn_actioner import * 
from agent.agent import *

class BalancedAgent(AbstractAgent):
    class State(IntEnum):
        HEALPACK_ZOME = auto()
        WEAPON_ZONE = auto()
        CENTER = auto()

    def __init__(self, game, health_threshold, weapon_ammo_threshold):
        super().__init__(game)
        self.actioner = WeaponFarmingAgent(game)
        self.health_threshold = health_threshold
        self.weapon_ammo_threshold = weapon_ammo_threshold
        self.state = BalanceMovementActioner.State.WEAPON_ZONE

    def calculate_state(self, stateAnalyzer: StateAnalyzer):
        if stateAnalyzer.get_player_hp() < self.health_threshold:
            return BalanceMovementActioner.State.HEALPACK_ZOME
        elif stateAnalyzer.get_cur_weapon_armor() < self.weapon_ammo_threshold:
            return BalanceMovementActioner.State.WEAPON_ZONE
        elif stateAnalyzer.get_weapon_possess()[3] == False:
            return BalanceMovementActioner.State.WEAPON_ZONE
        elif stateAnalyzer.get_weapon_possess()[4] == False:
            return BalanceMovementActioner.State.WEAPON_ZONE
        elif stateAnalyzer.get_weapon_possess()[6] == False:
            return BalanceMovementActioner.State.WEAPON_ZONE
        else:
            return BalanceMovementActioner.State.CENTER

    def get_state_agnet(self, state:State):
            if state == BalanceMovementActioner.State.HEALPACK_ZOME:
                return HealpackFarmingAgent(self.game)
            elif state == BalanceMovementActioner.State.WEAPON_ZONE:
                return WeaponFarmingAgent(self.game)
            elif state == BalanceMovementActioner.State.CENTER:
                return CenterStayAgent(self.game)

    def update_state(self, stateAnalyzer: StateAnalyzer):
        state = self.calculate_state(stateAnalyzer)
        if self.state != state or self.actioner.is_finished(stateAnalyzer): # 스테이트가 변하거나 기존 에이전트가 종료될 때만 업데이트함
            self.actioner = self.get_state_agnet(state)
            self.state = state

    def add_action(self, stateAnalyzer: StateAnalyzer, action_order_sheet: PlayerAction):
        self.update_state(stateAnalyzer)
        self.actioner.add_action(stateAnalyzer, action_order_sheet)
        
class BalancedAgent2(AbstractAgent):
    class State(IntEnum):
        HEALPACK_ZOME = auto()
        WEAPON_ZONE = auto()
        CENTER = auto()

    def __init__(self, game, health_threshold, weapon_ammo_threshold):
        super().__init__(game)
        self.actioner = WeaponFarmingAgent(game)
        self.health_threshold = health_threshold
        self.weapon_ammo_threshold = weapon_ammo_threshold
        self.state = BalanceMovementActioner.State.WEAPON_ZONE

    def calculate_state(self, stateAnalyzer: StateAnalyzer):
        if stateAnalyzer.get_player_hp() < self.health_threshold:
            return BalanceMovementActioner.State.HEALPACK_ZOME
        elif stateAnalyzer.get_cur_weapon_armor() < self.weapon_ammo_threshold:
            return BalanceMovementActioner.State.WEAPON_ZONE
        elif stateAnalyzer.get_weapon_possess()[3] == False:
            return BalanceMovementActioner.State.WEAPON_ZONE
        elif stateAnalyzer.get_weapon_possess()[4] == False:
            return BalanceMovementActioner.State.WEAPON_ZONE
        elif stateAnalyzer.get_weapon_possess()[6] == False:
            return BalanceMovementActioner.State.WEAPON_ZONE
        else:
            return BalanceMovementActioner.State.CENTER

    def get_state_agnet(self, state:State):
            if state == BalanceMovementActioner.State.HEALPACK_ZOME:
                return HealpackFarmingAgent(self.game)
            elif state == BalanceMovementActioner.State.WEAPON_ZONE:
                return WeaponFarmingAgent(self.game)
            elif state == BalanceMovementActioner.State.CENTER:
                return CenterStayAgent(self.game)

    def update_state(self, stateAnalyzer: StateAnalyzer):
        state = self.calculate_state(stateAnalyzer)
        if self.state != state or self.actioner.is_finished(stateAnalyzer): # 스테이트가 변하거나 기존 에이전트가 종료될 때만 업데이트함
            self.actioner = self.get_state_agnet(state)
            self.state = state

    def add_action(self, stateAnalyzer: StateAnalyzer, action_order_sheet: PlayerAction):
        self.update_state(stateAnalyzer)
        self.actioner.add_action(stateAnalyzer, action_order_sheet)

class DefensiveAgent(AbstractAgent):
    def __init__(self, game: vzd.DoomGame):
        super().__init__(game)
        self.actioner = BalancedAgent(game, 100, 100)
    
    def add_action(self, state: StateAnalyzer, action_order_sheet: PlayerAction):
        self.actioner.add_action(state, action_order_sheet)

class AggressiveAgent(AbstractAgent):
    def __init__(self, game: vzd.DoomGame):
        super().__init__(game)
        self.actioner = BalancedAgent(game, 50, 100)
    
    def add_action(self, state: StateAnalyzer, action_order_sheet: PlayerAction):
        self.actioner.add_action(state, action_order_sheet)

class AimerAgent(AbstractActioner):
    def __init__(self, game: vzd.DoomGame):
        super().__init__(game)
        self.actioner = BalancedAgent(game, 0, 100)
    
    def add_action(self, state: StateAnalyzer, action_order_sheet: PlayerAction):
        self.actioner.add_action(state, action_order_sheet)