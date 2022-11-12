from vizdoom_object_data import *
from actioner.moving_actioner import *
from actioner.aim_actioner import *
from actioner.weaopn_actioner import * 

class AbstractAgent:
    def __init__(self, game):
        self.game = game
    
    @ abstractmethod
    def do_action(self):
        pass



