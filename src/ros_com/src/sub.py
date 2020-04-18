#!/usr/bin/env python

# import #
import rospy
from std_msgs.msg import String

# node initialization #
rospy.init_node("sub")

# definitions of variables #


# definitions of functions #
def callback(msg):

    print msg.data

# definition of publisher/subscriber and services #
rospy.Subscriber('first_topic', String, callback)

# main program #
rospy.spin()
