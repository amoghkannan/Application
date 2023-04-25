#!/usr/bin/env python

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

def show_img():
  pub=rospy.Publisher('feed',Image,queue_size=10)
  rospy.init_node('image_feed',anonymous=True)
  rate=rospy.Rate(100)
  cap=cv2.VideoCapture(0)
  bridge=CvBridge()
  while not rospy.is_shutdown():
        ret,frame=cap.read()
        grayed=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        grayed = cv2.blur(grayed, (2,2))
        ret,thresh=cv2.threshold(grayed,127,255,0)
        unknown, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        for i in range(0,len(contours)):
          epsilon=0.01*cv2.arcLength(contours[i],True)
          approx=cv2.approxPolyDP(contours[i],epsilon,True)
          n_vertices=len(approx)
          M=cv2.moments(contours[i])
          if(M['m00']<0.001):
             continue
          cx=int(M['m10']/M['m00'])
          cy=int(M['m01']/M['m00'])
          if(n_vertices==3):
              cv2.putText(frame,'Triangle',(cx,cy),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),1,cv2.LINE_AA)
          if(n_vertices==4):
              cv2.putText(frame,'Rectangle',(cx,cy),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),1,cv2.LINE_AA)
          if(n_vertices==5):
              cv2.putText(frame,'Pentagon',(cx,cy),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),1,cv2.LINE_AA)
          if(n_vertices==6):
              cv2.putText(frame,'Hexagon',(cx,cy),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),1,cv2.LINE_AA)
          if(n_vertices>6):
              cv2.putText(frame,'ngon/circle',(cx,cy),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),1,cv2.LINE_AA)
        rospy.loginfo('Number of vertices is %s',n_vertices)
        cv2.imshow('Image feed',frame)
        cv2.waitKey(0)     
        pub.publish(bridge.cv2_to_imgmsg(frame))
             
        rate.sleep()
        cv2.destroyAllWindows()

if __name__ == '__main__':
  try:
    show_img()
  except rospy.ROSInterruptException:
    pass
