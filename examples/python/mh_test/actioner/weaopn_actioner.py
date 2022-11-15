import vizdoom as vzd
from actioner.actioner import *
from actioner.deathmatch_pos import *
from actioner.draw_map import *

class WeaponChangeActioner(AbstractActioner):
    def __init__(self, game:vzd.DoomGame):
        super().__init__(game)
        self.next_change_time = time() + random.randrange(3, 10)

    def add_action(self, stateData: StateAnalyzer, action_order_sheet: PlayerAction):
        # return super().add_action(stateData, action_order_sheet)
        # print(stateData.state.game_variables[4])
        # p = random.random()
        
        if self.next_change_time < time():
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
            for i in [6, 4, 3, 5, 2, 3, 1]:
                if 0 < possess[i] and 0 < ammo[i]:
                    empty = AbstractActioner.make_empty_action_order_sheet()
                    empty[weapon[i]] = 1
                    empty = AbstractActioner.make_into_doom_action(empty)
                    self.game.make_action(empty)
                    # action_order_sheet[weapon[i]] = 1
                    return

            # action_order_sheet[PlayerAction.weapone1] = 1
        

        # if p < 0.5:

        # if random.
        # if random.random() < 0.01:
        #     action_order_sheet[PlayerAction.SELECT_NEXT_WEAPON] = 1