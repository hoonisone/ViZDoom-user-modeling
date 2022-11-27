import vizdoom as vzd
from actioner.deathmatch_pos import *
from state.vizdoom_state import *
from actioner.actioner import * 


class AttackActioner2(AbstractActioner):
    """
    * 적을 조준하고 있으면 공격
    * option1: 공격 사이에 time_threshold 만큼 간격 보장
    * option2: 적이 enemy_threshold 보다 많으면 무조건 공격
    * option3: 대상의 크기를 object_range_ratio만큼 키워서 공격 가능 여부 계산
    * option4: 대상의 크기에 관계 없이 화면 중간에 일정 범위 안에 있으면 공격
    """
    def __init__(self, game: vzd.DoomGame, cool_time = 0,  enemy_threshold = 5, object_range_ratio = 2, screen_range_ratio = 50):
        super().__init__(game)

        # option1
        self.cool_time = cool_time
        self.last_atack_time = 0

        # option2
        self.enemy_threshold = enemy_threshold

        # option3
        self.object_range_ratio = object_range_ratio

        # option4
        self.screen_range_ratio = screen_range_ratio

    def add_action(self, stateData: StateAnalyzer, action_order_sheet: PlayerAction):
        # option1
        cur_time = time()
        #print("cur: ", cur_time, "thresh: ", self.last_atack_time + self.cool_time)
        if self.last_atack_time + self.cool_time > cur_time: # 쿨타임 안지남
            return

        #print("쏘기")
        self.last_atack_time = max(self.last_atack_time + self.cool_time, cur_time)

        # option2
        if self.enemy_threshold != None:
            if stateData.get_enemy_count() >= self.enemy_threshold: # 적이 임계치 보다 많으면
                action_order_sheet[PlayerAction.Atack] = 1
                #print("쏘기A")
                return

        # default
        target_id = stateData.get_closest_enemy_label_id() # 가장 가까운 적 구하기
        if target_id is None:
            #print("탈락")
            return

        if stateData.is_in_shotting_effective_zone(target_id, self.object_range_ratio, self.screen_range_ratio):# 쏠 수 있으면 공격
            action_order_sheet[PlayerAction.Atack] = 1
            #print("쏘기B")
            return

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