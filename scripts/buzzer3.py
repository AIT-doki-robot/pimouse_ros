#!/usr/bin/env python 
#encoding:utf-8

#include rospy
import rospy
from std_msgs.msg import UInt16 #read UInt16 from msg in std_msgs

def write_freq(hz=0):
    bfile = "/dev/rtbuzzer0"
    try:
        with open(bfile,"w") as f:
            f.write(str(hz) + "\n")
    except IOError:
        rospy.logerr("can't write to " + bfile)

def recv_buzzer(data):
    write_freq(data.data)

if __name__ == '__main__':
    rospy.init_node('buzzer')#initialization of node
    #for receiving the data from the other node
    rospy.Subscriber("buzzer", UInt16, recv_buzzer)
    #Subscriber("topic name", data type, callback function)
    #callback function: function activated when receiving the data
    
    rospy.spin()#keep the node active(just for waiting)
    
