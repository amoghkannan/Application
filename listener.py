#!/usr/bin/env python

import rospy
from std_msgs.msg import String

n=0
t0=0
def callback(data):
   if(n==0):
     global t0
     t0=data.data
     global n
     n=1    
   rospy.loginfo("It has been %f  seconds since we started this pointless conversation.",float(data.data)-float(t0))
   rospy.loginfo("Shut up already")

def listener():
  rospy.Subscriber('chatter',String,callback)
  rospy.init_node('listener',anonymous=True)
  rospy.spin()

if __name__ == '__main__':

      listener() 
