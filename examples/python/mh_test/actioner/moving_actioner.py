import vizdoom as vzd
from actioner.actioner import *
from deathmatch import *
from draw_map import *
import random

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
        

        action_order_sheet[PlayerAction.Run] = True #False
        action_order_sheet[PlayerAction.MoveFront] = front
        action_order_sheet[PlayerAction.MoveBack] = back
        action_order_sheet[PlayerAction.MoveRight] = right
        action_order_sheet[PlayerAction.MoveLeft] = left


        map_pos = self.map.access_map.get_map_pos((x, y))



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
        return self.map[(y,x)] < 20

class VisitActioner(MoveToActioner):

    access_map = None
    direction_map_dict = {}

    def __init__(self, game: vzd.DoomGame, position ):

        if VisitActioner.access_map is None:
            VisitActioner.access_map = AccessMap(game)

        if position not in VisitActioner.direction_map_dict:
            VisitActioner.direction_map_dict[position] = HeightMap(VisitActioner.access_map, position)

        super().__init__(game, VisitActioner.direction_map_dict[position], position)

class FarmingWeaponZone(SequentialActioner):
    path1 = [
        lambda game : VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.LEFT , YPartition.TOP)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.TOP_PESSAGE, XPartition.LEFT , YPartition.MIDDLE)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.TOP, XPartition.LEFT, YPartition.BOTTOM)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.TOP, XPartition.RIGHT, YPartition.BOTTOM)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.TOP, XPartition.RIGHT, YPartition.TOP)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.TOP, XPartition.LEFT, YPartition.TOP)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.TOP, XPartition.LEFT, YPartition.BOTTOM)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.TOP_PESSAGE, XPartition.LEFT , YPartition.MIDDLE)),
    ]

    path2 = [
        lambda game : VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.MIDDLE , YPartition.TOP)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.TOP_PESSAGE, XPartition.MIDDLE , YPartition.MIDDLE)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.TOP, XPartition.MIDDLE , YPartition.BOTTOM)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.TOP, XPartition.RIGHT, YPartition.BOTTOM)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.TOP, XPartition.RIGHT, YPartition.TOP)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.TOP, XPartition.LEFT, YPartition.TOP)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.TOP, XPartition.LEFT, YPartition.BOTTOM)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.TOP, XPartition.MIDDLE, YPartition.BOTTOM)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.TOP_PESSAGE, XPartition.MIDDLE, YPartition.MIDDLE))
    ]

    path3 = [
        lambda game : VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.RIGHT , YPartition.TOP)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.TOP_PESSAGE, XPartition.RIGHT , YPartition.MIDDLE)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.TOP, XPartition.RIGHT , YPartition.BOTTOM)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.TOP, XPartition.RIGHT, YPartition.TOP)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.TOP, XPartition.LEFT, YPartition.TOP)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.TOP, XPartition.LEFT, YPartition.BOTTOM)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.TOP, XPartition.RIGHT, YPartition.BOTTOM)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.TOP_PESSAGE, XPartition.MIDDLE, YPartition.MIDDLE))
    ]
    path4 = [
        lambda game : VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.LEFT , YPartition.BOTTOM)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.BOTTOM_PESSAGE, XPartition.LEFT , YPartition.MIDDLE)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.BOTTOM, XPartition.LEFT, YPartition.TOP)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.BOTTOM, XPartition.RIGHT, YPartition.TOP)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.BOTTOM, XPartition.RIGHT, YPartition.BOTTOM)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.BOTTOM, XPartition.LEFT, YPartition.BOTTOM)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.BOTTOM, XPartition.LEFT, YPartition.TOP)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.BOTTOM_PESSAGE, XPartition.LEFT , YPartition.MIDDLE)),
    ]

    path5 = [
        lambda game : VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.MIDDLE , YPartition.BOTTOM)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.BOTTOM_PESSAGE, XPartition.MIDDLE , YPartition.MIDDLE)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.BOTTOM, XPartition.MIDDLE , YPartition.TOP)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.BOTTOM, XPartition.RIGHT, YPartition.TOP)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.BOTTOM, XPartition.RIGHT, YPartition.BOTTOM)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.BOTTOM, XPartition.LEFT, YPartition.BOTTOM)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.BOTTOM, XPartition.LEFT, YPartition.TOP)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.BOTTOM, XPartition.MIDDLE, YPartition.TOP)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.BOTTOM_PESSAGE, XPartition.MIDDLE, YPartition.MIDDLE))
    ]

    path6 = [
        lambda game : VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.RIGHT , YPartition.BOTTOM)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.BOTTOM_PESSAGE, XPartition.RIGHT , YPartition.MIDDLE)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.BOTTOM, XPartition.RIGHT , YPartition.TOP)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.BOTTOM, XPartition.RIGHT, YPartition.BOTTOM)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.BOTTOM, XPartition.LEFT, YPartition.BOTTOM)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.BOTTOM, XPartition.LEFT, YPartition.TOP)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.BOTTOM, XPartition.RIGHT, YPartition.TOP)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.BOTTOM_PESSAGE, XPartition.MIDDLE, YPartition.MIDDLE))
    ]

    path_list = [path1, path2, path3, path4, path5, path6]

    def __init__(self, game):
        path = FarmingWeaponZone.path_list[random.randrange(len(FarmingWeaponZone.path_list))]
        super().__init__(game, path)

class FarmingHealpackZone(SequentialActioner):
    path1 = [
        lambda game : VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.LEFT , YPartition.TOP)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.LEFT_PESSAGE, XPartition.MIDDLE , YPartition.TOP)), # 입구로 가서
        lambda game : VisitActioner(game, MapPos.get_pos(Section.LEFT, XPartition.RIGHT, YPartition.TOP)),          # 돌고
        lambda game : VisitActioner(game, MapPos.get_pos(Section.LEFT, XPartition.LEFT, YPartition.TOP)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.LEFT, XPartition.LEFT, YPartition.BOTTOM)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.LEFT, XPartition.RIGHT, YPartition.BOTTOM)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.LEFT, XPartition.RIGHT, YPartition.TOP)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.LEFT_PESSAGE, XPartition.MIDDLE , YPartition.TOP)), # 동일 입구로 가기
        lambda game : VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.LEFT , YPartition.TOP)),
    ]

    path2 = [
        lambda game : VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.LEFT , YPartition.MIDDLE)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.LEFT_PESSAGE, XPartition.MIDDLE , YPartition.MIDDLE)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.LEFT, XPartition.RIGHT , YPartition.MIDDLE)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.LEFT, XPartition.RIGHT, YPartition.TOP)), 
        lambda game : VisitActioner(game, MapPos.get_pos(Section.LEFT, XPartition.LEFT, YPartition.TOP)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.LEFT, XPartition.LEFT, YPartition.BOTTOM)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.LEFT, XPartition.RIGHT, YPartition.BOTTOM)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.LEFT, XPartition.RIGHT , YPartition.MIDDLE)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.LEFT_PESSAGE, XPartition.MIDDLE, YPartition.MIDDLE)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.LEFT , YPartition.MIDDLE)),
    ]

    path3 = [
        lambda game : VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.LEFT , YPartition.BOTTOM)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.LEFT_PESSAGE, XPartition.MIDDLE , YPartition.BOTTOM)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.LEFT, XPartition.RIGHT, YPartition.BOTTOM)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.LEFT, XPartition.RIGHT, YPartition.TOP)), 
        lambda game : VisitActioner(game, MapPos.get_pos(Section.LEFT, XPartition.LEFT, YPartition.TOP)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.LEFT, XPartition.LEFT, YPartition.BOTTOM)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.LEFT, XPartition.RIGHT, YPartition.BOTTOM)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.LEFT_PESSAGE, XPartition.MIDDLE, YPartition.BOTTOM)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.LEFT , YPartition.BOTTOM)),
    ]
    path4 = [
        lambda game : VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.RIGHT , YPartition.TOP)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.RIGHT_PESSAGE, XPartition.MIDDLE , YPartition.TOP)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.RIGHT, XPartition.LEFT, YPartition.TOP)), 
        lambda game : VisitActioner(game, MapPos.get_pos(Section.RIGHT, XPartition.RIGHT, YPartition.TOP)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.RIGHT, XPartition.RIGHT, YPartition.BOTTOM)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.RIGHT, XPartition.LEFT, YPartition.BOTTOM)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.RIGHT, XPartition.LEFT, YPartition.TOP)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.RIGHT_PESSAGE, XPartition.MIDDLE , YPartition.TOP)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.RIGHT , YPartition.TOP)),
    ]

    path5 = [
        lambda game : VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.RIGHT , YPartition.MIDDLE)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.RIGHT_PESSAGE, XPartition.MIDDLE , YPartition.MIDDLE)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.RIGHT, XPartition.LEFT , YPartition.MIDDLE)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.RIGHT, XPartition.LEFT, YPartition.TOP)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.RIGHT, XPartition.RIGHT, YPartition.TOP)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.RIGHT, XPartition.RIGHT, YPartition.BOTTOM)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.RIGHT, XPartition.LEFT, YPartition.BOTTOM)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.RIGHT, XPartition.LEFT , YPartition.MIDDLE)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.RIGHT_PESSAGE, XPartition.MIDDLE, YPartition.MIDDLE)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.RIGHT , YPartition.MIDDLE)),
    ]

    path6 = [
        lambda game : VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.RIGHT , YPartition.BOTTOM)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.RIGHT_PESSAGE, XPartition.MIDDLE , YPartition.BOTTOM)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.RIGHT, XPartition.LEFT, YPartition.BOTTOM)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.RIGHT, XPartition.LEFT, YPartition.TOP)), 
        lambda game : VisitActioner(game, MapPos.get_pos(Section.RIGHT, XPartition.RIGHT, YPartition.TOP)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.RIGHT, XPartition.RIGHT, YPartition.BOTTOM)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.RIGHT, XPartition.LEFT, YPartition.BOTTOM)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.RIGHT_PESSAGE, XPartition.MIDDLE, YPartition.BOTTOM)),
        lambda game : VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.RIGHT , YPartition.BOTTOM)),
    ]

    path_list = [path1, path2, path3, path4, path5, path6]

    def __init__(self, game):
        path = FarmingHealpackZone.path_list[random.randrange(len(FarmingHealpackZone.path_list))]
        super().__init__(game, path)

class StayCenter(RandomActioner):
    """
        * 중앙 지역 거점 9 + 8개를 랜덤으로 이동
    """
    actioner_list = [
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.LEFT , YPartition.TOP),),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.LEFT , YPartition.TOP)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.LEFT , YPartition.TOP)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.LEFT , YPartition.MIDDLE)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.LEFT , YPartition.MIDDLE)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.LEFT , YPartition.MIDDLE)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.LEFT , YPartition.BOTTOM)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.LEFT , YPartition.BOTTOM)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.LEFT , YPartition.BOTTOM)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.MIDDLE , YPartition.TOP)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.MIDDLE , YPartition.TOP)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.MIDDLE , YPartition.TOP)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.MIDDLE , YPartition.MIDDLE)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.MIDDLE , YPartition.MIDDLE)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.MIDDLE , YPartition.MIDDLE)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.MIDDLE , YPartition.BOTTOM)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.MIDDLE , YPartition.BOTTOM)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.MIDDLE , YPartition.BOTTOM)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.RIGHT , YPartition.TOP)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.RIGHT , YPartition.TOP)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.RIGHT , YPartition.TOP)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.RIGHT , YPartition.MIDDLE)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.RIGHT , YPartition.MIDDLE)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.RIGHT , YPartition.MIDDLE)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.RIGHT , YPartition.BOTTOM)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.RIGHT , YPartition.BOTTOM)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.RIGHT , YPartition.BOTTOM)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER2, XPartition.LEFT , YPartition.TOP)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER2, XPartition.LEFT , YPartition.TOP)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER2, XPartition.LEFT , YPartition.TOP)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER2, XPartition.LEFT , YPartition.MIDDLE)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER2, XPartition.LEFT , YPartition.MIDDLE)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER2, XPartition.LEFT , YPartition.MIDDLE)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER2, XPartition.LEFT , YPartition.BOTTOM)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER2, XPartition.LEFT , YPartition.BOTTOM)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER2, XPartition.LEFT , YPartition.BOTTOM)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER2, XPartition.MIDDLE , YPartition.TOP)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER2, XPartition.MIDDLE , YPartition.TOP)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER2, XPartition.MIDDLE , YPartition.TOP)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER2, XPartition.MIDDLE , YPartition.MIDDLE)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER2, XPartition.MIDDLE , YPartition.MIDDLE)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER2, XPartition.MIDDLE , YPartition.MIDDLE)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER2, XPartition.MIDDLE , YPartition.BOTTOM)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER2, XPartition.MIDDLE , YPartition.BOTTOM)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER2, XPartition.MIDDLE , YPartition.BOTTOM)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER2, XPartition.RIGHT , YPartition.TOP)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER2, XPartition.RIGHT , YPartition.TOP)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER2, XPartition.RIGHT , YPartition.TOP)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER2, XPartition.RIGHT , YPartition.MIDDLE)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER2, XPartition.RIGHT , YPartition.MIDDLE)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER2, XPartition.RIGHT , YPartition.MIDDLE)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER2, XPartition.RIGHT , YPartition.BOTTOM)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER2, XPartition.RIGHT , YPartition.BOTTOM)),
        lambda game: VisitActioner(game, MapPos.get_pos(Section.CENTER2, XPartition.RIGHT , YPartition.BOTTOM)),
    ]

    def __init__(self, game):
        super().__init__(game, StayCenter.actioner_list)