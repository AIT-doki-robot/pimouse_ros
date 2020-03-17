#!/usr/bin/env python
#encoding: utf-8

#include
#for using math library: math
import rospy, sys, math
from pimouse_ros.msg import MotorFreqs
from geometry_msgs.msg import Twist
from std_srvs.srv import Trigger, TriggerResponse #Add two services from std_srvs
from pimouse_ros.srv import TimedMotion

class Motor():
    def __init__(self): # __init__: called when instance production
        if not self.set_power(False): sys.exit(1) #shutdown the motor if motor is on

        rospy.on_shutdown(self.set_power)
        self.sub_raw = rospy.Subscriber('motor_raw', MotorFreqs, self.callback_raw_freq)
        #subscribe raw data from callback function
        self.sub_cmd_vel = rospy.Subscriber('cmd_vel', Twist, self.callback_cmd_vel)
        #Definition of Service instance
        self.srv_on = rospy.Service('motor_on', Trigger, self.callback_on)
        self.srv_off = rospy.Service('motor_off', Trigger, self.callback_off)

        self.last_time = rospy.Time.now() # Record the time to be subscribed
        self.using_cmd_vel = False #whether cmd_vel is used

        self.srv_tm = rospy.Service('timed_motion', TimedMotion, self.callback_tm)

    def set_power(self, onoff=False):
        en = "/dev/rtmotoren0"
        try:
            with open(en, "w") as f: #open "/dev/rtmotoren0" in written mode
                f.write("1\n" if onoff else "0\n") # onoff=True -> 1, onoff=False ->0
            self.is_on = onoff #record ot motor status
            return True
        except:
            rospy.logger(" cannot write to " +en)
        return False

    def set_raw_freq(self, left_hz, right_hz):
        if not self.is_on:
            rospy.logger("not enpowered")
            return
        try:
            with open("/dev/rtmotor_raw_l0",'w') as lf,\
                 open("/dev/rtmotor_raw_r0",'w') as rf:
                lf.write(str(int(round(left_hz)))+"\n")
                # round(): 指定した桁で四捨五入。指定がなければ整数になる
                rf.write(str(int(round(right_hz)))+"\n")
        except:
            rospy.logerr("cannot write to rtmotor_raw_*")

    def onoff_response(self,onoff):
        d = TriggerResponse()
        d.success = self.set_power(onoff)
        d.message = "ON" if self.is_on else "OFF"
        return d

    def callback_on(self, message): return self.onoff_response(True)
    def callback_off(self, message): return self.onoff_response(False)

    def callback_raw_freq(self, message):
        self.set_raw_freq(message.left_hz, message.right_hz)

    def callback_cmd_vel(self, message):
        forward_hz = 80000.0*message.linear.x/(9*math.pi)
        rot_hz = 400.0*message.angular.z/math.pi
        print(forward_hz, rot_hz)
        self.set_raw_freq(forward_hz - rot_hz, forward_hz + rot_hz)
        self.using_cmd_vel = True
        self.last_time = rospy.Time.now()

    def callback_tm(self, message):
        if not self.is_on: # motor is not on
            rospy.logerr("not enpowered") #record the error
            return False #return False

        dev = "/dev/rtmotor0" #instance of device name
        try:
            with open(dev,'w') as f: #open the device file
                f.write("%d %d %d\n" %
                        (message.left_hz, message.right_hz, message.duration_ms))
                #write the values to the device file
        except:
            rospy.logerr("cannot write to "+dev)
            return False

        return True
    
if __name__ == '__main__':
    rospy.init_node('motors') #initialization of node
    m = Motor() #instance production
    
    rate = rospy.Rate(10)#set the interval of loop using (freq)

    while not rospy.is_shutdown():
            if m.using_cmd_vel and rospy.Time.now().to_sec() -m.last_time.to_sec() >=1.0 :
                m.set_raw_freq(0,0)
                m.using_cmd_vel = False
            rate.sleep()
