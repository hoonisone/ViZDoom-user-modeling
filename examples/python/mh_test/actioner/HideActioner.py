import vizdoom as vzd
from actioner.actioner import *
from actioner.deathmatch_pos import *
from actioner.draw_map import *
import random
from actioner.moving_actioner import *


class HideTopSector(SequentialActioner):
    path_list = [
        [
            lambda game : VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.RIGHT, YPartition.TOP)),
            lambda game : VisitActioner(game, MapPos.get_pos(Section.TOP_PESSAGE, XPartition.RIGHT , YPartition.MIDDLE)),
            lambda game : VisitActioner(game, MapPos.get_pos(Section.TOP, XPartition.RIGHT, YPartition.MIDDLE)),
            lambda game : VisitActioner(game, MapPos.get_pos(Section.TOP, XPartition.LEFT, YPartition.BOTTOM)),
        ],
        [
            lambda game : VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.RIGHT, YPartition.TOP)),
            lambda game : VisitActioner(game, MapPos.get_pos(Section.TOP_PESSAGE, XPartition.RIGHT , YPartition.MIDDLE)),
            lambda game : VisitActioner(game, MapPos.get_pos(Section.TOP, XPartition.RIGHT, YPartition.MIDDLE)),
            lambda game : VisitActioner(game, MapPos.get_pos(Section.TOP, XPartition.RIGHT, YPartition.BOTTOM)),
        ],
        [
            lambda game : VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.MIDDLE, YPartition.TOP)),
            lambda game : VisitActioner(game, MapPos.get_pos(Section.TOP_PESSAGE, XPartition.MIDDLE , YPartition.MIDDLE)),
            lambda game : VisitActioner(game, MapPos.get_pos(Section.TOP, XPartition.MIDDLE, YPartition.MIDDLE)),
            lambda game : VisitActioner(game, MapPos.get_pos(Section.TOP, XPartition.LEFT, YPartition.BOTTOM)),
        ],
        [
            lambda game : VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.MIDDLE, YPartition.TOP)),
            lambda game : VisitActioner(game, MapPos.get_pos(Section.TOP_PESSAGE, XPartition.MIDDLE , YPartition.MIDDLE)),
            lambda game : VisitActioner(game, MapPos.get_pos(Section.TOP, XPartition.MIDDLE, YPartition.MIDDLE)),
            lambda game : VisitActioner(game, MapPos.get_pos(Section.TOP, XPartition.RIGHT, YPartition.BOTTOM)),
        ],
        [
            lambda game : VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.LEFT, YPartition.TOP)),
            lambda game : VisitActioner(game, MapPos.get_pos(Section.TOP_PESSAGE, XPartition.LEFT , YPartition.MIDDLE)),
            lambda game : VisitActioner(game, MapPos.get_pos(Section.TOP_PESSAGE, XPartition.LEFT , YPartition.MIDDLE)),
            lambda game : VisitActioner(game, MapPos.get_pos(Section.TOP, XPartition.LEFT, YPartition.BOTTOM)),
        ],
        [
            lambda game : VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.LEFT, YPartition.TOP)),
            lambda game : VisitActioner(game, MapPos.get_pos(Section.TOP_PESSAGE, XPartition.LEFT , YPartition.MIDDLE)),
            lambda game : VisitActioner(game, MapPos.get_pos(Section.TOP_PESSAGE, XPartition.LEFT , YPartition.MIDDLE)),

            lambda game : VisitActioner(game, MapPos.get_pos(Section.TOP, XPartition.RIGHT, YPartition.BOTTOM)),
        ],        
    ]

    def __init__(self, game):
        path = HideTopSector.path_list[random.randrange(len(HideTopSector.path_list))]
        super().__init__(game, path)

class HideBottomSector(SequentialActioner):
    path_list = [
        [
            lambda game : VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.RIGHT, YPartition.BOTTOM)),
            lambda game : VisitActioner(game, MapPos.get_pos(Section.BOTTOM_PESSAGE, XPartition.RIGHT , YPartition.MIDDLE)),
            lambda game : VisitActioner(game, MapPos.get_pos(Section.BOTTOM, XPartition.RIGHT, YPartition.MIDDLE)),
            lambda game : VisitActioner(game, MapPos.get_pos(Section.BOTTOM, XPartition.LEFT, YPartition.TOP)),
        ],
        [
            lambda game : VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.RIGHT, YPartition.BOTTOM)),
            lambda game : VisitActioner(game, MapPos.get_pos(Section.BOTTOM_PESSAGE, XPartition.RIGHT , YPartition.MIDDLE)),
            lambda game : VisitActioner(game, MapPos.get_pos(Section.BOTTOM, XPartition.RIGHT, YPartition.MIDDLE)),
            lambda game : VisitActioner(game, MapPos.get_pos(Section.BOTTOM, XPartition.RIGHT, YPartition.TOP)),
        ],
        [
            lambda game : VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.MIDDLE, YPartition.BOTTOM)),
            lambda game : VisitActioner(game, MapPos.get_pos(Section.BOTTOM_PESSAGE, XPartition.MIDDLE , YPartition.MIDDLE)),
            lambda game : VisitActioner(game, MapPos.get_pos(Section.BOTTOM, XPartition.RIGHT, YPartition.MIDDLE)),
            lambda game : VisitActioner(game, MapPos.get_pos(Section.BOTTOM, XPartition.LEFT, YPartition.TOP)),
        ],
        [
            lambda game : VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.MIDDLE, YPartition.BOTTOM)),
            lambda game : VisitActioner(game, MapPos.get_pos(Section.BOTTOM_PESSAGE, XPartition.MIDDLE , YPartition.MIDDLE)),
            lambda game : VisitActioner(game, MapPos.get_pos(Section.BOTTOM, XPartition.RIGHT, YPartition.MIDDLE)),
            lambda game : VisitActioner(game, MapPos.get_pos(Section.BOTTOM, XPartition.RIGHT, YPartition.TOP)),
        ],
        [
            lambda game : VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.LEFT, YPartition.BOTTOM)),
            lambda game : VisitActioner(game, MapPos.get_pos(Section.BOTTOM_PESSAGE, XPartition.LEFT , YPartition.MIDDLE)),
            lambda game : VisitActioner(game, MapPos.get_pos(Section.BOTTOM, XPartition.RIGHT, YPartition.MIDDLE)),
            lambda game : VisitActioner(game, MapPos.get_pos(Section.BOTTOM, XPartition.LEFT, YPartition.TOP)),
        ],
        [
            lambda game : VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.MIDDLE, YPartition.BOTTOM)),
            lambda game : VisitActioner(game, MapPos.get_pos(Section.BOTTOM_PESSAGE, XPartition.MIDDLE , YPartition.MIDDLE)),
            lambda game : VisitActioner(game, MapPos.get_pos(Section.BOTTOM, XPartition.RIGHT, YPartition.MIDDLE)),
            lambda game : VisitActioner(game, MapPos.get_pos(Section.BOTTOM, XPartition.RIGHT, YPartition.TOP)),
        ],        
    ]
    def __init__(self, game):
        path = HideBottomSector.path_list[random.randrange(len(HideBottomSector.path_list))]
        super().__init__(game, path)

class HideLeftSector(SequentialActioner):
    path_list = [
        [
            lambda game : VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.LEFT, YPartition.TOP)),
            lambda game : VisitActioner(game, MapPos.get_pos(Section.LEFT_PESSAGE, XPartition.MIDDLE , YPartition.TOP)),
            lambda game : VisitActioner(game, MapPos.get_pos(Section.LEFT, XPartition.MIDDLE, YPartition.TOP)),
            lambda game : VisitActioner(game, MapPos.get_pos(Section.LEFT, XPartition.RIGHT, YPartition.TOP)),
        ],
        [
            lambda game : VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.LEFT, YPartition.TOP)),
            lambda game : VisitActioner(game, MapPos.get_pos(Section.LEFT_PESSAGE, XPartition.MIDDLE , YPartition.TOP)),
            lambda game : VisitActioner(game, MapPos.get_pos(Section.LEFT, XPartition.MIDDLE, YPartition.TOP)),
            lambda game : VisitActioner(game, MapPos.get_pos(Section.LEFT, XPartition.RIGHT, YPartition.BOTTOM)),
        ],
        [
            lambda game : VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.LEFT, YPartition.MIDDLE)),
            lambda game : VisitActioner(game, MapPos.get_pos(Section.LEFT_PESSAGE, XPartition.MIDDLE , YPartition.MIDDLE)),
            lambda game : VisitActioner(game, MapPos.get_pos(Section.LEFT, XPartition.MIDDLE, YPartition.MIDDLE)),
            lambda game : VisitActioner(game, MapPos.get_pos(Section.LEFT, XPartition.RIGHT, YPartition.TOP)),
        ],
        [
            lambda game : VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.LEFT, YPartition.MIDDLE)),
            lambda game : VisitActioner(game, MapPos.get_pos(Section.LEFT_PESSAGE, XPartition.MIDDLE , YPartition.MIDDLE)),
            lambda game : VisitActioner(game, MapPos.get_pos(Section.LEFT, XPartition.MIDDLE, YPartition.MIDDLE)),
            lambda game : VisitActioner(game, MapPos.get_pos(Section.LEFT, XPartition.RIGHT, YPartition.BOTTOM)),
        ],
        [
            lambda game : VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.LEFT, YPartition.MIDDLE)),
            lambda game : VisitActioner(game, MapPos.get_pos(Section.LEFT_PESSAGE, XPartition.MIDDLE , YPartition.MIDDLE)),
            lambda game : VisitActioner(game, MapPos.get_pos(Section.LEFT, XPartition.MIDDLE, YPartition.MIDDLE)),
            lambda game : VisitActioner(game, MapPos.get_pos(Section.LEFT, XPartition.RIGHT, YPartition.TOP)),
        ],
        [
            lambda game : VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.LEFT, YPartition.MIDDLE)),
            lambda game : VisitActioner(game, MapPos.get_pos(Section.LEFT_PESSAGE, XPartition.MIDDLE , YPartition.MIDDLE)),
            lambda game : VisitActioner(game, MapPos.get_pos(Section.LEFT, XPartition.MIDDLE, YPartition.MIDDLE)),
            lambda game : VisitActioner(game, MapPos.get_pos(Section.LEFT, XPartition.RIGHT, YPartition.BOTTOM)),
        ],    
    ]
    def __init__(self, game):
        path = HideLeftSector.path_list[random.randrange(len(HideLeftSector.path_list))]
        super().__init__(game, path)

class HideRightSector(SequentialActioner):
    path_list = [
        [
            lambda game : VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.RIGHT, YPartition.TOP)),
            lambda game : VisitActioner(game, MapPos.get_pos(Section.RIGHT_PESSAGE, XPartition.MIDDLE , YPartition.TOP)),
            lambda game : VisitActioner(game, MapPos.get_pos(Section.RIGHT, XPartition.MIDDLE, YPartition.TOP)),
            lambda game : VisitActioner(game, MapPos.get_pos(Section.RIGHT, XPartition.LEFT, YPartition.TOP)),
        ],
        [
            lambda game : VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.RIGHT, YPartition.TOP)),
            lambda game : VisitActioner(game, MapPos.get_pos(Section.RIGHT_PESSAGE, XPartition.MIDDLE , YPartition.TOP)),
            lambda game : VisitActioner(game, MapPos.get_pos(Section.RIGHT, XPartition.MIDDLE, YPartition.TOP)),
            lambda game : VisitActioner(game, MapPos.get_pos(Section.RIGHT, XPartition.LEFT, YPartition.BOTTOM)),
        ],
        [
            lambda game : VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.RIGHT, YPartition.MIDDLE)),
            lambda game : VisitActioner(game, MapPos.get_pos(Section.RIGHT_PESSAGE, XPartition.MIDDLE , YPartition.MIDDLE)),
            lambda game : VisitActioner(game, MapPos.get_pos(Section.RIGHT, XPartition.MIDDLE, YPartition.MIDDLE)),
            lambda game : VisitActioner(game, MapPos.get_pos(Section.RIGHT, XPartition.LEFT, YPartition.TOP)),
        ],
        [
            lambda game : VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.RIGHT, YPartition.MIDDLE)),
            lambda game : VisitActioner(game, MapPos.get_pos(Section.RIGHT_PESSAGE, XPartition.MIDDLE , YPartition.MIDDLE)),
            lambda game : VisitActioner(game, MapPos.get_pos(Section.RIGHT, XPartition.MIDDLE, YPartition.MIDDLE)),
            lambda game : VisitActioner(game, MapPos.get_pos(Section.RIGHT, XPartition.LEFT, YPartition.BOTTOM)),
        ],
        [
            lambda game : VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.RIGHT, YPartition.MIDDLE)),
            lambda game : VisitActioner(game, MapPos.get_pos(Section.RIGHT_PESSAGE, XPartition.MIDDLE , YPartition.MIDDLE)),
            lambda game : VisitActioner(game, MapPos.get_pos(Section.RIGHT, XPartition.RIGHT, YPartition.MIDDLE)),
            lambda game : VisitActioner(game, MapPos.get_pos(Section.RIGHT, XPartition.LEFT, YPartition.TOP)),
        ],
        [
            lambda game : VisitActioner(game, MapPos.get_pos(Section.CENTER1, XPartition.RIGHT, YPartition.MIDDLE)),
            lambda game : VisitActioner(game, MapPos.get_pos(Section.RIGHT_PESSAGE, XPartition.MIDDLE , YPartition.MIDDLE)),
            lambda game : VisitActioner(game, MapPos.get_pos(Section.RIGHT, XPartition.MIDDLE, YPartition.MIDDLE)),
            lambda game : VisitActioner(game, MapPos.get_pos(Section.RIGHT, XPartition.LEFT, YPartition.BOTTOM)),
        ],    
    ]
    def __init__(self, game):
        path = HideRightSector.path_list[random.randrange(len(HideRightSector.path_list))]
        super().__init__(game, path)