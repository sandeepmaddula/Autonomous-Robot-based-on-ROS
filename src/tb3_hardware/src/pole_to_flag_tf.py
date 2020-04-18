#!/usr/bin/env python

import rospy
import tf2_ros
import tf_conversions
import geometry_msgs

from nav_msgs.msg import Odometry
from geometry_msgs.msg import Pose

############# creation of objects  #####################
odo = Pose()

br = tf2_ros.TransformBroadcaster()

def get_flag_tf():
    t = geometry_msgs.msg.TransformStamped()
    #calculating transform
    t.header.stamp = rospy.Time.now()
    t.header.frame_id = "pole_link"
    t.child_frame_id = "flag_link"
    t.transform.translation.x = 0
    t.transform.translation.y = 0
    t.transform.translation.z = 0.02
    q = tf_conversions.transformations.quaternion_from_euler(0,0,-odo.orientation.z)
    t.transform.rotation.x = q[0]
    t.transform.rotation.y = q[1]
    t.transform.rotation.z = q[2]
    t.transform.rotation.w = q[3]
    return t

def callback(msg):
    global odo
    odo = msg.pose.pose
    print msg.pose.pose.position.x
    

#### definition of publisher/subscriber and services ###
rospy.Subscriber('/odom', Odometry, callback) 


#### main program 
if __name__ == '__main__':
    rospy.init_node("pole_to_flag_tf")
    rate = rospy.Rate(50)

    while not rospy.is_shutdown():
        br.sendTransform(get_flag_tf())
        rate.sleep()
