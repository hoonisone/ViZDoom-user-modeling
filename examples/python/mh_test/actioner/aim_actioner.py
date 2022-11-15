import vizdoom as vzd
import math
from actioner.deathmatch_pos import *
from state.vizdoom_state import *
from actioner.actioner import * 

import random

class AimActioner(AbstractActioner):
    """
    바라보는 시선 컨트롤 agent
    * option1: aim speed => frame당 rotate_ratio만큼 이동
    * option2: large_doridori => 적이 많으면 도리도리(크게) - doridori_enemy_count_threshold
    * option3: clairvoyance => 벽 투시 (화면에 안보여도 조준) 아니면 랜덤으로 아무데나 바라봄
    * option4: small_doridori => 적 조준시 약간 도리도리(작게) 
    * option5
    """
    def __init__(self, game: vzd.DoomGame, 
        # option1
        rotate_ratio=0.90, 
        # option2
        large_doridori = True,
        enemy_threshold = 5,
        large_doridori_speed = 1,
        large_doridori_range = 30,
        # option3
        clairvoyance = True, 
        random_aim_change_p = 0.01,
        # option4
        small_doridori = True,
        small_doridori_speed = 5,
        small_doridori_range = 1,
    
    ):
        super().__init__(game)

        # option2
        self.rotate_ratio = rotate_ratio
        # option2
        self.large_doridori = large_doridori
        self.enemy_threshold = enemy_threshold
        self.large_doridori_speed = large_doridori_speed
        self.large_doridori_range = large_doridori_range
        # option3
        self.clairvoyance = clairvoyance
        self.random_aim_change_p = random_aim_change_p
        # option4
        self.small_doridori = small_doridori
        self.small_doridori_speed = small_doridori_speed
        self.small_doridori_range = small_doridori_range
        # actioner
        self.large_doridori_actioner = DoriDoriActioner(game, large_doridori_speed, large_doridori_speed)
        self.closest_enomy_aim_actioner = ClosestEnomyAimActioner(game, rotate_ratio = self.rotate_ratio)
        self.random_pos_fixation_actioner = RandomPosFixationAction_V1(game, rotate_ratio = self.rotate_ratio, change_p = random_aim_change_p)
        self.visible_closest_nomy_aim_actioner = VisibleClosestEnomyAimActioner(game, rotate_ratio = self.rotate_ratio, doridori_speed = self.small_doridori_speed, doridori_range = self.small_doridori_range)
                


    def add_action(self, state: StateAnalyzer, action_order_sheet: PlayerAction):            
        if state.is_enemy_exist_in_screen(): # 적이 보이면
            self.visible_closest_nomy_aim_actioner.add_action(state, action_order_sheet)
            if state.get_enemy_count() > self.enemy_threshold: # 적이 많으면
                self.large_doridori_actioner.add_action(state, action_order_sheet)
            
        elif state.is_enemy_exist_in_game(): # 적이 있으면
            if self.clairvoyance: # 투시가 가능하면
                self.closest_enomy_aim_actioner.add_action(state, action_order_sheet) # 투시하여 최근접 적 조준
            else: # 불가하면
                self.random_pos_fixation_actioner.add_action(state, action_order_sheet) # 랜덤으로 아무데나 보기

        
        
        
class PosFixationActioner(AbstractActioner):
    """
    특정 위치를 바라본다.
    * option1: aim speed => frame당 rotate_ratio만큼 이동
    """
    def __init__(self, game: vzd.DoomGame, target_pos:tuple, rotate_ratio=0.1):
        super().__init__(game)
        self.target_pos = target_pos
        self.rotate_ratio = rotate_ratio

    def add_action(self, stateData: StateAnalyzer, action_order_sheet: PlayerAction):
        (x, y) = stateData.get_player_pos()
        (tx, ty) = self.target_pos
        r_x, r_y = tx-x, ty-y
        angle = stateData.get_player().angle
    
        if r_x == 0: return

        theta = math.atan((r_y)/(r_x))

        if (r_x<0): # 정의역 예외 처리
            theta += math.pi

        theta = theta*180/math.pi # 라다안 -> 도
        if theta < 0:
            theta += 360

        rotate = theta - angle  # 조준을 위해 필요한 angle 변화량
        
        if rotate > 180:
            rotate -= 360  
        if rotate < -180:
            rotate += 360
        action_order_sheet[PlayerAction.rotateX] = -rotate*self.rotate_ratio


class RandomPosFixationAction(AbstractActioner):
    def __init__(self, game: vzd.DoomGame, target_pos_list:list, rotate_ratio:float, change_p:float):
        super().__init__(game)
        self.rotate_ratio = rotate_ratio
        self.target_pos_list = target_pos_list
        self.change_p = change_p
        self.change_sub_actioner()

    def add_action(self, stateData: StateAnalyzer, action_order_sheet: PlayerAction):
        if random.random() < self.change_p:
            self.change_sub_actioner()
        self.sub_actioner.add_action(stateData, action_order_sheet)    

    def change_sub_actioner(self):
        pos = self.target_pos_list[random.randrange(len(self.target_pos_list))]
        self.sub_actioner = PosFixationActioner(self.game, pos, rotate_ratio = self.rotate_ratio)

class RandomPosFixationAction_V1(RandomPosFixationAction):
    def __init__(self, game: vzd.DoomGame, rotate_ratio = 0.1, change_p =  0.01, ):
        pos_list = [
            MapPos.get_pos(Section.TOP_PESSAGE, XPartition.LEFT, YPartition.MIDDLE),
            MapPos.get_pos(Section.TOP_PESSAGE, XPartition.MIDDLE, YPartition.MIDDLE),
            MapPos.get_pos(Section.TOP_PESSAGE, XPartition.RIGHT, YPartition.MIDDLE),

            MapPos.get_pos(Section.BOTTOM_PESSAGE, XPartition.LEFT, YPartition.MIDDLE),
            MapPos.get_pos(Section.BOTTOM_PESSAGE, XPartition.MIDDLE, YPartition.MIDDLE),
            MapPos.get_pos(Section.BOTTOM_PESSAGE, XPartition.RIGHT, YPartition.MIDDLE),
            MapPos.get_pos(Section.CENTER2, XPartition.LEFT, YPartition.TOP),
            MapPos.get_pos(Section.CENTER2, XPartition.LEFT, YPartition.MIDDLE),
            MapPos.get_pos(Section.CENTER2, XPartition.LEFT, YPartition.BOTTOM),
            MapPos.get_pos(Section.CENTER2, XPartition.MIDDLE, YPartition.TOP),
            MapPos.get_pos(Section.CENTER2, XPartition.MIDDLE, YPartition.MIDDLE),
            MapPos.get_pos(Section.CENTER2, XPartition.MIDDLE, YPartition.BOTTOM),
            MapPos.get_pos(Section.CENTER2, XPartition.RIGHT, YPartition.TOP),
            MapPos.get_pos(Section.CENTER2, XPartition.RIGHT, YPartition.MIDDLE),
            MapPos.get_pos(Section.CENTER2, XPartition.RIGHT, YPartition.BOTTOM),
        ]
        super().__init__(game, pos_list, change_p =  change_p, rotate_ratio = rotate_ratio)

class DoriDoriActioner(AbstractActioner):
    # 현재 바라보고 있는 방향 기준 좌우로 도리도리
    
    def __init__(self, game: vzd.DoomGame, speed = 1, range = 30):
        super().__init__(game)
        self.speed = speed
        self.range = range

    def add_action(self, stateData: StateAnalyzer, action_order_sheet: PlayerAction) -> None:
        action_order_sheet[PlayerAction.rotateX] += self.range*math.sin(self.speed*time())

class ClosestEnomyAimActioner(AbstractActioner):
    """
    * 모든 적 중에 가장 가까운 오브젝트를 바라본다.
    * option1: aim speed => frame당 rotate_ratio만큼 이동
    """
    def __init__(self, game: vzd.DoomGame, rotate_ratio = 0.1):
        super().__init__(game)
        self.actioner = PosFixationActioner(game, (0, 0), rotate_ratio = rotate_ratio)

    def add_action(self, stateData: StateAnalyzer, action_order_sheet: PlayerAction):
        target_id = stateData.get_closest_enemy_object_id()
        if target_id != None:
            self.actioner.target_pos = stateData.get_object_pos(target_id)    
            
        self.actioner.add_action(stateData, action_order_sheet)

class VisibleClosestEnomyAimActioner(AbstractActioner):
    """
    * 화면에 보이는 적 중에 가장 가까운 오브젝트를 바라본다.
    * option1: aim speed => frame당 rotate_ratio만큼 이동
    """
    def __init__(self, game: vzd.DoomGame, rotate_ratio = 0.1, doridori = True, doridori_speed = 1, doridori_range = 1):
        super().__init__(game)
        self.actioner = PosFixationActioner(game, (0, 0), rotate_ratio = rotate_ratio)
        self.doridori = doridori
        self.doridori_actioner = DoriDoriActioner(game, doridori_speed, doridori_range)

    def add_action(self, stateData: StateAnalyzer, action_order_sheet: PlayerAction):
        target_id = stateData.get_closest_enemy_label_id()
        if target_id != None:
            self.actioner.target_pos = stateData.get_object_pos(target_id)    
            
        self.actioner.add_action(stateData, action_order_sheet)
        if self.doridori:
            self.doridori_actioner.add_action(stateData, action_order_sheet)




