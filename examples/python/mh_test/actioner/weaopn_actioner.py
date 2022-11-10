import vizdoom as vzd
from actioner.actioner import *
from deathmatch import *
from draw_map import *

class WeaponChangeActioner(AbstractActioner):
    def __init__(self, game:vzd.DoomGame):
        super().__init__(game)

    def add_action(self, stateData: StateData2, action_order_sheet: PlayerAction):
        # return super().add_action(stateData, action_order_sheet)
        # print(stateData.state.game_variables[4])
        # p = random.random()
        
        if int(time()) % 5 == 0:

            weapon = [
                PlayerAction.weapone1,
                PlayerAction.weapone1,
                PlayerAction.weapone2,
                PlayerAction.weapone3,
                PlayerAction.weapone4,
                PlayerAction.weapone5,
                PlayerAction.weapone6,
            ]
            possess = stateData.get_weapon_possess()
            ammo = stateData.get_weapon_ammo()
            for i in [6, 4, 2, 3, 5, 1]:
                if 0 < possess[i] and 0 < ammo[i]:
                    empty = AbstractActioner.make_empty_action_order_sheet()
                    empty[PlayerAction.weapone6] = 1
                    empty = AbstractActioner.make_into_doom_action(empty)
                    self.game.make_action(empty)
                    action_order_sheet[weapon[i]] = 1
                    return

            action_order_sheet[PlayerAction.weapone1] = 1
        

        # if p < 0.5:

        # if random.
        # if random.random() < 0.01:
        #     action_order_sheet[PlayerAction.SELECT_NEXT_WEAPON] = 1