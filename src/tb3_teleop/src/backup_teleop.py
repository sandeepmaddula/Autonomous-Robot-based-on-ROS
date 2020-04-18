#!/usr/bin/env python
# -*- coding: utf-8 -*-

###################  import  ###########################
import rospy
from geometry_msgs.msg import Twist   #turtle cmd_vel message type
from sensor_msgs.msg import Joy

############# creation of objects  #####################
stop = 0
control = False
move = Twist()

#############  node initialization  ####################
rospy.init_node('teleop')

############ initialize values #########################
joy_topic = rospy.get_param('joy_topic', '/joy')
cmd_vel_topic = rospy.get_param('cmd_vel_topic', '/cmd_vel')


############ definitions of functions ##################
def callback(msg):
    global move
    global stop
    global control

    if msg.buttons[7]:
        stop = 1
    elif msg.buttons[6]:
        stop = 0
        control = not control

#    if msg.buttons[0]:
#        control = 1
#    elif msg.buttons[1]:
#        control = 0
        
    move.linear.x = msg.axes[3]
    move.angular.z = msg.axes[0]*2.0



#### definition of publisher/subscriber and services ###
rospy.Subscriber(joy_topic, Joy, callback)           #Subscriber for joystick cmd
pub = rospy.Publisher(cmd_vel_topic, Twist, queue_size=1)   #Publisher to robot

############# main program #############################

#--------------endless loop till shut down -------------#
rate = rospy.Rate(10)

while not rospy.is_shutdown():
    if stop:
        move.linear.x = 0
        move.angular.z = 0

    if control:
        pub.publish(move)
    
    rate.sleep()
