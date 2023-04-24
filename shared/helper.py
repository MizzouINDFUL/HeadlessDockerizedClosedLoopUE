import json
import time

def write_into_json(in_file: str, tag, value):
    #modifies the value of a tag in the json file
    with open(in_file, 'r') as file:
        try:
            data = json.load(file)
            data[tag] = value
            with open(in_file, 'w') as outfile:
                json.dump(data, outfile)
        except json.JSONDecodeError as exc:
            print(exc)

def read_json(in_file: str):
    out = {}
    with open(in_file, 'r') as file:
        try:
            out = json.load(file)
            return out
        except json.JSONDecodeError as exc:
            print(exc)

def get_current_time(brackets = False):
    if brackets:
        return "[" + time.strftime("%Y-%m-%d_%H-%M-%S", 
                             time.localtime()) + "]"
    else:
        return time.strftime("%Y-%m-%d_%H-%M-%S", 
                             time.localtime())
    
def get_ue_condition_tags(path: str = "./unreal.json"):
    return read_json(path)

class UnrealBridge():
    def __init__(self, status_file_path = "./unreal.json") -> None:
        self.ue_state = {}
        self.status_file_path = status_file_path
        # self.reset_ue_tags()
    
    def update_ue_state(self):
        self.ue_state = get_ue_condition_tags(self.status_file_path)
    
    def set_ue_condition_tag(self, tag: str, value: any):
        write_into_json(self.status_file_path, tag, value)
        self.update_ue_state()

    def reset_ue_tags(self):
        #open ./shared/unreal.json
        #set all states to 0
        with open(self.status_file_path, 'r') as file:
            try:
                data = json.load(file)
                data['play'] = 0
                data['stop'] = 0
                data['ready'] = 0
                data['playing'] = 0
                data['begin_play'] = 0
                data['end_play'] = 0
                self.ue_state = data

                with open(self.status_file_path, 'w') as outfile:
                    json.dump(data, outfile)
            except json.JSONDecodeError as exc:
                print(exc)
    
    '''
    different states in which Unreal can be 
    this helps us understand which operations to perform next
    '''
    def is_engine_ready(self):
        if self.ue_state is None:
            return False
        return self.ue_state["ready"] == 1
    
    def is_requesting_play(self):
        if self.ue_state is None:
            return False
        return self.ue_state["play"] == 1

    def is_requesting_stop(self):
        if self.ue_state is None:
            return False
        return self.ue_state["stop"] == 1
    
    def is_engine_playing(self):
        if self.ue_state is None:
            return False
        return self.ue_state["playing"] == 1
    
    def is_in_begin_play(self):
        if self.ue_state is None:
            return False
        return self.ue_state["begin_play"] == 1
    
    def is_in_end_play(self):
        if self.ue_state is None:
            print(get_current_time(True) + "ue_state is None")
            return False
        return self.ue_state["end_play"] == 1
    
    ''''''
