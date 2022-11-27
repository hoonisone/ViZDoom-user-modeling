from state.vizdoom_state import *
from actioner.moving_actioner import *
from actioner.aim_actioner import *
from actioner.weaopn_actioner import * 
from actioner.attackActioner import *
from agent.agent import *
import random

class AttackActioner(AbstractActioner):
    """
    * 적을 조준하고 있으면 공격
    * option1: 공격 사이에 time_threshold 만큼 간격 보장
    * option2: 적이 enemy_threshold 보다 많으면 무조건 공격
    * option3: 대상의 크기를 object_range_ratio만큼 키워서 공격 가능 여부 계산
    * option4: 대상의 크기에 관계 없이 화면 중간에 일정 범위 안에 있으면 공격
    """
    def __init__(self, game: vzd.DoomGame, cool_time = 0,  enemy_threshold = 5, object_range_ratio = 2, screen_range_ratio = 50):
        super().__init__(game)
        self.cool_time = cool_time
        self.last_atack_time = 0
        self.enemy_threshold = enemy_threshold
        self.object_range_ratio = object_range_ratio
        self.screen_range_ratio = screen_range_ratio

    def add_action(self, stateData: StateAnalyzer, action_order_sheet: PlayerAction):
        target_id = stateData.get_closest_enemy_label_id()
        
        flag = (target_id != None) and (stateData.is_in_shotting_effective_zone(target_id, self.object_range_ratio, self.screen_range_ratio))
        self.cool_time = 0 if flag else 0.1
        
        cur_time = time()
        if self.last_atack_time + self.cool_time > time(): return
            
        self.last_atack_time = max(self.last_atack_time + self.cool_time, cur_time)
        action_order_sheet[PlayerAction.Atack] = 1

class TacticalAgent(AbstractAgent):
    """
    * 중앙에서 힐팩 존 근처로 가서 들어간 뒤 한 바퀴 돌고 나오는 에이전트
    """
    def __init__(self, game):
        super().__init__(game)
        self.attack_actioner = AttackActioner(game, cool_time=1)
        self.aim_actioner = AimActioner(game)
        # self.movement_actioner = ThoroughlyVisitAllSector(game) # 힐팩 존 반복 방문 
        self.movement_actioner = RoughlyVisitAllSector(game)
        self.weapon_actioner = WeaponChangeActioner(game)
    
    def add_action(self, state: StateAnalyzer, action_order_sheet: PlayerAction):
        self.attack_actioner.add_action(state, action_order_sheet)
        self.aim_actioner.add_action(state, action_order_sheet)
        self.movement_actioner.add_action(state, action_order_sheet)
        self.weapon_actioner.add_action(state, action_order_sheet)

    def is_finished(self, state: StateAnalyzer) -> bool:
        return self.movement_actioner.is_finished(state)

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
                return CycledActioner(self.game, [lambda game : FarmingHealpackZone(game)]) # 힐팩 존 반복 방문 
            elif state == BalanceMovementActioner.State.WEAPON_ZONE:
                return CycledActioner(self.game, [lambda game : FarmingWeaponZone(game)]) # 힐팩 존 반복 방문 
            elif state == BalanceMovementActioner.State.CENTER:
                return CycledActioner(self.game, [lambda game : VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.MIDDLE , YPartition.MIDDLE))]) # 힐팩 존 반복 방문

    def update_state(self, stateAnalyzer: StateAnalyzer):
        state = self.calculate_state(stateAnalyzer)
        if self.state != state or self.actioner.is_finished(stateAnalyzer): # 스테이트가 변하거나 기존 에이전트가 종료될 때만 업데이트함
            self.actioner = self.get_state_agnet(state)
            self.state = state

    def add_action(self, stateAnalyzer: StateAnalyzer, action_order_sheet: PlayerAction):
        self.update_state(stateAnalyzer)
        self.actioner.add_action(stateAnalyzer, action_order_sheet)
        

CycledActioner(game, [lambda game : FarmingWeaponZone(game)]) # 힐팩 존 반복 방문 
 