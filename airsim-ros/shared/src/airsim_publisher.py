import rospy
import message_filters
import airsim
import cv2
import os
import shutil
from cv_bridge import CvBridge
from sensor_msgs.msg import Image, CameraInfo
from geometry_msgs.msg import PoseStamped
import json
from std_msgs.msg import String
from ground_truth_msg import *

import tf2_ros

import sys
sys.stdout = open("/root/shared/src/log_publisher.txt", "w")


class AirSimPublisher():

    def __init__(self):

        rospy.init_node('airsim_publisher', anonymous=True)

        self.bridge = CvBridge()

        self.tfBuffer = tf2_ros.Buffer()
        self.tfListener = tf2_ros.TransformListener(self.tfBuffer)
        self.br = tf2_ros.TransformBroadcaster()

        #ground truth
        self.frame_count = 0
        self.gt = GroundTruth()

        queue_size = 1
        topic = 'mindful'

        self.pub_info = rospy.Publisher(f'{topic}_info', CameraInfo, queue_size=queue_size)
        self.pub_pose = rospy.Publisher(f'{topic}_pose', PoseStamped, queue_size=queue_size)
        self.pub_image = rospy.Publisher(f'{topic}_image', Image, queue_size=queue_size)
        self.pub_depth = rospy.Publisher(f'{topic}_depth', Image, queue_size=queue_size)
        self.pub_ground_truth = rospy.Publisher(f'{topic}_ground_truth', String, queue_size=queue_size)

        self.sub_image = message_filters.Subscriber('/airsim_node/drone_1/front/Scene', Image)
        self.sub_depth = message_filters.Subscriber('/airsim_node/drone_1/front/DepthPlanar', Image)
        self.sub_info = message_filters.Subscriber('/airsim_node/drone_1/front/Scene/camera_info', CameraInfo)
        
        self.sub_synced = message_filters.ApproximateTimeSynchronizer([self.sub_image, self.sub_depth, self.sub_info], 1, slop=0.05)
        self.sub_synced.registerCallback(self.callback)

        rospy.spin()

    def callback(self, msg_image:Image, msg_depth:Image, msg_info:CameraInfo):

        timestamp = msg_info.header.stamp

        try:
            tf = self.tfBuffer.lookup_transform('map', 'front_optical', timestamp)
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
            print('exception')
            return
        
        client = airsim.VehicleClient()
        client.confirmConnection()

        client.simPause(True)

        camera_name = "front"
        image_type = airsim.ImageType.Scene

        client.simSetDetectionFilterRadius(camera_name, image_type, 80 * 100000) # in [cm]
        client.simAddDetectionFilterMeshName(camera_name, image_type, "SM*") 
        
        detections = client.simGetDetections(camera_name, image_type)

        #copnvert Image to numpy array
        png = self.bridge.imgmsg_to_cv2(msg_image, "bgr8")

        frame_name = f'f{self.frame_count}'
        # self.gt[frame_name] = {}
        # self.gt[frame_name]["annotations"] = []

        frame = {}

        frame[frame_name] = {}
        frame[frame_name]["annotations"] = []

        # self.gt.data["frameAnnotations"][frame_name] = {}
        self.gt.data["frameAnnotations"].update({frame_name: {"annotations": []}})

        if detections:
            for detection in detections:

                frame[frame_name]["annotations"].append({"class": detection.name,"shape": {"data": [detection.box2D.min.x_val,detection.box2D.min.y_val,detection.box2D.max.x_val - detection.box2D.min.x_val,detection.box2D.max.y_val - detection.box2D.min.y_val],"type": "bbox_xywh"}})

                self.gt.data["frameAnnotations"][frame_name]["annotations"].append({"class": detection.name,"shape": {"data": [detection.box2D.min.x_val,detection.box2D.min.y_val,detection.box2D.max.x_val - detection.box2D.min.x_val,detection.box2D.max.y_val - detection.box2D.min.y_val],"type": "bbox_xywh"}})

                cv2.rectangle(png,(int(detection.box2D.min.x_val),int(detection.box2D.min.y_val)),(int(detection.box2D.max.x_val),int(detection.box2D.max.y_val)),(255,0,0),2)
                cv2.putText(png, detection.name, (int(detection.box2D.min.x_val),int(detection.box2D.min.y_val - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (36,255,12))

        #convert numpy array to Image
        msg_image = self.bridge.cv2_to_imgmsg(png, "bgr8")
        
        # gt_string = String()
        # gt_string.data = str('"'+frame_name + '":{' + str(self.gt[frame_name]) + '},')

        client.simClearDetectionMeshNames(camera_name, image_type)

        client.simPause(False)

        client = None

        tf.header.frame_id = "map"
        tf.child_frame_id = "mindful_camera"
        self.br.sendTransform(tf)

        msg_pose = PoseStamped()
        msg_pose.header.stamp = timestamp
        msg_pose.header.frame_id = "map"
        msg_pose.pose.position.x = tf.transform.translation.x
        msg_pose.pose.position.y = tf.transform.translation.y
        msg_pose.pose.position.z = tf.transform.translation.z
        msg_pose.pose.orientation.x = tf.transform.rotation.x
        msg_pose.pose.orientation.y = tf.transform.rotation.y
        msg_pose.pose.orientation.z = tf.transform.rotation.z
        msg_pose.pose.orientation.w = tf.transform.rotation.w
        self.pub_pose.publish(msg_pose)

        msg_image.header.stamp = timestamp
        msg_depth.header.stamp = timestamp
        self.pub_image.publish(msg_image)
        self.pub_depth.publish(msg_depth)

        self.pub_info.publish(msg_info)

        

        gt_string = String()

        #convert the dictiiary to string
        gt_string.data = str(json.dumps(self.gt.data))
        self.pub_ground_truth.publish(gt_string)
        self.frame_count += 1

        # client.simPause(False)

if __name__ == '__main__':

    #remove 'rgb' folder
    if os.path.exists('rgb'):
        os.remove('rgb')

    #remove 'depth' folder
    if os.path.exists('depth'):
        os.remove('depth')

    pub = AirSimPublisher()
