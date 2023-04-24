from std_msgs.msg import *
import json
class GroundTruth(std_msgs.msg.Empty):
    def __init__(self):
        self.data = {}

        self.data["collection"] = "MyCollection"
        self.data["fileUID"] = "example"
        self.data["startTime"] = "2022-1-5T13:21:05.431000"
        self.data["stopTime"] = "2022-1-5T13:22:18.725000"
        self.data["nFrames"] = 2
        self.data["frameAnnotations"] = {}
    
    def add_frame_annotation(self, frame_annotation: dict):
        #add to the frameAnnotations dictionary
        self.data["frameAnnotations"].update(frame_annotation)