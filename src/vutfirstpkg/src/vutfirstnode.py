#!/usr/bin/env python

import rospy

rospy.init_node('vutfirstnode')
rate = rospy.Rate(10)

if rospy.has_param("turtleviz/background_b"):
    print "Parameter found!"

color_b = rospy.get_param("turtleviz/background_b")
print color_b

rospy.set_param("turtleviz/background_b", 10)

color_b = rospy.get_param("turtleviz/background_b")
print color_b

while not rospy.is_shutdown():
    # ADD YOUR CODE HERE
    #print "hello"
    rate.sleep()
