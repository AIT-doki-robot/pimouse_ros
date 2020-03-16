#!/usr/bin/env python

import sys, rospy
from pimouse_ros.msg import LightSensorValues
#from (package name) import (data type)

if __name__== '__main__':
    devfile = '/dev/rtlightsensor0'
    rospy.init_node('lightsensors') #node initialization
    pub = rospy.Publisher('lightsensors',LightSensorValues, queue_size=1)
    #Publisher(topic name, data type, queue size)

    rate = rospy.Rate(10)#interval of loop [Hz]
    while not rospy.is_shutdown():#judge for shutdown the program
        try:
            with open(devfile,'r') as f:
                data = f.readline().split()
                #data is split because the device send each data with "space"
                data = [ int(e) for e in data ]
                # input each value in data to d,then transform string to integer
                d = LightSensorValues()
                d.right_forward = data[0]
                d.right_side = data[1]
                d.left_side = data[2]
                d.left_forward = data[3]
                d.sum_all = sum(data)
                d.sum_forward = data[0]+data[3]
                pub.publish(d)
        except IOError:
            rospy.logger("cannot write to "+devfile)

        rate.sleep()
          
