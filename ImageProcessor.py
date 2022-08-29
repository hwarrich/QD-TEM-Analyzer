import cv2
import cv2 as cv
import math
from Main import *
from Stats import *

"""
This function contains the main image processing logic. It will find the scale bar and all of the quantum dots in an image.
"""

#is this a image?
def isImage(file):
    return (file.endswith(".png") or file.endswith(".jpg") or file.endswith(".jpeg"))

#given an image, remove scale bar and return its location
def removeScaleBar(img):
    #assume scale bar is black
    _, thresh = cv.threshold(img, 10, 255, cv.THRESH_BINARY)
    contours, _ = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    #remove the largest contour from the list
    if(len(contours) > 1):
        contours = contours[1:]
    index = 0
    count = 0
    for contour in contours:
        xRec, yRec, wRec, hRec = cv.boundingRect(contour)
        dimensions = img.shape
        height, width = dimensions
        if(wRec < width/7.0 or wRec > width/3.0):
            pass
            #print(str(width/7.0) + " " + str(width/3.0))
        elif(hRec > height/5):
            pass
        elif(cv.contourArea(contour) > 5000):
            pass
        elif(cv.contourArea(contour) < 80):
            pass
        elif(hRec * 2 > wRec):
            pass
        else:
            if(cv.contourArea(contour) > cv.contourArea(contours[index])):
                index = count
        count = count + 1

    c = contours[index]
    cv.drawContours(img, [c], -1, 255, thickness=cv2.FILLED)
    xRec, yRec, wRec, hRec = cv.boundingRect(c)
    return img, xRec, yRec, wRec, hRec

#use adaptive thresholding to make a binary image
def preProcess(img):
    bilateral = cv2.bilateralFilter(img, 20, 40, 30)
    binaryImg = cv.adaptiveThreshold(bilateral, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 37, 0)

    kernel = np.ones((5, 5), np.uint8)
    closing = cv.morphologyEx(binaryImg, cv.MORPH_CLOSE, kernel)

    opening = cv.morphologyEx(closing, cv.MORPH_OPEN, kernel)
    return opening

#Given an image, get the QD contours and compute some stats
def processImage(img, wavelength, map, imageName):
    output = img.copy()
    copy = img.copy()

    img, xRec, yRec, wRec, hRec = removeScaleBar(img)

    # blur and smooth image
    preprocessedImg = preProcess(img)

    mask = removeBorderContours(preprocessedImg, xRec, yRec, wRec, hRec)

    output, contours = drawOutput(mask, output)
    myContourList = ContourList(contours, copy)
    cv.setMouseCallback('Output', myContourList.click_event)
    cv.waitKey(0)

    diameters = calculateDiameter(myContourList.points, wRec)
    maxDiameter = math.ceil((max(diameters)))
    minDiamter = math.floor((min(diameters)))
    makeSingleTEMHistogram(diameters, wavelength, imageName, minDiamter, maxDiameter)
    map.accumulate(diameters, wavelength)

#removes all quantum dots that are touching the border of the image
def removeBorderContours(cimg, xRec, yRec, wRec, hRec):
    contours, _ = cv.findContours(cimg, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)

    height, width = cimg.shape
    mask = np.zeros(cimg.shape[:2], dtype=cimg.dtype) + 255

    for c in contours:
        touchingEdge = False
        if(cv.contourArea(c) < 600):
            touchingEdge = True
        for point in c:
            x, y = point[0]
            if (x <= 3):
                touchingEdge = True
            if (x >= width - 3):
                touchingEdge = True
            if (y <= 3):
                touchingEdge = True
            if (y >= height - 3):
                touchingEdge = True
            if (y >= yRec and y <= yRec + hRec and x >= xRec  and x <= xRec + wRec):
                touchingEdge = True
        if (not touchingEdge):
            cv.drawContours(mask, [c], 0, (0), -1)
        touchingEdge = False
    return mask

def drawOutput(mask, output):
    contours, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    contours = contours[1:]
    cv.drawContours(output, contours, -1, 255, 2)
    cv.imshow('Output', output)
    return output, contours