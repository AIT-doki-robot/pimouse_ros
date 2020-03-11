#!/usr/bin/env python
#encoding: utf-8

# This is a test program for buzze1.py
#include of library
#unittest: Test framework in Phthon
import rospy, unittest, rostest
import rosnode
import time

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

if __name__ == '__main__': #main function in C++ or C
    time.sleep(3) #wait for node activation
    rospy.init_node('travis_test_buzzer') #node initialization
    #rostest.rosrun()
    #1st: package name for test, name of this package, class on test
    rostest.rosrun('pimouse_ros','travis_test_buzzer',BuzzerTest)
