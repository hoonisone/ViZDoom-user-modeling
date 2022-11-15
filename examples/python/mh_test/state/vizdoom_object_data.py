from pickletools import float8
from time import get_clock_info
from tkinter.messagebox import NO
from turtle import st
from winsound import PlaySound
import numpy as np
from vizdoom_enum.vizdoom_object_name import *
import math
from vizdoom_enum.vizdoom_game_variable import *

def dist(p1, p2):
    p1 = np.array(p1)
    p2 = np.array(p2)
    return np.sqrt(np.sum(np.square(p1-p2)))

class StateData2:

    def __init__(self, game):
        self.game = game
        self.state = self.game.get_state()
        self.palyer_pos = None
        self.player_id = None
        self.enemy_id_list = None
        self.closest_enemy_id = None
        self.closest_enomy_object_id = None
        self.id_object_dict = None # id 와 object 쌍 저장
        self.id_label_dict = None # id 와 label 쌍 저장
        self.enemy_label_id_list = None
        self.closest_enemy_label_id = None
        self.weapon_ammo = None
        self.weapon_possess = None

    def get_weapon_possess(self):
        if self.weapon_possess == None:
            self.weapon_possess = [
                self.state.game_variables[GameVariable.WEAPON0],
                self.state.game_variables[GameVariable.WEAPON1],
                self.state.game_variables[GameVariable.WEAPON2],
                self.state.game_variables[GameVariable.WEAPON3],
                self.state.game_variables[GameVariable.WEAPON4],
                self.state.game_variables[GameVariable.WEAPON5],
                self.state.game_variables[GameVariable.WEAPON6],
            ]
        return self.weapon_possess

    def get_weapon_ammo(self):
        if self.weapon_ammo == None:
            v = self.state.game_variables
            self.weapon_ammo = [
                v[GameVariable.AMMO0],
                v[GameVariable.AMMO1],
                v[GameVariable.AMMO2],
                v[GameVariable.AMMO3],
                v[GameVariable.AMMO4],
                v[GameVariable.AMMO5],
                v[GameVariable.AMMO6]]
        return self.weapon_ammo

    def get_player_id(self):
        if self.player_id == None:
            for object in self.state.objects:
                player_pos = self.get_player_pos()
                object_pos = (object.position_x, object.position_y)
                
                if object.name == "DoomPlayer" and dist(player_pos, object_pos) < 5:
                    self.player_id = object.id
                    break
        return self.player_id
    
    def is_enemy(self, id): # object가 적인지 판단.
        if self.get_object(id).name in enemy_name_list:
            return True
        if (self.get_object(id).name == "DoomPlayer") and (id != self.get_player_id()): # 적 플레이어
            return True
        return False

    def get_enemy_id_list(self): # 존재하는 모든 적 object의 id 리스트 반환
        if self.enemy_id_list == None:
            enemy_id_list= []
            for object in self.state.objects:
                if self.is_enemy(object.id):
                    enemy_id_list.append(object.id)

            self.enemy_id_list = enemy_id_list

        return self.enemy_id_list

    def get_closest_enemy_object_id(self):
        if self.closest_enomy_object_id == None:
            min_dist = 10000000
            min_enemy_id = None
            for id in self.get_enemy_id_list():
                dist = self.get_dist_from_player(id)
                if dist < min_dist:
                    min_enemy_id = id
                    min_dist = dist
            self.closest_enomy_object_id = min_enemy_id
        
        return self.closest_enomy_object_id
                
    def get_dist_from_player(self, id):
        player = self.get_object(self.get_player_id())
        object = self.get_object(id)
        player_pos = (player.position_x, player.position_y)
        object_pos = (object.position_x, object.position_y)
        return dist(player_pos, object_pos)

    def dist(p1, p2):
        p1 = np.array(p1)
        p2 = np.array(p2)
        return np.sqrt(np.sum(np.square(p1-p2)))

    def get_id_object_dict(self):
        if self.id_object_dict == None:
            id_object_dict = {}
            for object in self.state.objects:
                id_object_dict[object.id] = object
            self.id_object_dict = id_object_dict

        return self.id_object_dict

    def get_id_label_dict(self):
        if self.id_label_dict == None:
            id_label_dict = {}
            for object in self.state.labels:
                id_label_dict[object.object_id] = object
            self.id_label_dict = id_label_dict

        return self.id_label_dict

    def get_object(self, id):
        id_object_dict = self.get_id_object_dict()
        return id_object_dict[id] if id in id_object_dict else None

    def get_label(self, id):
        id_label_dict = self.get_id_label_dict()
        return id_label_dict[id] if id in id_label_dict else None

    def get_enemy_label_id_list(self):
        if self.enemy_label_id_list == None:
            enemy_label_id_list = []
            for label in self.state.labels:
                if self.is_enemy(label.object_id):
                    enemy_label_id_list.append(label.object_id)
            self.enemy_label_id_list = enemy_label_id_list

        return self.enemy_label_id_list

    def get_closest_enemy_label_id(self):
        if self.closest_enemy_id is None:
            min_dist = 1000000000
            min_enemy_label_id = None
            for enemy_label_id in self.get_enemy_id_list():
                dist = self.get_dist_from_player(enemy_label_id)
                if dist < min_dist:
                    min_dist = dist
                    min_enemy_label_id = enemy_label_id
            self.closest_enemy__id = min_enemy_label_id
        return self.closest_enemy_id

    def get_visible_closest_enemy_label_id(self):
        if self.closest_enemy_label_id is None:
            min_dist = 1000000000
            min_enemy_label_id = None
            for enemy_label_id in self.get_enemy_label_id_list():
                dist = self.get_dist_from_player(enemy_label_id)
                if dist < min_dist:
                    min_dist = dist
                    min_enemy_label_id = enemy_label_id
            self.closest_enemy_label_id = min_enemy_label_id
        return self.closest_enemy_label_id
     

    def get_x_pixel_dist(self, id): # 화면 상에서 object와 플레이어의 중심좌표 간의 거리
        object_label = self.get_label(id)
        player_label = self.get_label(self.get_player_id())
        if object_label is None:
            return None

        if player_label is None:
            return None

        # print("player_id: %s, player: %s, target: %s"%(str(self.get_player_id()), str(player_label), str(object_label)))
        return (object_label.x + object_label.width/2) - self.game.get_screen_width()/2
        # return (object_label.x + object_label.width/2) - (player_label.x+player_label.width/2)

    def is_in_shotting_effective_zone(self, id):

        x_pixel_dist = self.get_x_pixel_dist(id)
        if x_pixel_dist is None:
            return False
        # print(math.fabs(x_pixel_dist))
        # print(math.fabs(x_pixel_dist), max(50, self.get_label(id).width))
        return math.fabs(x_pixel_dist) <= max(self.game.get_screen_width()/50, self.get_label(id).width) # 플레이어와 표적의 중심 좌표가 표적의 withd 보다 짧은가

    def get_player_pos(self):
        if self.palyer_pos == None:
            x = self.get_game_variagle(GameVariable.POSITION_X)
            y = self.get_game_variagle(GameVariable.POSITION_Y)
            self.palyer_pos = (x, y)
        return self.palyer_pos

    def get_player(self):
        return self.get_object(self.get_player_id())

    def get_game_variagle(self, variable:GameVariable):
        return self.state.game_variables[variable]

def get_angle_from_player_to_direction(px, py, dx, dy): # player를 기준으로 (x, y)의 방향을 angle(0~359)로 반환

    # 상대 거리 좌표
    x_dist = dx - px
    y_dist = dy - py

    d = dist((dx, dy), (px, py))

    if x_dist == 0:
        if y_dist > 0:
            return 90
        else:
            return 270

    a = math.acos(x_dist/d)/math.pi*180
    if y_dist < 0:
        a =  360-a # x 축 대칭

    return a
    

