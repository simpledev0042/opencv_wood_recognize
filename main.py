from Library import image, file
import sys
import os
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from Library import file
import json
import math

sys.path.append(os.getcwd() + "\\Library")

class BlackLine:
    def __init__(self, st, en):
        self.st = st
        self.en = en
        self.deep = en - st
        self.center = (en + st) / 2


class Rule:
    def __init__(self, st, height, step, size):
        self.st = st
        self.step = step
        self.size = size


class MainRect:
    def __init__(self, image, lines):
        self.image = image
        self.lines = lines


def isSame(a, b):
    if (a == 0 or b == 0):
        return False
    if (a < b):
        return (a / b > 0.8)
    else:
        return (a / b) < (1/0.8)


def isSame2(a, b):
    if (a == 0 or b == 0):
        return False
    if (a < b):
        return isSame(a, b/2)
    else:
        return isSame(a/2, b)


def hasRule(lines, height):
    sm = 0
    for line in lines:
        sm = sm + line.deep
    if (isSame(height * 0.9, sm)):
        return -1
    avgStep = 0
    steps = []
    realSteps = []
    cntRealSteps = []
    beforeCenter = -1
    for line in lines:
        if (beforeCenter != -1):
            steps.append(line.center - beforeCenter)
        beforeCenter = line.center

    nStep = len(steps)
    if (nStep):
        realSteps.append(steps[0])
        cntRealSteps.append(0)
        for i in range(1, nStep):
            nRealStep = len(realSteps)
            for j in range(0, nRealStep):
                if (isSame(steps[i], realSteps[j])):
                    realSteps[j] = ((steps[i] + realSteps[j]) / 2)
                    cntRealSteps[j] = cntRealSteps[j] + 1
                elif (isSame2(steps[i], realSteps[j])):
                    realSteps[j] = (steps[i] + realSteps[j]) / 3
                    cntRealSteps[j] = cntRealSteps[j] + 2
                else:
                    realSteps.append(steps[i])
                    cntRealSteps.append(1)
        nRealStep = len(realSteps)
        for i in range(0, nRealStep):
            if (cntRealSteps[i] > 3 and realSteps[i] * (cntRealSteps[i]+2) > height * 0.8):
                return realSteps[i]
    return -1

def makeLine( arr ) :
    avg = 0
    for item in arr:
        avg = avg + item
    nItem = len( arr )
    avg = int( avg / nItem )
    status = True
    for i in range(0, nItem) :
        if arr[i] > avg * 1.5:
            arr[i] = int((avg + arr[i] / 2) / 2)
            status = False
    return [arr, status]

def checkMin( arr ) :
    avg = 0
    for item in arr:
        avg = avg + item
    avg = (avg / len( arr ))
    nItem = len( arr )
    for i in range( 0, nItem ) :
        if( arr[i] < avg / 6 ) :
            arr[i] = avg
    return arr

def getApproximateLine( arr, addVal ) :
    x = np.array( arr )
    if addVal < 0 :
        x = abs( addVal ) - x
    else :
        x = x + addVal
    avg = int(np.average( x ))
    avgTop = np.average(x[0:int(len(arr)/2)])
    avgBottom = np.average(x[int(len(arr)/2):len(arr)])
    res = []
    if( (avg < avgTop and avg > avgBottom) or (avg > avgTop and avg < avgBottom) ) :
        distTop = avgTop - avg
        distBotton = avgBottom - avg
        avgT = int((math.fabs( distTop ) + math.fabs( distBotton )))
        distTop = int( distTop / math.fabs(distTop - 1E-9)) * avgT
        distBotton = int( distBotton / math.fabs(distBotton - 1E-9)) * avgT
        avgTop = distTop + avg
        avgBottom = distBotton + avg
        res.append((int(avgTop), 0))
        res.append((int(avgBottom), len(arr)))
    else :
        res.append((int(avg), 0))
        res.append((int(avg), len(arr)))
    return res

def getLugRect( image ) :
    # image = cv.GaussianBlur(image, (5, 5), 0)
    src = image.copy()
    image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    kernel = np.ones((20, 20), np.uint8)
    h = image.shape[0]
    w = image.shape[1]
    left = w
    right = 0
    image = cv.morphologyEx(image, cv.MORPH_CLOSE, kernel)
    avg = 0
    for y in range(0, h, int(h / 20)):
        sm = 0
        for x in range(0, w, int(w / 20)):
            avg = avg + image[y, x]
    avg = int( avg / 400 );
    ret2, image = cv.threshold(image, avg * 0.83, 255, cv.THRESH_TOZERO_INV)
    ret2, image = cv.threshold(image, avg * 0.3, 255, cv.THRESH_TOZERO)
    image = cv.morphologyEx(image, cv.MORPH_CLOSE, kernel)
    leftEnds = []
    rightEnds = []
    leftEnd = 0
    rightEnd = w
    for x in range(0, w):
        sm = 0
        for y in range(0, h):
            pix = image[y, x]
            if( pix < 5 ) :
                sm = sm + 1
        if( sm > h * 0.9 ) :
            leftEnd = x
        else :
            break
        
    for x in range( 0, w) :
        sm = 0
        for y in range(0, h) :
            if image[y, w-x-1] < 5 :
                sm = sm + 1
        if( sm > h * 0.9 ) :
            rightEnd = w - x - 1
        else :
            break
            
    for y in range( 0, h) :
        l = 0
        for x in range( 0, w ) :
            if image[y, x] < 5 :
                l = x
            else :
                break
        if( l < leftEnd ) :
            l = leftEnd
        leftEnds.append( l - leftEnd )
    
    for y in range(0, h) :
        r = w - 1
        for x in range( 0, w) :
            if image[y, w-x-1] < 5 :
                r = w-x-1
            else :
                break
        if( r > rightEnd ) :
            r = rightEnd
        rightEnds.append( rightEnd - r )
    cnt = 1
    while cnt :
        [res, status] = makeLine( leftEnds );
        leftEnds = res
        cnt = cnt + 1
        if( res == True or cnt > 20 ):
            break
    cnt = 1
    while 1 :
        [res, status] = makeLine( rightEnds )
        rightEnds = res
        cnt = cnt + 1
        if res == True or cnt > 20:
            break
# ret = cv.circle(ret, (x, int(line.center)),
#                                     radius=0, color=(0, 0, 255), thickness=2)
    checkMin( leftEnds )
    checkMin( rightEnds)
    lft = getApproximateLine(leftEnds, leftEnd)
    rlt = getApproximateLine(rightEnds, -rightEnd)
    src = cv.line(src, lft[0], lft[1], (0,0,255), 3)
    src = cv.line(src, lft[0], (0, 0), (0,0,255), 3)
    src = cv.line(src, lft[1], (0, h), (0,0,255), 3)
    src = cv.line(src, (0, 0), (0, h), (0,0,255), 3)
    
    src = cv.line(src, rlt[0], rlt[1], (0,0,255), 3)
    src = cv.line(src, rlt[0], (w, 0), (0,0,255), 3)
    src = cv.line(src, rlt[1], (w, h), (0,0,255), 3)
    src = cv.line(src, (w, 0), (w, h), (0,0,255), 3)
    # for i in range(0, h) :
    #     src = cv.circle( src, (int(leftEnd + leftEnds[i]), i), radius = 0, color = (0,0,255), thickness = 2)
    #     src = cv.circle( src, (int(rightEnd - rightEnds[i]), i), radius = 0, color = (255,0,0), thickness = 2)
        
        # src = cv.circle( src, (int(leftEnd), i), radius = 0, color = (0,255,255), thickness = 1)
        # src = cv.circle( src, (int(rightEnd), i), radius = 0, color = (0,255,255), thickness = 1)
    return src

def main():
    fileList = file.getFileList("./images")
    for imageFile in fileList:
        img = cv.imread(imageFile)
        fileName = os.path.basename(imageFile).split(".")[0]
        fileDir = os.path.dirname(imageFile)
        res = getLugRect(img)
        # cv.imshow("Img", res)
        cv.imwrite(fileDir+"\\new\\"+fileName+"_new.png", res)
        # cv.waitKey(0)
        print( imageFile )


if __name__ == '__main__':
    main()
