from enum import IntEnum, auto

class Section(IntEnum):

    # 구역
    TOP = auto()
    BOTTOM = auto()
    LEFT = auto()
    RIGHT = auto()
    CENTER1 = auto() # 센터 전체
    CENTER2 = auto() # 센터의 중앙 부분 (너무 구석으로 가지 않기 위함)

    TOP_PESSAGE = auto()
    BOTTOM_PESSAGE = auto()
    LEFT_PASSAGE = auto()
    RIGHT_PASSAGE = auto()
    
class XPartition(IntEnum):
    LEFT = 0
    MIDDLE = 1
    RIGHT = 2

class YPartition(IntEnum):
    TOP = 3
    MIDDLE = 4
    BOTTOM = 5

class MapPos:
    TOP_X_L = 50
    TOP_X_R = 980
    TOP_X_C = (TOP_X_L + TOP_X_R)/2
    TOP_Y_T = 1260
    TOP_Y_B = 1115
    TOP_Y_C = (TOP_Y_T + TOP_Y_B)/2

    BOTTOM_X_L = TOP_X_L
    BOTTOM_X_R = TOP_X_R
    BOTTOM_X_C = TOP_X_C
    BOTTOM_Y_T = TOP_Y_T-1350
    BOTTOM_Y_B = TOP_Y_B-1350
    BOTTOM_Y_C = TOP_Y_C-1350

    LEFT_X_L = -240
    LEFT_X_R = -80
    LEFT_X_C = (LEFT_X_L + LEFT_X_R)/2
    LEFT_Y_T = 980
    LEFT_Y_B = 50
    LEFT_Y_C = (LEFT_Y_T + LEFT_Y_B)/2

    RIGHT_X_L = LEFT_X_L + 1335
    RIGHT_X_C = LEFT_X_C + 1335
    RIGHT_X_R = LEFT_X_R + 1335
    RIGHT_Y_T = LEFT_Y_T
    RIGHT_Y_C = LEFT_Y_C
    RIGHT_Y_B = LEFT_Y_B

    CENTER_X_L = 20
    CENTER_X_R = 1005
    CENTER_X_C = (CENTER_X_L + CENTER_X_R)/2
    CENTER_Y_T = 1000
    CENTER_Y_B = 30
    CENTER_Y_C = (CENTER_Y_T + CENTER_Y_B)/2

    # 입구 좌표
    TOP_PESSAGE_X_L = 210
    TOP_PESSAGE_X_R = 820
    TOP_PESSAGE_X_C = (TOP_PESSAGE_X_L + TOP_PESSAGE_X_R)/2
    TOP_PESSAGE_Y = 1060

    BOTTOM_PESSAGE_X_L = TOP_PESSAGE_X_L
    BOTTOM_PESSAGE_X_C = TOP_PESSAGE_X_C
    BOTTOM_PESSAGE_X_R = TOP_PESSAGE_X_R        
    BOTTOM_PESSAGE_Y = -40


    LEFT_PESSAGE_X = -35
    LEFT_PESSAGE_Y_T = 810
    LEFT_PESSAGE_Y_B = 210
    LEFT_PESSAGE_Y_C = (LEFT_PESSAGE_Y_T + LEFT_PESSAGE_Y_B)/2

    RIGHT_PESSAGE_X = 1055
    RIGHT_PESSAGE_Y_T = LEFT_PESSAGE_Y_T
    RIGHT_PESSAGE_Y_C = LEFT_PESSAGE_Y_C
    RIGHT_PESSAGE_Y_B = LEFT_PESSAGE_Y_B

    position = {
        Section.TOP:{
            XPartition.LEFT:TOP_X_L +10,
            XPartition.MIDDLE:TOP_X_C ,
            XPartition.RIGHT:TOP_X_R-10,
            YPartition.TOP:TOP_Y_T -10,
            YPartition.MIDDLE:TOP_Y_C,
            YPartition.BOTTOM:TOP_Y_B +10,},

        Section.BOTTOM:{
            XPartition.LEFT:BOTTOM_X_L +10,
            XPartition.MIDDLE:BOTTOM_X_C,
            XPartition.RIGHT:BOTTOM_X_R-10,
            YPartition.TOP:BOTTOM_Y_T-10,
            YPartition.MIDDLE:BOTTOM_Y_C,
            YPartition.BOTTOM:BOTTOM_Y_B +10,},

        Section.LEFT:{
            XPartition.LEFT:LEFT_X_L +10,
            XPartition.MIDDLE:LEFT_X_C,
            XPartition.RIGHT:LEFT_X_R-10,
            YPartition.TOP:LEFT_Y_T-10,
            YPartition.MIDDLE:LEFT_Y_C,
            YPartition.BOTTOM:LEFT_Y_B +10,},

        Section.RIGHT:{
            XPartition.LEFT:RIGHT_X_L +10,
            XPartition.MIDDLE:RIGHT_X_C,
            XPartition.RIGHT:RIGHT_X_R-10,
            YPartition.TOP:RIGHT_Y_T-10,
            YPartition.MIDDLE:RIGHT_Y_C,
            YPartition.BOTTOM:RIGHT_Y_B +10,},

        Section.CENTER1:{
            XPartition.LEFT:CENTER_X_L +10,
            XPartition.MIDDLE:CENTER_X_C,
            XPartition.RIGHT:CENTER_X_R-10,
            YPartition.TOP:CENTER_Y_T-10,
            YPartition.MIDDLE:CENTER_Y_C,
            YPartition.BOTTOM:CENTER_Y_B +10,},

        Section.CENTER2:{
            XPartition.LEFT:TOP_PESSAGE_X_L +10,
            XPartition.MIDDLE:TOP_PESSAGE_X_C,
            XPartition.RIGHT:TOP_PESSAGE_X_R-10,
            YPartition.TOP:LEFT_PESSAGE_Y_T-10,
            YPartition.MIDDLE:LEFT_PESSAGE_Y_C,
            YPartition.BOTTOM:LEFT_PESSAGE_Y_B +10,},

        Section.TOP_PESSAGE:{
            XPartition.LEFT:TOP_PESSAGE_X_L,
            XPartition.MIDDLE:TOP_PESSAGE_X_C,
            XPartition.RIGHT:TOP_PESSAGE_X_R,
            YPartition.TOP:TOP_PESSAGE_Y,
            YPartition.MIDDLE:TOP_PESSAGE_Y,
            YPartition.BOTTOM:TOP_PESSAGE_Y,},


        Section.BOTTOM_PESSAGE:{
            XPartition.LEFT:BOTTOM_PESSAGE_X_L,
            XPartition.MIDDLE:BOTTOM_PESSAGE_X_C,
            XPartition.RIGHT:BOTTOM_PESSAGE_X_R,
            YPartition.TOP:BOTTOM_PESSAGE_Y,
            YPartition.MIDDLE:BOTTOM_PESSAGE_Y,
            YPartition.BOTTOM:BOTTOM_PESSAGE_Y,},

        Section.LEFT_PASSAGE:{
            XPartition.LEFT:LEFT_PESSAGE_X,
            XPartition.MIDDLE:LEFT_PESSAGE_X,
            XPartition.RIGHT:LEFT_PESSAGE_X,
            YPartition.TOP:LEFT_PESSAGE_Y_T,
            YPartition.MIDDLE:LEFT_PESSAGE_Y_C,
            YPartition.BOTTOM:LEFT_PESSAGE_Y_B,},


        Section.RIGHT_PASSAGE:{
            XPartition.LEFT:RIGHT_PESSAGE_X,
            XPartition.MIDDLE:RIGHT_PESSAGE_X,
            XPartition.RIGHT:RIGHT_PESSAGE_X,
            YPartition.TOP:RIGHT_PESSAGE_Y_T,
            YPartition.MIDDLE:RIGHT_PESSAGE_Y_C,
            YPartition.BOTTOM:RIGHT_PESSAGE_Y_B,},
    }

    @staticmethod
    def get_pos(section:Section, x_part:XPartition, y_part:YPartition): # (x, y)
        x = MapPos.position[section][x_part]
        y = MapPos.position[section][y_part]
        return (int(x), int(y)) 