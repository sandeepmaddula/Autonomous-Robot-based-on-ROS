#!/usr/bin/env python

import rospy
import tf2_ros
from geometry_msgs.msg import TransformStamped

rospy.init_node('node_listener')    #init node

transformData = TransformStamped()        #setup object to receive transform
tfBuffer = tf2_ros.Buffer()
listener = tf2_ros.TransformListener(tfBuffer)   #setup tf listener

rate = rospy.Rate(10.0)             #set spin rate to 10 Hz

while not rospy.is_shutdown():

  #lookup for the newest transform
  try:
    transformData = tfBuffer.lookup_transform('camera_link', 'ar_marker_19', rospy.Time(0))

    print transformData
    print '########'

  except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
    pass

  rate.sleep()
