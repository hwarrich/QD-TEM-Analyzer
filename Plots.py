import matplotlib.pyplot as plt
import numpy as np
from decimal import Decimal
import random
import os

"""
This class makes some plots to present the computed information. It can be easily modified to get different graphs/plots.
"""

#Make a single histogram for one image
def makeSingleTEMHistogram(diameters, wavelength, name, minDiameter, maxDiameter):
    plt.clf()
    plt.figure(figsize=(14,7))
    plt.style.use('classic')
    binwidth = 0.2
    color = (random.random(), random.random(), random.random())
    plt.hist(diameters, bins = np.arange(minDiameter - binwidth, maxDiameter + binwidth, binwidth), color = color, lw = 1, density = True)
    plt.title("Size Distribution of " + str(name) + " Quantum Dots")
    plt.xlabel('Size (nm)')
    plt.ylabel('Count')
    plt.annotate(str(wavelength) + " nm", xy=(0.89, 0.95), xycoords='axes fraction', color = 'black')
    standardDevation = np.std(diameters)
    standardDevation = Decimal(str(standardDevation)).quantize(Decimal("1.0"))
    average = np.average(diameters)
    average = Decimal(str(average)).quantize(Decimal("1.0"))

    plt.annotate(str(average) + " ± " + str(standardDevation) + " nm", xy=(0.89, 0.90), xycoords='axes fraction', color='black')
    plt.tick_params(top=False, right=False)
    plt.minorticks_off()

    pathToHere = os.path.abspath(__file__)
    pathToFolder = os.path.join(os.path.dirname(pathToHere))
    pathToOutput = os.path.join(pathToFolder,'output', wavelength, (str(name) + " histogram.jpg"))
    plt.savefig(pathToOutput)

#make a plot using summary stats
def makeScatter(wavelengths, averages, stds, aggregateDiameters):
    plt.clf()
    box = plt.boxplot(aggregateDiameters, notch='True',patch_artist=True, labels= wavelengths)
    colors = ['green', 'red']
    for patch, color in zip(box['boxes'], colors):
        patch.set_facecolor(color)
    plt.title("Summary Statistics")
    plt.xlabel("Peak Emission Wavelength (nm)")
    plt.ylabel("Diameter (nm)")
    plt.tick_params(top=False, right=False)
    plt.minorticks_off()
    pathToHere = os.path.abspath(__file__)
    pathToFolder = os.path.join(os.path.dirname(pathToHere))
    pathToOutput = os.path.join(pathToFolder, 'output', "Summary Stats.jpg")
    plt.savefig(pathToOutput)

