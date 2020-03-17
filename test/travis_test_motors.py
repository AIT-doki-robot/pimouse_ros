#!/usr/bin/env python
#encoding: utf-8

import unittest, rostest
import rosnode, rospy
import time
from pimouse_ros.msg import MotorFreqs
from geometry_msgs.msg import Twist
from std_srvs.srv import Trigger, TriggerResponse #Add service
from pimouse_ros.srv import TimedMotion #Add a new service

class MotorTest(unittest.TestCase):
    def setUp(self):
        rospy.wait_for_service('/motor_on')#wait for service activation
        rospy.wait_for_service('/motor_off')
        rospy.wait_for_service('/timed_motion')#Wait for service activation

        on = rospy.ServiceProxy('/motor_on', Trigger)#service instance generation
    
    def file_check(self, dev, value, message):
        with open("/dev/"+dev,"r") as f: #open the device
            self.assertEqual(f.readline(), str(value)+"\n",message)

    def test_node_exist(self): #check for node existance
        nodes = rosnode.get_node_names()
        print(nodes)
        self.assertIn('/motors', nodes, "node does not exist")

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

    def test_on_off(self):
        #test for motor on ->off
        off = rospy.ServiceProxy('/motor_off',Trigger)#service instance generation
        #Simultaneously, the motor becomes off using the service '/motor_off'
        ret = off()

        self.assertEqual(ret.success, True, "motor off does not succeeded")
        self.assertEqual(ret.message, "OFF", "motor off wrong mesage")

        with open("/dev/rtmotoren0","r") as f:
            data = f.readline()
            self.assertEqual(data,"0\n","wrong value in rtmotor0 at motor off")

        #test for motor off -> on
        on = rospy.ServiceProxy('/motor_on', Trigger) # motor on
        ret = on()

        self.assertEqual(ret.success, True, "motor on does not succeeded")
        self.assertEqual(ret.message, "ON", "motor on wrong message")
        with open("/dev/rtmotoren0","r") as f:
            data = f.readline()
            self.assertEqual(data,"1\n","wrong value in rtmotor0 at motor on")

    def test_put_value_timed(self):
        #test for timed motion
        tm = rospy.ServiceProxy('/timed_motion', TimedMotion)#generation instance
        tm(-321,654,1500) #actual input to timed motion
        with open("/dev/rtmotor0", "r") as f:
            data = f.readline()
            self.assertEqual(data, "-321 654 1500\n","value does not written to rtmotor0")

if __name__ == '__main__':
#    time.sleep(3)
    rospy.init_node('travis_test_motors')
    rostest.rosrun('pimouse_ros','travis_test_motors',MotorTest)
