#!/usr/bin/env python
# -*- coding: utf-8 -*-

###################  import  ###########################
import rospy
from std_msgs.msg import String           #keyboard cmd message type
from geometry_msgs.msg import Twist   #turtle cmd_vel message type
from std_srvs.srv import Empty
from maskor_turtlesim.srv import Kill
from maskor_turtlesim.srv import Spawn

import random

############# creation of objects  #####################

#############  node initialization  ####################
rospy.init_node('keyboard_control', anonymous=True)

##### initialize values ####
cmd_vel_topic = rospy.get_param('cmd_vel_topic', '/turtle1/cmd_vel')
key_cmd_topic = rospy.get_param('key_cmd_topic', '/keyboard_cmd')
speed_scaling = rospy.get_param('speed_scaling', 1)

############ definitions of functions ##################
def callback(msg):

	global speed_scaling

	move = Twist()

	if msg.data == "UP":
		move.linear.x = 1
	elif msg.data == "DOWN":
		move.linear.x = -1
	elif msg.data == "LEFT":
		move.angular.z = 1
	elif msg.data == "RIGHT":
		move.angular.z = -1

	elif msg.data == "PLUS":
		speed_scaling += 1
	elif msg.data == "MINUS":
		speed_scaling -=1

	elif msg.data == "CLEAR":
		clear()
	elif msg.data == "RESET":
		reset()
	elif msg.data == "KILL":
		kill()
	elif msg.data == "SPAWN":
		spawn()
	
	move.linear.x = move.linear.x * speed_scaling
	move.angular.z = move.angular.z * speed_scaling	

	pub.publish(move)



def clear():
    rospy.wait_for_service('clear')
    try:
        clear = rospy.ServiceProxy('clear', Empty)
        clear()
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e


def reset():
    rospy.wait_for_service('reset')
    try:
        reset = rospy.ServiceProxy('reset', Empty)
        reset()
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e


def kill():
    rospy.wait_for_service('kill')
    try:
        kill = rospy.ServiceProxy('kill', Kill)
        kill("turtle1")
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e


def spawn():
    rospy.wait_for_service('spawn')
    try:
        spawn = rospy.ServiceProxy('spawn', Spawn)
        name = spawn(random.uniform(0,10),random.uniform(0,10),0,"")
	print "Spawned turtle with",name
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e


#### definition of publisher/subscriber and services ###
rospy.Subscriber(key_cmd_topic, String, callback)           #Subscriber for keyboard cmd
pub = rospy.Publisher(cmd_vel_topic, Twist, queue_size=1)   #Publisher to turtlesim


############# main program #############################

#--------------endless loop till shut down -------------#
rospy.spin()



