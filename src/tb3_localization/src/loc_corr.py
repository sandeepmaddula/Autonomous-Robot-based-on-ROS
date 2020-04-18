#!/usr/bin/env python
# -*- coding: utf-8 -*-

###################  import  ###########################
import rospy
from std_srvs.srv import Empty
from geometry_msgs.msg import PoseWithCovarianceStamped
from geometry_msgs.msg import Twist

import math

############# creation of objects  #####################
resflag = 0
rotflag = 0
move = Twist()

#############  node initialization  ####################
rospy.init_node('loc_corr')


############ definitions of functions ##################
def reset_filter():
    rospy.wait_for_service('global_localization')
    try:
        reset = rospy.ServiceProxy('global_localization', Empty)
        reset()
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e


def callback(msg):
    global resflag
    global rotflag

    err = math.sqrt(msg.pose.covariance[0] + msg.pose.covariance[7])
    print 'position variance: ' + str(err)
    angerr = math.sqrt(msg.pose.covariance[35]) * 180.0 / math.pi
    print 'angle variance: ' + str(angerr)

    if resflag == 0 and (err > 0.15 or angerr > 10):
        reset_filter()
        resflag = 100
        rotflag = 60
        print 'resetting filter'

    if err < 0.15 and angerr < 10:
        rotflag = 0


rospy.Subscriber('amcl_pose', PoseWithCovarianceStamped, callback)           #Subscriber
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)


############# main program #############################

rate = rospy.Rate(10)
#--------------endless loop till shut down -------------#

while not rospy.is_shutdown():
    if resflag > 0:
        resflag -= 1
    if rotflag > 0:
        if rotflag > 20 and rotflag < 40:
            move.linear.x = 0.0
            move.angular.z = 2.0
        else:
            move.linear.x = 0.25    
            move.angular.z = 0.0

        pub.publish(move)
        print 'rotating: ' + str(rotflag)
        rotflag -= 1

#    print resflag
    rate.sleep()
