"""
Project: Create a mosaic of images from images of any size.
Author: Rubens de Castro Pereira
Advisor: Dibio Leandro Borges
Date: 18/03/2021
Version: 1.0.0
"""

# Importing needed libraries
import os
import math
import json
import cv2
from shutil import copyfile

# ###########################################
# Constants
# ###########################################
LINE_FEED = '\n'


# ###########################################
# Application Methods
# ###########################################


# ###########################################
# Methods of Level 1
# ###########################################


# # processing all images of the folder
def processInputImages(inputOriginalImagesPath, outputCroppedImagesMosaicPath, sizeSquareImage):
    # defining counters
    totalOfImages = 0

    # processing each image of the folder
    for fileName in os.listdir(inputOriginalImagesPath):

        # check if file is an image or not
        if fileName.lower().find('jpg') == -1 and fileName.lower().find('jpeg') == -1:
            continue

        # get jpeg position
        jpegPosition = -1
        jpegPosition = fileName.find('jpg')
        if jpegPosition == -1: jpegPosition = fileName.find('jpeg')
        if jpegPosition == -1: jpegPosition = fileName.find('JPG')
        if jpegPosition == -1: jpegPosition = fileName.find('JPEG')

        # get only image name
        inputImageName = fileName[:jpegPosition - 1]

        # adding image counter
        totalOfImages += 1

        # reading image
        print('')
        print('Reading image:', fileName)
        inputImage = cv2.imread(inputOriginalImagesPath + fileName)
        if inputImage is not None:
            # creating new file
            id = inputImageName[1:]
            imageHeight, imageWidth, imageChannel = inputImage.shape
            print(
                'Image: ' + inputImageName + "  shape: " + " height:" + str(imageHeight) + " width:" + str(
                    imageWidth))

        # segments the original image to define the ROI (Region Of Interest)

        # segments the image
        # segementByContours(inputImage, inputImageName, sizeSquareImage, outputCroppedImagesMosaicPath)

        # segments the image
        # segementByGaussianBlurAndCanny(inputImage, inputImageName, sizeSquareImage, outputCroppedImagesMosaicPath)

        # segments the image
        segementByWatershed(inputImage, inputImageName, sizeSquareImage, outputCroppedImagesMosaicPath)

    # printing statistics
    print('')
    print('Estatísticas do Processamento:')
    print('------------------------------')
    print('Total de imagens             : ', totalOfImages)

    print('Máximo Height                : ', sizeSquareImage)
    print('Máximo Width                 : ', sizeSquareImage)
    print('')


# ###########################################
# Methods of Level 2
# ###########################################


# segments the original image to define the ROI (Region Of Interest)
# https://www.geeksforgeeks.org/find-and-draw-contours-using-opencv-python/
def segementByContours(inputImage, inputImageName, sizeSquareImage, outputCroppedImagesMosaicPath):
    # get image shape
    # imageHeight, imageWidth, imageChannel = inputImage.shape

    # Grayscale
    gray = cv2.cvtColor(inputImage, cv2.COLOR_BGR2GRAY)

    # Find Canny edges
    edged = cv2.Canny(gray, 30, 200)
    cv2.waitKey(0)

    # Finding Contours
    # Use a copy of the image e.g. edged.copy()
    # since findContours alters the image
    contours, hierarchy = cv2.findContours(edged,
                                           cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # showing image
    imageWindowName = 'Canny'
    showImageInWindow(edged, imageWindowName, 800, 600, True)
    # cv2.waitKey(0)

    print("Number of Contours found = " + str(len(contours)))

    # Draw all contours
    # -1 signifies drawing all contours
    cv2.drawContours(inputImage, contours, -1, (0, 255, 0), 3)

    # showing image
    imageWindowName = 'Contours'
    showImageInWindow(inputImage, imageWindowName, 800, 600, True)
    cv2.waitKey(0)

    cv2.destroyAllWindows()


# segments the original image to define the ROI (Region Of Interest)
# https://towardsdatascience.com/extracting-regions-of-interest-from-images-dacfd05a41ba
def segementByGaussianBlurAndCanny(inputImage, inputImageName, sizeSquareImage, outputCroppedImagesMosaicPath):
    # Grayscale
    gray = cv2.cvtColor(inputImage, cv2.COLOR_BGR2GRAY)

    # Gaussian Blur
    gray = cv2.GaussianBlur(inputImage, (11, 11), 0)
    # showing image
    imageWindowName = 'GaussianBlur'
    showImageInWindow(gray, imageWindowName, 800, 600, True)
    # cv2.waitKey(0)

    # Find Canny edges
    edged = cv2.Canny(gray, 30, 200)
    # cv2.waitKey(0)

    # Finding Contours
    # Use a copy of the image e.g. edged.copy()
    # since findContours alters the image
    contours, hierarchy = cv2.findContours(edged,
                                           cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # showing image
    imageWindowName = 'Canny'
    showImageInWindow(edged, imageWindowName, 800, 600, True)
    # cv2.waitKey(0)

    print("Number of Contours found = " + str(len(contours)))

    # Draw all contours
    # -1 signifies drawing all contours
    cv2.drawContours(inputImage, contours, -1, (0, 255, 0), 3)

    # showing image
    imageWindowName = 'Canny'
    showImageInWindow(inputImage, imageWindowName, 800, 600, True)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# https://docs.opencv.org/master/d3/db4/tutorial_py_watershed.html
def segementByWatershed(inputImage, inputImageName, sizeSquareImage, outputCroppedImagesMosaicPath):
    # Grayscale
    gray = cv2.cvtColor(inputImage, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # showing image
    imageWindowName = 'gray'
    showImageInWindow(gray, imageWindowName, 800, 600, True)
    imageWindowName = 'ret'
    showImageInWindow(ret, imageWindowName, 800, 600, True)
    imageWindowName = 'threshold'
    showImageInWindow(thresh, imageWindowName, 800, 600, True)
    cv2.waitKey(0)

    # Gaussian Blur
    gray = cv2.GaussianBlur(inputImage, (11, 11), 0)
    # showing image
    imageWindowName = 'GaussianBlur'
    showImageInWindow(gray, imageWindowName, 800, 600, True)
    # cv2.waitKey(0)

    # Find Canny edges
    edged = cv2.Canny(gray, 30, 200)
    # cv2.waitKey(0)

    # Finding Contours
    # Use a copy of the image e.g. edged.copy()
    # since findContours alters the image
    contours, hierarchy = cv2.findContours(edged,
                                           cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # showing image
    imageWindowName = 'Canny'
    showImageInWindow(edged, imageWindowName, 800, 600, True)
    # cv2.waitKey(0)

    print("Number of Contours found = " + str(len(contours)))

    # Draw all contours
    # -1 signifies drawing all contours
    cv2.drawContours(inputImage, contours, -1, (0, 255, 0), 3)

    # showing image
    imageWindowName = 'Canny'
    showImageInWindow(inputImage, imageWindowName, 800, 600, True)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# ###########################################
# Methods of Level 3
# ###########################################


def showImageInWindow(image, imageWindowName, width, height, showImage):
    if not showImage:
        return

    # Showing Image
    # Giving name to the window with Image
    # And specifying that window is resizable
    cv2.namedWindow(imageWindowName, cv2.WINDOW_NORMAL)
    cv2.imshow(imageWindowName, image)
    cv2.resizeWindow(imageWindowName, width, height)


# ###########################################
# Methods of Level 4
# ###########################################


# define the cropped name
def getCroppedImageName(inputImageName, mosaicLin, mosaicCol, sufixName):
    # setting the name of cropped mosaic image
    mosaicLinName = '{:03d}'.format(mosaicLin)
    mosaicColName = '{:03d}'.format(mosaicCol)
    croppedImageName = inputImageName + '-r' + mosaicLinName + '-c' + mosaicColName + sufixName
    return croppedImageName


# save the cropped image
def saveCroppedImage(croppedImagePathAndImageName, croppedImage):
    # croppedImageName = croppedImagePathAndImageName
    cv2.imwrite(croppedImagePathAndImageName + '.jpg', croppedImage)
    print(croppedImagePathAndImageName)


# save the details of cropped image
def saveCroppedImageDetailsFile(outputCroppedImagesMosaicPath, originalImageName, originalImageHeight,
                                originalImageWidth,
                                sizeSquareImage, mosaicLin, mosaicCol, linP1, colP1, linP2, colP2,
                                sufixName
                                ):
    # setting annotation file
    croppedImageName = getCroppedImageName(originalImageName, mosaicLin, mosaicCol, sufixName)
    croppedImagePathAndImageName = outputCroppedImagesMosaicPath + croppedImageName + '-details.txt'

    # setting the details in JSON format
    croppedImageDetails = {
        'croppedImagePath': str(outputCroppedImagesMosaicPath),
        'originalImageName': str(originalImageName),
        'originalImageHeight': str(originalImageHeight),
        'originalImageWidth': str(originalImageWidth),
        'croppedImageName': str(croppedImageName),
        'sizeSquareImage': str(sizeSquareImage),
        'mosaicLin': str(mosaicLin),
        'mosaicCol': str(mosaicCol),
        'linP1': str(linP1),
        'colP1': str(colP1),
        'linP2': str(linP2),
        'colP2': str(colP2)
    }

    # writing details file
    with open(croppedImagePathAndImageName, 'w') as json_file:
        json.dump(croppedImageDetails, json_file)


# ###########################################
# Main method
# ###########################################
if __name__ == '__main__':
    INPUT_ORIGINAL_IMAGES_PATH = \
        'E:/desenvolvimento/projetos/DoctoralProjects/ImageMosaicProjectImages/01. input original images/'
    OUTPUT_CROPPED_IMAGES_MOSAIC_PATH = \
        'E:/desenvolvimento/projetos/DoctoralProjects/ImageMosaicProjectImages/02. output cropped images mosaic/'

    print('Creates Images Mosaic')
    print('---------------------------------')
    print('')
    print('Input images path    : ', INPUT_ORIGINAL_IMAGES_PATH)
    print('Mosaic images path  : ', OUTPUT_CROPPED_IMAGES_MOSAIC_PATH)
    print('')

    # setting the size square image to crop with a fixed size (height and width) used in the YOLOv4
    sizeSquareImage = 128

    # processing the annotated images
    processInputImages(INPUT_ORIGINAL_IMAGES_PATH, OUTPUT_CROPPED_IMAGES_MOSAIC_PATH, sizeSquareImage)

    # end of processing
    print('End of processing')
