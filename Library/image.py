# import sys
# import os
# # sys.path.append(os.getcwd() + "\\Library")    
# # print(os.getcwd())
# import cv2 as cv
# import numpy as np
# from matplotlib import pyplot as plt
# from Library import file 
# import argparse
# # import imutils

# def processImage(filePath):
#     img = cv.imread(filePath,0)
#     kernel = np.ones((5,5),np.uint8)
#     # erosion = cv.erode(img,kernel,iterations = 1)
#     opening = cv.morphologyEx(img, cv.MORPH_OPEN, kernel)
#     closing = cv.morphologyEx(opening, cv.MORPH_CLOSE, kernel)
#     ret, thresh = cv.threshold(closing, 20, 255, 0)
#     kernel = np.ones((10,10),np.uint8)
#     opening = cv.morphologyEx(thresh, cv.MORPH_CLOSE, kernel)
#     return opening;

# def processImage2( filePath ):
#     image = cv.imread(imagePath)
#     image = imutils.resize(image, width=450)
#     gray = cv.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     blurred = cv.GaussianBlur(gray, (5, 5), 0)
#     edged = cv.Canny(blurred, 30, 150)
#     return edged

# def processImage3(filePath):
#     img = cv.imread(filePath,0)
#     kernel = np.ones((5,5),np.uint8)
#     # erosion = cv.erode(img,kernel,iterations = 1)
#     opening = cv.morphologyEx(img, cv.MORPH_OPEN, kernel)
#     closing = cv.morphologyEx(opening, cv.MORPH_CLOSE, kernel)
#     # ret, thresh = cv.threshold(closing, 40, 255, 0)
#     thresh = cv.adaptiveThreshold(img,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY,11,2)
#     kernel = np.ones((10,10),np.uint8)
#     opening = cv.morphologyEx(thresh, cv.MORPH_CLOSE, kernel)
#     return opening;