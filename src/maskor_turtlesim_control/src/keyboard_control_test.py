#!/usr/bin/env python

import rospy
from std_srvs.srv import Empty
from std_msgs.msg import String

rospy.init_node('keyboard_control', anonymous=True)

key_cmd_topic = rospy.get_param('key_cmd_topic','/keyboard_cmd')

def callback(msg):
	if msg.data == "RESET":
		reset()

def reset():
	rospy.wait_for_service('reset')
	try:
		reset_srv = rospy.ServiceProxy('reset', Empty)
		reset_srv()
	except rospy.ServiceException, e:
		print "Service call failed: %s" %e

def spawn():
	x = random.uniform(0,10)
	y = random.uniform(0,10)
	
	rospy.wait_for_service('spawn')
	try:
		spawn_srv = rospy.ServiceProxy('spawn', Spawn)
		resp = spawn_srv(x,y,0,"")
		print "Spawned turtle with",resp
	except rospy.ServiceException, e:
		print "Service call failed: %s"%e

rospy.Subscriber(key_cmd_topic, String, callback)

rospy.spin()
