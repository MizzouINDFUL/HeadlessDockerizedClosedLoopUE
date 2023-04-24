import rospy
import numpy as np
from sensor_msgs.msg import Image, CameraInfo
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import String
from ground_truth_msg import *
from cv_bridge import CvBridge
import os
import shutil
import cv2
import json
import time
import yaml

import sys
sys.stdout = open("/root/shared/src/log_extractor.txt", "w")

#evaluate settings.yml file
with open("/root/shared/src/settings.yml", 'r') as stream:
    try:
        settings = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

#get the topic with topic typers dictionary from the command line
topics = settings["topics"]

#get the topic with topic folders dictionary
topicFolders = settings["topic-folder"]

#get the topic with Json file names dictionary
topicJsonFiles = settings["topic-json"]

# And returns the name of the image file with the following foramt: 0000000.png, 0000001.png, etc.
def get_image_name(img_counter):
    asStr: str = str(img_counter)
    result: str = ""
    for i in range(7 - len(asStr)):
        result += "0"
    result += asStr
    result += ".png"
    return result

def get_numpy_name(img_counter):
    asStr: str = str(img_counter)
    result: str = ""
    for i in range(7 - len(asStr)):
        result += "0"
    result += asStr
    result += ".npy"
    return result

def is_valid_new_folder(pathName: str):
    return pathName != "" and pathName != "."

class AirSimExtractor():
    def __init__(self, topicName:str, topicType:str, topicFolder: str, json_name = "") -> None:
        if is_valid_new_folder(topicFolder):
            #create a folder for the topic if ir doesn't exist, don't make it write-protected
            if not os.path.exists('/root/shared/src/'+topicFolder):
                os.system("mkdir -m 777 /root/shared/src/"+topicFolder)
                print("Created folder: "+topicFolder)
            else:
                #delete all files in the folder
                os.system("rm -rf /root/shared/src/"+topicFolder+"/*")
                print("Deleted all files in folder: "+topicFolder)

        self.topicFolder = topicFolder
        self.topicName = topicName
        self.topicType = topicType
        self.jsonRef = None
        self.count = 0

        self.decl = {}
        self.decl["collection"] = "MyCollection"
        self.decl["fileUID"] = "example"
        self.decl["startTime"] = "2022-1-5T13:21:05.431000"
        self.decl["stopTime"] = "2022-1-5T13:22:18.725000"
        self.decl["nFrames"] = 2
        self.decl["frameDeclarations"] = {}

        if json_name != "":
            if json_name.find(".json") != -1:
                pass
                # json_name = json_name.replace(".json", ".txt")
            if json_name.find(".yml") != -1:
                json_name = json_name.replace(".yml", ".txt")
            #create a text file for the json data
            self.jsonRef = open("/root/shared/src/"+json_name, "w")

    def subscribe(self):
        # if topicName contains "depth", then subscribe to the depth topic
        if str(self.topicName).find("depth") != -1:
            rospy.Subscriber(self.topicName, Image, self.depth_callback)
        elif self.topicType == "Image":
            rospy.Subscriber(self.topicName, Image, self.image_callback)
        elif self.topicType == "PoseStamped":
            rospy.Subscriber(self.topicName, PoseStamped, self.json_callback)
        elif self.topicType == "CameraInfo":
            rospy.Subscriber(self.topicName, CameraInfo, self.json_callback)
        elif self.topicType == "String":
            rospy.Subscriber(self.topicName, String, self.gt_callback)
        else:
            print("Topic type "+self.topicType+" not supported")
            return
        
    #runs a yolo model on the image and returns the image with the bounding boxes
    def run_yolo(self, image, img_counter):
        # Load Yolo
        net = cv2.dnn.readNet("/root/darknet/yolov3.weights", "/root/darknet/cfg/yolov3.cfg")
        classes = []
        with open("/root/darknet/data/coco.names", "r") as f:
            classes = [line.strip() for line in f.readlines()]

        print("YOLO classes: ", classes)
        
        layer_names = net.getLayerNames()
        print(len(layer_names))
        output_layers = [layer_names[layer - 1] for layer in net.getUnconnectedOutLayers()]
        colors = np.random.uniform(0, 255, size=(len(classes), 3))

        # Loading image
        img = image
        img = cv2.resize(img, None, fx=0.4, fy=0.4)
        height, width, channels = img.shape

        # Detecting objects
        blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

        net.setInput(blob)
        outs = net.forward(output_layers)

        # Showing informations on the screen
        class_ids = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    # Object detected
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    # Rectangle coordinates
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        font = cv2.FONT_HERSHEY_SIMPLEX
        frame_name = f'f{img_counter}'
        self.decl["frameDeclarations"].update({frame_name: {"declarations": []}})
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                color = colors[i]
                cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
                cv2.putText(img, label, (x, y + 30), font, 1, color, 1)
                self.decl["frameDeclarations"][frame_name]["declarations"].append({"confidence": confidences[i],"class": label, "type": "bbox_xywh", "shape" : {"data": [x, y, w, h]}})
        
        return img
    
    #DEPRECATED
    def __get_folder_count(self):
        return len(os.listdir("/root/shared/src/"+self.topicFolder))
    
    def depth_callback(self, msg):

        curr_count = self.count
        self.count += 1

        print("Received a depth image!")

        # Convert the ROS message to an OpenCV image
        cv_image = bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')
        
        name_og = get_numpy_name(curr_count)
        name = self.topicFolder + name_og

        #convert image to a numpy array and save it to a numpy file
        numpy_array = np.array(cv_image)
        np.save(name, numpy_array)

        if is_valid_new_folder(self.topicFolder):
            os.system("mv /root/shared/src/"+name+" /root/shared/src/"+self.topicFolder+"/")
            print("Moved depth image to folder: "+self.topicFolder)
            print("Renaming the depth image: "+name_og)
            #rename the image from name to name_og
            os.system("mv /root/shared/src/"+self.topicFolder+"/"+name+" /root/shared/src/"+self.topicFolder+"/"+name_og)
    
    def image_callback(self, msg):

        curr_count = self.count
        self.count += 1

        print("Received an image!")
        # Convert the ROS message to an OpenCV image
        cv_image = bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')

        cv_image = self.run_yolo(cv_image, curr_count)

        with open("decl.json", 'w') as f:
            json.dump(self.decl, f)

        name_og = get_image_name(curr_count)
        name = self.topicFolder + name_og

        print("Saving the image #"+str(curr_count)+" to disk...")
        print("Image name: "+name)
        # Save the image to disk
        cv2.imwrite(name, cv_image, [int(cv2.IMWRITE_PNG_COMPRESSION), 0])
        #move the rgb image to the topic folder
        if is_valid_new_folder(self.topicFolder):
            os.system("mv /root/shared/src/"+name+" /root/shared/src/"+self.topicFolder+"/")
            print("Moved image to folder: "+self.topicFolder)
            print("Renaming the image: "+name_og)
            #rename the image from name to name_og
            os.system("mv /root/shared/src/"+self.topicFolder+"/"+name+" /root/shared/src/"+self.topicFolder+"/"+name_og)
            

        print("Saved the image #"+str(curr_count)+" to disk!")
    
    def json_callback(self, msg):
        print("Received a json info!")

        #save the message to a text file
        if self.jsonRef != None:
            self.jsonRef.write(str(msg)+"\n")
        
        #add the pose to a json file
        print(msg)
    
    #dumps the recieved ground truth data into a json file
    def gt_callback(self, msg):
        print("Received a ground truth data!")
        print(msg.data)

        string = msg.data

        res = json.loads( string ) 

        #indent the json file
        res = json.dumps(res, indent=4)

        res = json.loads(res)

        #string to json
        with open(self.jsonRef.name, 'w') as f:
            json.dump(res, f)
        

print("Topics: ", topics)

# Initialize the ROS node
rospy.init_node('image_saver')

# Initialize a CvBridge object to convert between ROS messages and OpenCV images
bridge = CvBridge()

os.chdir("/root/shared/src")

for topicName in topics.keys():
    topicType = topics[topicName]
    topicFolder = topicFolders[topicName]
    json_name = ""
    if topicName in topicJsonFiles:
        json_name = topicJsonFiles[topicName]
    extractor = AirSimExtractor(topicName, topicType, topicFolder, json_name)
    extractor.subscribe()

rospy.spin()


