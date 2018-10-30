#!/usr/bin/python3
import os
import sys
import matplotlib.pyplot as plt
import cv2
import numpy as np


#image = cv2.imread("/Users/sam/code/Hackathon/InnerOuter/0-0/12.250-CF716-U02822-35625-2017-11-17-NA_B1.JPG")
#image = cv2.imread("/Users/sam/code/Hackathon/InnerOuter/0-0/DSC01277.JPG")
if len(sys.argv) > 1:
    for filename in sys.argv[1:]:
        image = cv2.imread(filename,0)
        #gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Create mask
        height,width = image.shape
        mask = np.zeros((height,width), np.uint8)

        gray = cv2.GaussianBlur(image,(5,5),0)
        gray = cv2.medianBlur(gray,5)

        gimage = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,3.5)

        circles = cv2.HoughCircles(gray,cv2.HOUGH_GRADIENT,1,100,param1=45,param2=30,minRadius=0,maxRadius=100)

        circles = np.uint16(np.around(circles))

        for _,i in enumerate(circles[0,:]):
            mask = np.zeros((height,width), np.uint8)

            # draw the outer circle
            cv2.circle(image,(i[0],i[1]),i[2],(0,255,0),2)
            # draw the center of the circle
            cv2.circle(image,(i[0],i[1]),2,(0,0,255),3)
            
            #Code below this point deals with cropping out found circles and writing the cropped circle
            cv2.circle(mask,(i[0],i[1]),i[2],(255,255,255),thickness=-1)
        
            # Copy that image using that mask
            masked_data = cv2.bitwise_and(image, image, mask=mask)

            # Apply Threshold
            __,thresh = cv2.threshold(mask,1,255,cv2.THRESH_BINARY)

            # Find Contour
            contours = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
            x,y,w,h = cv2.boundingRect(contours[0])

            # Crop masked_data
            crop = masked_data[y:y+h,x:x+w]

            #Finaly write circle to file (Probably need to change path or except arguments here)
            cv2.imwrite("/Users/sam/code/Hackathon/InnerOuter/circles/circle-" + str(_) + ".jpg", crop)


        #Used to add text to image. Maybe useful method to note which circles are which
        #font = cv2.FONT_HERSHEY_SIMPLEX
        #cv2.putText(image,'OpenCV',(10,500), font, 4,(255,255,255),2,cv2.LINE_AA)

        cv2.imshow('detected circles',image)
        
        #Used to show cropped images 
        #cv2.imshow('Cropped Eye',crop)

        cv2.waitKey(0)
        cv2.destroyAllWindows()
