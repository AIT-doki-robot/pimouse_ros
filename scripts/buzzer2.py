#!/usr/bin/env python 
#encoding:utf-8

#include rospy
import rospy
from std_msgs.msg import UInt16 #read UInt16 from msg in std_msgs

def recv_buzzer(data):
    rospy.loginfo(type(data))#check the data type
    rospy.loginfo(data.data)#output the log to the standard output

if __name__ == '__main__':
    rospy.init_node('buzzer')#initialization of node
    #for receiving the data from the other node
    rospy.Subscriber("buzzer", UInt16, recv_buzzer)
    #Subscriber("topic name", data type, callback function)
    #callback function: function activated when receiving the data
    
    rospy.spin()#keep the node active(just for waiting)
    
