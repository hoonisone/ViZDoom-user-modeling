from pickletools import float8
from tkinter.messagebox import NO
from turtle import st
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
        self.name = ObjectName(ObjectName.ToEnum(object.name))
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


        self.player = self.get_object_date_list(name = ObjectName.DoomPlayer)[0]
        
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
            if object.name == ObjectName.DoomPlayer:
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
    

