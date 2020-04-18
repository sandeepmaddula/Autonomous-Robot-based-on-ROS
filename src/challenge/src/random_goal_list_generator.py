#!/usr/bin/env python

# import #
import rospy
from std_msgs.msg import Int16
from ar_track_alvar_msgs.msg import AlvarMarkers
import random

# node initialization #
rospy.init_node("random_goal_list_generator")


# definitions of variables #
next_goal = random.randint(0, 9)
last_goal = next_goal

msg_int = Int16()

# definitions of functions #
def generate_next_goal():
    global next_goal, last_goal
    while last_goal == next_goal:
        goal_range = range(last_goal - 3, last_goal - 2) + range(last_goal + 2, last_goal + 4)
        next_goal = random.choice(goal_range)
        if next_goal > 9:
            next_goal -= 9
        if next_goal < 0:
            next_goal += 9
    last_goal = next_goal
    print("Next goal: " + str(next_goal))


def callback(msg):
    if not msg.markers:
        return
    global next_goal, last_goal
    if int(msg.markers[0].id) == int(last_goal):
        generate_next_goal()

# definition of publisher/subscriber and services #
pub = rospy.Publisher('next_goal', Int16, queue_size=1)
rospy.Subscriber('ar_pose_marker', AlvarMarkers, callback)

# main program #
generate_next_goal()

r = rospy.Rate(10) #10 Hz
while not rospy.is_shutdown():
    # write a string to the ROS message field
    msg_int.data = next_goal
    pub.publish(msg_int)
    r.sleep()
