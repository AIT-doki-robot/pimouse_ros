#!/usr/bin/env python
#encoding: utf-8

import unittest, rostest
import rosnode, rospy
import time
from pimouse_ros.msg import MotorFreqs
from geometry_msgs.msg import Twist

class MotorTest(unittest.TestCase):
    def file_check(self, dev, value, message):
        with open("/dev/"+dev,"r") as f: #open the device
            self.assertEqual(f.readline(), str(value)+"\n",message)

    def test_node_exist(self): #check for node existance
        nodes = rosnode.get_node_names()
        print(nodes)
        self.assertEqual('/motors', nodes, "node does not exist")

    def test_put_freq(self): #test for motor_raw
        pub = rospy.Publisher('/motor_raw', MotorFreqs)
        #definition of instance(not publishing)
        
        m = MotorFreqs()
        m.left_hz = 123
        m.right_hz = 456
        for i in range(10): # 10 times
            pub.publish(m) # actual publishing here
            time.sleep(0.1)

        self.file_check("rtmotor_raw_l0", m.left_hz, "wrong left value from motor_raw")
        self.file_check("rtmotor_raw_r0", m.right_hz, "wrong right value from motor_raw")

    def test_put_cmd_vel(self): #test for cmd_vel
        pub = rospy.Publisher('/cmd_vel',Twist)
        #definition of instance(not publishing)
        m = Twist()

        m.linear.x = 0.1414
        m.angular.z = 1.57
        for i in range(10):
            pub.publish(m) #actual publishing here
            time.sleep(0.1)

        self.file_check("rtmotor_raw_l0", 200, "wrong left value from cmd_vel")
        self.file_check("rtmotor_raw_r0",600, "wrong right value from cdm_vel")
        time.sleep(1.1)

        self.file_check("rtmotor_raw_l0",0, "don't stop after 1[s]")
        self.file_check("rtmotor_raw_r0",0, "don't stop after 1[s]")

if __name__ == '__main__':
    time.sleep(3)
    rospy.init_node('travis_test_motors')
    rostest.rosrun('pimouse_ros','travis_test_motors',MotorTest)
