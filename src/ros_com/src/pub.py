#!/usr/bin/env python

# import #
import rospy
from std_msgs.msg import String

# node initialization #
rospy.init_node("pub")

# definitions of variables #
msg_string = String()

# definitions of functions #

# definition of publisher/subscriber and services #
pub = rospy.Publisher('first_topic', String, queue_size=1)

# main program #
r = rospy.Rate(5) #5 Hz

while not rospy.is_shutdown():

    # write a string to the ROS message field
    msg_string.data = "Welcome to ROS!"
    pub.publish(msg_string)
    r.sleep()


