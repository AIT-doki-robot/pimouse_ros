#!/usr/bin/env python 
#encoding:utf-8

#include rospy
import rospy

#initialization of node, then registered the node into ROS
rospy.init_node('buzzer')

# keep the node active (for waiting)
rospy.spin()
