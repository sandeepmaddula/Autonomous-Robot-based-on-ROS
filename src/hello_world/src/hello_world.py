#!/usr/bin/env python

import rospy

rospy.init_node('hello_world')
freq = rospy.get_param("freq", 10)
text = rospy.get_param("text", "Hello World!")

rate = rospy.Rate(freq)

#print "Hello world!", rospy.Time.now()


while not rospy.is_shutdown():
    # ADD YOUR CODE HERE
    print text, rospy.get_time()
    rate.sleep()
