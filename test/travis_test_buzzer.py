#!/usr/bin/env python
#encoding: utf-8

# This is a test program for buzze1.py
#include of library
#unittest: Test framework in Phthon
import rospy, unittest, rostest
import rosnode
import time
from std_msgs.msg import UInt16

#definition of class
#Due to principles in unittest,
#the name of function for test should begin with "test_".
#In addition, the new function should be derived from "uniitest.TestCase".
class BuzzerTest(unittest.TestCase):
    #definition of instance
    def test_node_exist(self):#"self" means the instance itself, not the class.
        nodes = rosnode.get_node_names() #get the node list in active
        #assertIn(): word in the list, list, output in case not included
        self.assertIn('/buzzer', nodes, "node does not exist")

    #added function for studying Publisher
    def test_put_value(self):
        pub = rospy.Publisher('/buzzer', UInt16)#Publisher(topic name, data type)
        for i in range(10):
            pub.publish(1234)#publish the data "1234"
            time.sleep(0.1)

        with open("/dev/rtbuzzer0","r") as f:
            data = f.readline()
            self.asserEqual(data,"1234\n","value does not written to rtbuzzer0")
            #asserEqual(data,expected,actual) actual:executed when not be expected
        
if __name__ == '__main__': #main function in C++ or C
    time.sleep(3) #wait for node activation
    rospy.init_node('travis_test_buzzer') #node initialization
    #rostest.rosrun()
    #1st: package name for test, name of this package, class on test
    rostest.rosrun('pimouse_ros','travis_test_buzzer',BuzzerTest)
