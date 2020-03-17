#!/usr/bin/env python
#encoding: utf-8

# This is a test program for buzze1.py
#include of library
#unittest: Test framework in Phthon
import rospy, unittest, rostest, actionlib
import rosnode
import time
from std_msgs.msg import UInt16
from pimouse_ros.msg import MusicAction, MusicResult, MusicFeedback, MusigGoal

#definition of class
#Due to principles in unittest,
#the name of function for test should begin with "test_".
#In addition, the new function should be derived from "uniitest.TestCase".
class BuzzerTest(unittest.TestCase):
    #Add SetUp for Action test
    def SetUp(self):
        self.client = actionlib.SimpleActionClient("/music",MusicAction)
        #create a client for action
        self.device_values = []
        #create a list instance for values in the device file
    
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
            self.assertEqual(data,"1234\n","value does not written to rtbuzzer0")
            #asserEqual(data,expected,actual) actual:executed when not be expected
    #added function for music test
    def test_music(self):
        goal = MusicGoal() # create a instance for action goal
        goal.freqs = [100, 200, 300, 400, 0] #set the frequency
        goal.durations = [1.0, 2.0, 3.0, 2.0] #set the duration

        self.client.wait_for_server() #wait for server
        self.client.send_goal(goal, feedback_cb = self.feedback_cb)
        #send goal, 2nd item is callback function to catch the feedback
        self.client.wait_for_server()

        self.assertTrue(self.client.get_result(), "Invalid result")
        self.assertEqual(goal.freqs, self.device_values, "Invalid feedback:" + ",".join([str(e) for e in self.device_values]))

        ##preemotion##
        self.device_values = [] #empty device values
        self.client.send_goal(goal, feedback_cb = self.feedback_cb)
        #send the goal to preempt
        
        self.client.wait_for_result(rospy.Duration.from_sec(0.5))

        self.asserFalse(self.client.get_result(), "stop is requested but return true")
        self.assertFalse(goal.freqs == self.device_values, "not stopped")

    def feedback_cb(self, feedback):
        with open("/dev/rtbuzzer0","r") as f:
            data = f.readline()
            self.device_values.append(int(data.rstrip()))
            # read values in the device file and add the list
        
if __name__ == '__main__': #main function in C++ or C
    time.sleep(3) #wait for node activation
    rospy.init_node('travis_test_buzzer') #node initialization
    #rostest.rosrun()
    #1st: package name for test, name of this package, class on test
    rostest.rosrun('pimouse_ros','travis_test_buzzer',BuzzerTest)
