#!/usr/bin/env python
# -*- coding: utf-8 -*-

###################  import  ###########################
import rospy
from geometry_msgs.msg import PoseWithCovarianceStamped

import math

############# creation of objects  #####################

#############  node initialization  ####################
rospy.init_node('cov_printer')


############ definitions of functions ##################
def callback(msg):
    err = math.sqrt(msg.pose.covariance[0] + msg.pose.covariance[7])
    print 'position error: ' + str(err)


#### definition of publisher/subscriber and services ###
rospy.Subscriber('amcl_pose', PoseWithCovarianceStamped, callback)           #Subscriber
#pub = rospy.Publisher(cmd_vel_topic, Twist, queue_size=1)   #Publisher to turtlesim

############# main program #############################

#--------------endless loop till shut down -------------#
rospy.spin()
