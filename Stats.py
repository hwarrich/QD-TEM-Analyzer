import cv2
from ImageProcessor import *
from Plots import *

"""
A class to help calculate some basic stats
"""

def calculateDiameter(contours, scaleBarWidth):
    #can adjust scale (nm)
    scale = 20
    diameters = []
    for qd in contours:
        area = cv2.contourArea(qd)
        radiusSquared = area / math.pi
        diameter = math.sqrt(radiusSquared) * 2
        diameter = diameter / scaleBarWidth
        diameter = diameter * scale
        if(diameter < 15):
            diameters.append(diameter)
    return diameters

def computeStats(diameterByWavelen):
    wavelengths = []
    averages = []
    stds = []
    aggregateDiameters = []
    for wavelength in diameterByWavelen.keys():
        diameters = diameterByWavelen[wavelength]
        standardDevation = np.std(diameters)
        average = np.average(diameters)
        wavelengths.append(wavelength)
        averages.append(average)
        stds.append(standardDevation)
        aggregateDiameters.append(diameters)
    aggregateDiameters = np.array(aggregateDiameters, dtype= object).flatten()
    makeScatter(wavelengths, averages, stds, aggregateDiameters)
