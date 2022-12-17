import numpy as np
import cv2 as cv
import os
import sys

mylist = []
capFront = cv.VideoCapture(0)

def print_coord(event,x,y,flags,param):
    if event == cv.EVENT_LBUTTONDOWN:
        mylist.append([x,y])
ret, img = capFront.read()
imgheight, imgwidth = img.shape[:2]
resizedImg = cv.resize(img,(int(imgwidth), int(imgheight)), interpolation = cv.INTER_AREA)
cv.namedWindow('Get Coordinates')
cv.setMouseCallback('Get Coordinates',print_coord)
cv.imshow('Get Coordinates',resizedImg)
cv.waitKey(0)
cv.destroyAllWindows()
print(mylist)
mat = np.array(mylist)
