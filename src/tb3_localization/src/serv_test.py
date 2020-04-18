#!/usr/bin/env python
# -*- coding: utf-8 -*-

###################  import  ###########################
import rospy
from std_srvs.srv import Empty

############# creation of objects  #####################

#############  node initialization  ####################
rospy.init_node('serv_test')


############ definitions of functions ##################
def update_filter():
    rospy.wait_for_service('global_localization')
    try:
        update = rospy.ServiceProxy('global_localization', Empty)
        update()
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e


############# main program #############################

update_filter()

#--------------endless loop till shut down -------------#
#rospy.spin()
