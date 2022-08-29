from ImageProcessor import *
from Util import *

"""
The main logic of the program. Given that all folders in 'images' contain QDs with similar peak emission wavelengths,
this program will go through each folder and process all of the images in each folder. Then, it will repeat this process
for all folders/wavelengths before computing some statistics and saving the plots in an output folder.
"""

def main():
    images_path = os.getcwd()+ os.sep + 'images'
    suffix = [".jpg", '.jpeg', '.png']

    #make a new map to map wavelength to the correct images
    map = Map()

    #loop through all of the images
    for i in os.listdir(images_path):
        folder = os.path.basename(i)
        file = images_path + os.sep + folder
        for image in os.listdir(file):
            fileName, fileExtension = os.path.splitext(image)
            # is it an image file with 'suffix' extension ?
            if os.path.isfile(file + os.sep + image) and fileExtension in suffix:
                #read and process image, save result into map
                img = cv2.imread(image, 0)
                processImage(img, folder, map, fileName)
    #compute summary stats
    computeStats(map.dict)
    cv.destroyAllWindows()


if __name__ == "__main__":
    main()

