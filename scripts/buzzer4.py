#!/usr/bin/env python 
#encoding:utf-8

#include rospy
import rospy, actionlib #Add actionlib for action server
from std_msgs.msg import UInt16 #read UInt16 from msg in std_msgs
from pimouse_ros.msg import MusicAction, MusicResult, MusicFeedback

def write_freq(hz=0):
    bfile = "/dev/rtbuzzer0"
    try:
        with open(bfile,"w") as f:
            f.write(str(hz) + "\n")
    except IOError:
        rospy.logerr("can't write to " + bfile)

def recv_buzzer(data):
    write_freq(data.data)

def exec_music(goal): # pass: executing noting
    r = MusicResult() #Create instance of Music Result
    fb = MusicFeedback() #Create instance of Music Feedback

    for i, f in enumerate(goal.freqs):
    # for a, b in enumerate(list):
    # a: index of element in list
    # b: value of element in list
    # enumerate(list): while an element can be pull
        fb.remaining_steps = len(goal.freqs) -1
        #len(): obtain the length of list
        music.publish_feedback(fb)

        if music.is_preempt_requested():# if the action is preempted
            write_freq(0) #stop the music by frequency=0[hz]
            r.finished = False # Result = false
            music.set_preempted(r) #return the result
            return 

        write_freq(f)
        rospy.sleep(1.0 if i >= len(goal.durations) else goal.durations[i])
        #1.0[s] sleep when duration is not specified 

    r.finished = True
    music.set_succeeded(r)

if __name__ == '__main__':
    rospy.init_node('buzzer')#initialization of node
    #for receiving the data from the other node
    rospy.Subscriber("buzzer", UInt16, recv_buzzer)
    #Subscriber("topic name", data type, callback function)
    #callback function: function activated when receiving the data

    music = actionlib.SimpleActionServer('music', MusicAction, exec_music, False)
    #Generation of Action instance
    #exec_music(): callback function
    music.start()
    
    rospy.spin()#keep the node active(just for waiting)
    
