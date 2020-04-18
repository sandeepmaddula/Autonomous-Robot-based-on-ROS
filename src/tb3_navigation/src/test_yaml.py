#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import yaml
from geometry_msgs.msg import Pose

try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

pose = Pose()

pose.position.x = 4
pose.position.y = 5
pose.position.z = 6


#with open('../data/test.yaml', 'a') as outfile:
#    yaml.dump(pose, outfile, default_flow_style=False)

#stream = file('../data/test.yaml', 'r')
#res = yaml.load(stream, Loader=Loader)
#print res

pnt = {
  'x': 1,
  'y': 1,
  'theta': 2.5
}

pnts = {
    19: {
        'x': 1,
        'y': 1,
        'a': 0
    },

    9: {
        'x': 2,
        'y': 1,
        'a': 0
    }
}

print pnts


