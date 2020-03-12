#!/usr/bin/env python
#encoding: utf-8
#日本語のテスト

import sys, rospy
#sys: library on process in Python
from pimouse_ros.msg import LightSensorValues
#from (package name) import (data type)

def get_freq():
    f = rospy.get_param('lightsensors_freq',10)
    #get_param(param_name): basic use
    #get_param(param_name): get the value from the parameter server
    #get_param(param_name,default_value) in case of the parameter doesn't exist
    try:
        if f <= 0.0:
            raise Exception()
    except:
        rospy.logger("value error: lightsensors_freq")
        sys.exit(1)

    return f

if __name__== '__main__':
    devfile = '/dev/rtlightsensor0'
    rospy.init_node('lightsensors') #node initialization
    pub = rospy.Publisher('lightsensors',LightSensorValues, queue_size=1)
    #Publisher(topic name, data type, queue size)

    freq = get_freq() # definition of the parameter freq
    rate = rospy.Rate(freq)#set the interval of loop using freq
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

        f = get_freq()#current value of freq
        if f != freq:#if the parameter is changed
            freq = f #put the new parameter into freq
            rate = rospy.Rate(freq) #set the interval into the new one
            
        rate.sleep()
          
