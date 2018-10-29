#!/usr/bin/python3
import os
import matplotlib.pyplot as plt
import cv2
import numpy as np


#image = cv2.imread("/Users/sam/code/Hackathon/InnerOuter/0-0/12.250-CF716-U02822-35625-2017-11-17-NA_B1.JPG")
#image = cv2.imread("/Users/sam/code/Hackathon/InnerOuter/0-0/DSC01277.JPG")
image = cv2.imread("/Users/sam/code/Hackathon/InnerOuter/7-6/Picture78.JPG")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#gray = cv2.resize(gray, (1000, 1000))

gray = cv2.GaussianBlur(gray,(5,5),0)
gray = cv2.medianBlur(gray,5)

gimage = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,3.5)

circles = cv2.HoughCircles(gimage,cv2.HOUGH_GRADIENT,1,100,param1=45,param2=30,minRadius=0,maxRadius=100)

circles = np.uint16(np.around(circles))
for i in circles[0,:]:
    # draw the outer circle
    cv2.circle(image,(i[0],i[1]),i[2],(0,255,0),2)
    # draw the center of the circle
    cv2.circle(image,(i[0],i[1]),2,(0,0,255),3)

cv2.imshow('detected circles',image)
cv2.waitKey(0)
cv2.destroyAllWindows()
