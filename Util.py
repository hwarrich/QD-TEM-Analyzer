import cv2 as cv

"""
Util provides some helpful classes and functions to use
"""

#This class helps keep track of the list of contours found and helps update the outline of the QDs that are selected
class ContourList:
    def __init__(self, points, img):
        self.points = points
        self.img = img
        self.copy = img.copy()

    #A function to handle clicks on individual QDs
    #This will unhighlight a QD that is clicked
    def click_event(self, event, x, y, flags, param):
        if(event == cv.EVENT_LBUTTONDOWN):
            self.removeContour(self.points, x, y)
            cv.drawContours(self.img, self.points, -1, 255, 2)
            cv.imshow("Output", self.img)
            self.img = self.copy.copy()

    #helper function to remove contour from list
    def removeContour(self, contours, x, y):
        contours = list(contours)
        for i in range(len(contours)):
            c = contours[i]
            xRec, yRec, wRec, hRec = cv.boundingRect(c)
            if (y >= yRec and y <= yRec + hRec and x >= xRec and x <= xRec + wRec):
                contours.pop(i)
                break
        contours = tuple(contours)
        self.points = contours

#A class to help keep track of QDs that have been clicked
class Points:
    def __init__(self):
        self.points = []

    def click_event(self, event, x, y, flags, param):
        if(event == cv.EVENT_LBUTTONDOWN):
            self.points.append((x, y))

#Maps wavelengths to contours
class Map:
    def __init__(self):
        self.dict = dict()
    def accumulate(self, contours, wavelength):
        if(wavelength in self.dict.keys()):
            self.dict[wavelength] = self.dict[wavelength] + contours
        else:
            self.dict[wavelength] = contours

