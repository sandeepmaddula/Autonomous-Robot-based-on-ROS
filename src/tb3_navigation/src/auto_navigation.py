#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import actionlib
import tf_conversions
import math
from sensor_msgs.msg import Joy
from move_base_msgs.msg import MoveBaseActionGoal, MoveBaseActionFeedback, MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import Pose
import actionlib_msgs

#############  node initialization  ####################
rospy.init_node('auto_navigation')


client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
client.wait_for_server()

def send_to_goal(goal_pose, absolute = True):
    global client

    #ori = tf_conversions.transformations.quaternion_from_euler(0, 0, math.pi)

    goal = MoveBaseGoal()
    goal.target_pose.pose = goal_pose

    if absolute:
        goal.target_pose.header.frame_id  = 'map'
    else:
        goal.target_pose.header.frame_id  = 'base_link'

    goal.target_pose.header.stamp     = rospy.Time.now()

    print goal

    client.send_goal(goal, done_cb, active_cb, feedback_cb)


def done_cb(state, result):
    if client.get_state() == actionlib_msgs.msg.GoalStatus.SUCCEEDED:
        #rospy.loginfo("Successfully reached goal")
        print "Successfully reached goal"
    elif client.get_state() == actionlib_msgs.msg.GoalStatus.PREEMPTED:
        #rospy.loginfo("Goal preempted by user!")
        print "Goal preempted by user!"
    else:
        #rospy.logerror("Other execution status of move_base actionclient")
        print "Other execution status of move_base actionclient"
        print client.get_state() 


def active_cb():
    pass

def feedback_cb(feedback):
    pass


def joy_cb(msg):
    global client

    if msg.buttons[7]:
        print '------cancelling goal-------'
        client.cancel_goal()

#### definition of publisher/subscriber and services ###
rospy.Subscriber('/joy', Joy, joy_cb)


############# main program #############################
goal_pose = Pose()
goal_pose.position.x = 0
goal_pose.position.y = -1
goal_pose.position.z = 0
ori = tf_conversions.transformations.quaternion_from_euler(0, 0, -math.pi/2)
goal_pose.orientation.x = ori[0]
goal_pose.orientation.y = ori[1]
goal_pose.orientation.z = ori[2]
goal_pose.orientation.w = ori[3]

send_to_goal(goal_pose, True)


#--------------endless loop till shut down -------------#
rate = rospy.Rate(10)

while not rospy.is_shutdown():
    #print 'running'
    
    rate.sleep()
