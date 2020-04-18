#!/usr/bin/env python

import rospy
import tf2_ros
import math
from geometry_msgs.msg import TransformStamped
from geometry_msgs.msg import Twist

rospy.init_node('node_listener')    #init node

desired_dist = rospy.get_param("~desired_dist", 1.5)
dist_deadzone = rospy.get_param("~dist_deadzone", 0.1)
dist_sat = rospy.get_param("~dist_sat", 0.5)
max_speed = rospy.get_param("~max_speed", 0.25)
angle_deadzone = rospy.get_param("~angle_deadzone", 1.0)
angle_sat = rospy.get_param("~angle_sat", 10.0)
eps_min = rospy.get_param("~eps_min", 0.5)
eps_sat = rospy.get_param("~eps_sat", 7.0)

transformData = TransformStamped()        #setup object to receive transform
tfBuffer = tf2_ros.Buffer()
listener = tf2_ros.TransformListener(tfBuffer)   #setup tf listener

rate = rospy.Rate(20.0)             #set spin rate to 10 Hz

pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)   #Publisher to robot

while not rospy.is_shutdown():

  #lookup for the newest transform
    move = Twist()
    move.linear.x = 0
    move.angular.z = 0

    #print 'rt' + str(rospy.get_rostime().secs)
    curr_time = rospy.get_rostime()

#    print type(curr_time)

    try:
        transformData = tfBuffer.lookup_transform('base_link', 'ar_marker_19', rospy.Time(0))

        dur = curr_time - transformData.header.stamp
        diff = dur.secs + dur.nsecs / 1000000000.0

        print "---stari: " + str(diff)
        if diff < 1.2:
#            dxy = math.sqrt(transformData.transform.translation.z * transformData.transform.translation.z + transformData.transform.translation.y * transformData.transform.translation.y)
            dist = transformData.transform.translation.x

            phi = math.atan2(transformData.transform.translation.y, dist)

            phi = phi * 180.0 / math.pi

            print 'distance: ' + str(dist)
            print 'angle: ' + str(phi)

            dx = desired_dist - dist

            if math.fabs(dx) < dist_deadzone:
                move.linear.x = 0
            elif math.fabs(dx) > dist_sat:
                move.linear.x = -math.copysign(1, dx)
            else:
                move.linear.x = -math.copysign((math.fabs(dx) - dist_deadzone) / (dist_sat - dist_deadzone), dx)


            dphi = 0.0 - phi
            eps = 1.0

            if math.fabs(dphi) < angle_deadzone:
                move.angular.z = 0
            elif math.fabs(dphi) > angle_sat:
                move.angular.z = -math.copysign(1, dphi)
            else:
                move.angular.z = -math.copysign((math.fabs(dphi) - angle_deadzone) / (angle_sat - angle_deadzone), dphi)

            if math.fabs(dphi) > eps_sat:
                eps = eps_min
            else:
                eps = 1 - eps_min * math.fabs(dphi) / eps_sat

            move.linear.x *= max_speed * eps
#            move.angular.z *= 0.3
                
            print move.linear.x
            print move.angular.z

#            if transformData.transform.translation.x > 1:
#                move.linear.x = 0.2

#        print transformData
#        print '########'

    except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
        pass

    pub.publish(move)

    rate.sleep()
