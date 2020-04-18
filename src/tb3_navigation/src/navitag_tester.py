#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import actionlib
import tf_conversions
import math
from sensor_msgs.msg import Joy
from move_base_msgs.msg import MoveBaseActionGoal, MoveBaseActionFeedback, MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import Pose
from geometry_msgs.msg import Twist
import actionlib_msgs
from ar_track_alvar_msgs.msg import AlvarMarkers
from std_msgs.msg import Int16


#############  AR tags position definition  ####################

townA = {
    6: {
        'x': 0.80,
        'y': 0.97,
        'z': 0.631,
        'w': 0.776
    },

    7: {
        'x': 1.51,
        'y': -0.39,
        'z': 0.288,
        'w': 0.958
    },

    8: {
        'x': 2.20,
        'y': -1.00,
        'z': -0.788,
        'w': 0.612
    },

    4: {
        'x': 4.13,
        'y': -0.89,
        'z': 0.549,
        'w': 0.836
    },

    3: {
        'x': 3.64,
        'y': -2.46,
        'z': -0.448,
        'w': 0.894
    },

    9: {
        'x': 2.28,
        'y': -2.68,
        'z': 0.712,
        'w': 0.702
    },

    2: {
        'x': 2.33,
        'y': -3.00,
        'z': -0.092,
        'w': 0.996
    },

    1: {
        'x': 0.63,
        'y': -2.36,
        'z': 0.935,
        'w': -0.355
    },

    0: {
        'x': 0.19,
        'y': -1.46,
        'z': 0.741,
        'w': 0.672
    },

    5: {
        'x': 2.58,
        'y': 0.65,
        'z': 0.945,
        'w': -0.328
    }
}

townB = {
    6: {
        'x': 0.34,
        'y': -0.68,
        'z': -0.704,
        'w': 0.711
    },

    5: {
        'x': 2.08,
        'y': -1.08,
        'z': 0.835,
        'w': 0.550
    },

    4: {
        'x': 3.91,
        'y': 0.13,
        'z': -0.414,
        'w': 0.910
    },

    3: {
        'x': 3.59,
        'y': 2.75,
        'z': 0.102,
        'w': 0.995
    },

    2: {
        'x': 1.99,
        'y': 2.81,
        'z': -0.106,
        'w': 0.994
    },

    9: {
        'x': 2.10,
        'y': 2.66,
        'z': -0.830,
        'w': 0.559
    },

    1: {
        'x': 0.47,
        'y': 2.36,
        'z': 0.883,
        'w': 0.469
    },

    0: {
        'x': 0.01,
        'y': 1.40,
        'z': -0.738,
        'w': 0.675
    },

    7: {
        'x': 1.32,
        'y': 0.15,
        'z': -0.504,
        'w': 0.864
    },

    8: {
        'x': 1.92,
        'y': 0.76,
        'z': 0.667,
        'w': 0.745
    }
}



#############  node initialization  ####################
rospy.init_node('navitag_tester')


client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
client.wait_for_server()

town = rospy.get_param('~town','townA')
last_goal_id = 0
recovery_move = 0

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
    global last_goal_id
    global recovery_move

    if client.get_state() == actionlib_msgs.msg.GoalStatus.SUCCEEDED:
        #rospy.loginfo("Successfully reached goal")
        print "Successfully reached goal"
        last_goal_id += 1
        if last_goal_id <= 9:
            print 'Navigating to AR tag ' + str(last_goal_id)
            send_to_goal(get_goal(last_goal_id))

    elif client.get_state() == actionlib_msgs.msg.GoalStatus.PREEMPTED:
        #rospy.loginfo("Goal preempted by user!")
        print "Goal preempted by user!"

    elif client.get_state() == 4: #selhani hledani planu
        print "Goal is not reachable!"
        recovery_move = 20

    else:
        #rospy.logerror("Other execution status of move_base actionclient")
        print "Other execution status of move_base actionclient"
        print client.get_state() 


def get_goal(tag_id):
    global town
    goal_pose = Pose()

    goal_pose.position.x = town[tag_id]['x']
    goal_pose.position.y = town[tag_id]['y']
    goal_pose.position.z = 0

    goal_pose.orientation.x = 0
    goal_pose.orientation.y = 0
    goal_pose.orientation.z = town[tag_id]['z']
    goal_pose.orientation.w = town[tag_id]['w']

    return goal_pose


def active_cb():
    pass

def feedback_cb(feedback):
    pass


def joy_cb(msg):
    global client

    if msg.buttons[7]:
        print '------cancelling goal-------'
        client.cancel_goal()


def marker_cb(msg):
    if not msg.markers:
        return
    global last_goal_id
    if int(msg.markers[0].id) == int(last_goal_id):
        last_goal_id += 1
        if last_goal_id <= 9:
            print 'Navigating to AR tag ' + str(last_goal_id)
            send_to_goal(get_goal(last_goal_id))

def goal_cb(msg):
    global last_goal_id
    if last_goal_id == msg.data:
        return

    last_goal_id = msg.data
    print 'Navigating to AR tag ' + str(msg.data)
    send_to_goal(get_goal(last_goal_id))


#### definition of publisher/subscriber and services ###
rospy.Subscriber('/joy', Joy, joy_cb)
#rospy.Subscriber('/ar_pose_marker', AlvarMarkers, marker_cb)
rospy.Subscriber('/next_goal', Int16, goal_cb)

pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)


############# main program #############################

#send_to_goal(get_goal(last_goal_id))


#--------------endless loop till shut down -------------#
rate = rospy.Rate(10)

while not rospy.is_shutdown():
    #print 'running'

    if recovery_move > 0:
        print 'recovering: ' + str(recovery_move)
        move = Twist()
        move.linear.x = 0.0
        move.angular.z = 1.0
        pub.publish(move)

        recovery_move -= 1
        if recovery_move == 0:
            print 'Navigating to AR tag ' + str(last_goal_id)
            send_to_goal(get_goal(last_goal_id))
        
    
    rate.sleep()
