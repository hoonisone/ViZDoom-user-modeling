from pickletools import float8
from time import get_clock_info
from tkinter.messagebox import NO
from turtle import st
from winsound import PlaySound
import numpy as np
from vizdoom_object_name import *
import math

def dist(p1, p2):
    p1 = np.array(p1)
    p2 = np.array(p2)
    return np.sqrt(np.sum(np.square(p1-p2)))




class ObjectData:
    def __init__(self, object):
        self.id = object.id
        self.object = object
        self.name = DoomObject(DoomObject.ToEnum(object.name))
        self.pos = (object.position_x, object.position_y)
        self.visible = False

class StateData:
    # Dict<ObjectName, List<object>>
    type_objects_dict = {}
    def __init__(self, state):
        self.id_object_dict = self.make_id_object_dict(state) # id-object 쌍 생성
        self.type_objects_dict = self.make_type_objects_dict(self.id_object_dict.values()) # type-object 쌍 생성
        
        self.set_visible_value(state) # 모든 객체에 visible 값 세팅
        self.set_dist_to_player() # 모든 객체에 player와의 거리 계산
        self.set_label_infor(state)


        self.player = self.get_object_date_list(name = DoomObject.DoomPlayer)[0]
        
    def set_label_infor(self, state): # visible의 경우 label 정보를 세팅해줌
        for label in state.labels:
            object = self.id_object_dict[label.object_id]
            object.x = label.x
            object.y = label.y
            object.w = label.width
            object.h = label.height

    def set_visible_value(self, state): # visible 변수 세팅
        for label in state.labels:
            self.id_object_dict[label.object_id].visible = True
    

    def set_dist_to_player(self): # state에 모든 object에 대해 player와의 거리를 구하고 세팅해준다.
        # Player 찾기
        player = None
        for object in self.id_object_dict.values():
            if object.name == DoomObject.DoomPlayer:
                player = object
                break
        
        for object in self.id_object_dict.values(): 
            object.dist_to_player = dist(object.pos, player.pos)

    def get_object_date_list(self, name = None, visible=None):
        objects = self.id_object_dict.values()

        # name에 맞는 object만 남기기
        if name is not None:
            target = []
            for o in objects:
                if o.name == name:
                    target.append(o)
            objects = target

        # visible조건에 맞는 object만 남기기
        if visible is not None:
            target = []
            for o in objects:
                if o.visible == visible:
                    target.append(o)
            objects = target
        
        return objects

    @staticmethod
    def make_id_object_dict(state):
        id_object_dict = {}
        for o in state.objects:
            id_object_dict[o.id] = ObjectData(o)
        return id_object_dict

    @staticmethod
    def make_type_objects_dict(objects):
        type_objects_dict = {}
        for object in objects:
            if object.name not in type_objects_dict:
                type_objects_dict[object.name] = []
            type_objects_dict[object.name].append(object)
        return type_objects_dict


class StateData2:

    def __init__(self, state):
        self.state = state
        self.player = None
        self.enemies = None
        self.closest_enomy = None
        self.id_object_dict = None
        self.enemy_labels = None
        self.closest_enemy_label = None

    def get_player(self):
        if self.player == None:
            for object in self.state.objects:
                if object.name == "DoomPlayer":
                    self.player = object
                    break     
        
        return self.player
    
    def is_enemy(self, object): # object가 적인지 판단.
        return object.name in enemy_name_list

    def get_enemies(self): # 존재하는 모든 적 OBJECT를 담은 리스트 반환
        if self.enemies == None:
            enemies= []
            for object in self.state.objects:
                if self.is_enemy(object):
                    enemies.append(object)

            self.enemies = enemies

        return self.enemies


    def get_closest_enomy(self):
        if self.closest_enomy == None:
            min_dist = 10000000
            min_enemy = None
            for object in self.get_enemies():
                dist = self.get_dist_from_player(object)
                if dist < min_dist:
                    min_enemy = object
                    min_dist = dist
            self.closest_enomy = min_enemy
        
        return self.closest_enomy
                
    def get_dist_from_player(self, object):
        player = self.get_player()
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

    def get_enemy_labels(self):
        id_object_dict = self.get_id_object_dict()
        if self.enemy_labels == None:
            enemy_labels = []
            for label in self.state.labels:
                if self.is_enemy(id_object_dict[label.object_id]):
                    enemy_labels.append(label)
            self.enemy_labels = enemy_labels

        return self.enemy_labels

    def get_closest_enemy_label(self):
        if self.closest_enemy_label is None:
            min_dist = 1000000000
            min_enemy_label = None
            for enemy_label in self.get_enemy_labels():
                object = self.get_id_object_dict()[enemy_label.object_id]
                dist = self.get_dist_from_player(object)
                if dist < min_dist:
                    min_dist = dist
                    min_enemy_label = enemy_label
            self.closest_enemy_label = min_enemy_label
        return self.closest_enemy_label



def get_player(game):
    for obj in game.get_state().objects:
        if obj.name == "DoomPlayer":
            return obj

    return None

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
    

