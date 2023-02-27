import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import os
import cv2

# Initialize the ROS node
rospy.init_node('image_saver')

# Initialize a CvBridge object to convert between ROS messages and OpenCV images
bridge = CvBridge()

# Define a function to get the name of the image file
# Takes the image number as an argument
# And returns the name of the image file with the following foramt: 0000000.png, 0000001.png, etc.
def get_image_name(img_counter):
    asStr: str = str(img_counter)
    result: str = ""
    for i in range(7 - len(asStr)):
        result += "0"
    result += asStr
    result += ".png"
    return result


# Define a callback function to process the images
def image_callback(msg):
    print("Received an image!")
    # Convert the ROS message to an OpenCV image
    cv_image = bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')

    #get number of files in the rgb/ folder
    count = len(os.listdir('./'))

    # Save the image to disk
    cv2.imwrite(get_image_name(count), cv_image, [int(cv2.IMWRITE_PNG_COMPRESSION), 0])
    print("Saved the image #"+str(count)+" to disk!")
    #os.system("pwd")
    #os.system("ls")

# Create the rgb/ folder if it doesn't exist
if not os.path.exists('/root/shared/src/rgb/'):
    os.system("mkdir -m 777 /root/shared/src/rgb")
    print("Created the rgb/ folder!")
else:
    os.system("rm -r /root/shared/src/rgb/*")

os.chdir('/root/shared/src/rgb/')

# Subscribe to the image topic
image_sub = rospy.Subscriber('/bh_image', Image, image_callback)

# Spin the ROS node to process incoming messages
rospy.spin()
