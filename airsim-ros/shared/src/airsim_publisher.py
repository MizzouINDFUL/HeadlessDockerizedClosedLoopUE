import rospy
import message_filters
from cv_bridge import CvBridge
from sensor_msgs.msg import Image, CameraInfo
from geometry_msgs.msg import PoseStamped

import tf2_ros


class AirSimPublisher():

    def __init__(self):

        rospy.init_node('airsim_publisher', anonymous=True)

        self.bridge = CvBridge()

        self.tfBuffer = tf2_ros.Buffer()
        self.tfListener = tf2_ros.TransformListener(self.tfBuffer)
        self.br = tf2_ros.TransformBroadcaster()

        queue_size = 1
        topic = 'mindful'

        self.pub_info = rospy.Publisher(f'{topic}_info', CameraInfo, queue_size=queue_size)
        self.pub_pose = rospy.Publisher(f'{topic}_pose', PoseStamped, queue_size=queue_size)
        self.pub_image = rospy.Publisher(f'{topic}_image', Image, queue_size=queue_size)
        self.pub_depth = rospy.Publisher(f'{topic}_depth', Image, queue_size=queue_size)

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
            print(tf)
        except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
            print('exception')
            return

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


if __name__ == '__main__':
    pub = AirSimPublisher()
