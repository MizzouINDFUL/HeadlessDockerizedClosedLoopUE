import rospy
from sensor_msgs.msg import Image, CameraInfo
from geometry_msgs.msg import PoseStamped
from cv_bridge import CvBridge
import os
import cv2
import json
import time
import yaml

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

        if json_name != "":
            #replace .json with .txt
            json_name = json_name.replace(".json", ".txt")
            #create a text file for the json data
            self.jsonRef = open("/root/shared/src/"+json_name, "w")
        
    def subscribe(self):
        if self.topicType == "Image":
            rospy.Subscriber(self.topicName, Image, self.image_callback)
        elif self.topicType == "PoseStamped":
            rospy.Subscriber(self.topicName, PoseStamped, self.json_callback)
        elif self.topicType == "CameraInfo":
            rospy.Subscriber(self.topicName, CameraInfo, self.json_callback)
        else:
            print("Topic type "+self.topicType+" not supported")
            return
    
    def get_folder_count(self):
        return len(os.listdir("/root/shared/src/"+self.topicFolder))
    
    def image_callback(self, msg):
        print("Received an image!")
        # Convert the ROS message to an OpenCV image
        cv_image = bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')
        curr_count = self.get_folder_count()
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

