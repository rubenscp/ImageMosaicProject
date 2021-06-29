"""
Project: Create a mosaic of images from images of any size.
Author: Rubens de Castro Pereira
Advisor: Dibio Leandro Borges
Date: 18/02/2021
Version: 1.0.0
"""

# Importing needed libraries
import os
import math
import json
import cv2
from shutil import copyfile
# import pandas as pd
from pandas import read_excel
import numpy as np

import skimage
from skimage.util import img_as_float
from skimage.segmentation import slic
from skimage.util import img_as_ubyte, img_as_int
from skimage import img_as_float

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
def processInputImages(experimentRootPath,
                       inputOriginalImagesPath,
                       inputSegmentedOriginalImagesPath,
                       inputRegionOfInterestPath,
                       outputCroppedImagesMosaicPath,
                       sizeSquareImage):
    # defining counters
    totalOfImages = 0

    # getting roi of images by Excel files in the version 2003 (xls)
    imageMosaicPathAndROIFile = inputRegionOfInterestPath + 'ROI (Region Of Interest) of mosaic.xls'
    roi = getROI(imageMosaicPathAndROIFile)

    # xxx1 = isROI(roi, 1, 1)

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
        # segmentedInputImage = segmentByMorphological(inputImage, inputImageName, outputCroppedImagesMosaicPath)
        # segmentedInputImage = segmentByDibio(inputOriginalImagesPath)

        segmentedInputImage = []
        # segmentedInputImage = segmentBySuperPixel(inputImage, inputImageName, outputCroppedImagesMosaicPath)

        # create the mosaic of images
        cropImagesMosaic(inputImage, inputImageName, sizeSquareImage, outputCroppedImagesMosaicPath, roi,
                         segmentedInputImage)

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

# get ROI (Region Of Interest)
def getROI(imageMosaicPathAndROIFile):
    # defining roi
    roi = None

    # read excel file in the version 2003
    roi = read_excel(imageMosaicPathAndROIFile, sheet_name='roi', header=None, index_col=None).to_numpy()

    # returning ROI
    return roi


# crops the bounding box image
def cropImagesMosaic(inputImage, inputImageName, sizeSquareImage, outputCroppedImagesMosaicPath,
                     roi,
                     segmentedInputImage):
    # get image shape
    imageHeight, imageWidth, imageChannel = inputImage.shape

    # defining the folder path to put the images mosaic
    MOSAIC_PATH = 'mosaic\\'

    # calculating number of mosaic
    numberOfMosaicLines = math.ceil(imageHeight / sizeSquareImage)
    numberOfMosaicColuns = math.ceil(imageWidth / sizeSquareImage)

    # cropping images in the horizontal and vertical bands
    mosaicImage = inputImage.copy()
    for mosaicLin in range(1, numberOfMosaicLines + 1):
        for mosaicCol in range(1, numberOfMosaicColuns + 1):
            # setting indicator of image cropping
            croppingImageOfROI = False
            croppingImageOfSegmentedImage = False

            # defining the two points of the cropped image
            linP1, colP1, linP2, colP2 = getP1AndP2OfHorizontalVerticalCrop(mosaicLin, mosaicCol,
                                                                            sizeSquareImage,
                                                                            imageWidth,
                                                                            imageHeight)

            # selecting mosaic according by ROI
            if isROI(roi, mosaicLin, mosaicCol):
                croppingImageOfROI = True
                # percentageBackgroundDesired = 0
                # if isLeaf(segmentedInputImage, linP1, colP1, linP2, colP2, percentageBackgroundDesired):
                #     croppingImageOfROI = True
            else:
                percentageBackgroundDesired = 0
                if isLeaf(segmentedInputImage, linP1, colP1, linP2, colP2, percentageBackgroundDesired):
                    croppingImageOfSegmentedImage = True

            # selecting mosaic according by ROI
            if croppingImageOfROI or croppingImageOfSegmentedImage:
                # cropping mosaic image
                cropHorizontalVerticalImage(inputImage, inputImageName, outputCroppedImagesMosaicPath, sizeSquareImage,
                                            mosaicLin, mosaicCol, mosaicImage,
                                            croppingImageOfROI, croppingImageOfSegmentedImage)

    # saving the mosaic image
    mosaicImageName = outputCroppedImagesMosaicPath + MOSAIC_PATH + inputImageName + '-mosaic-hv'
    saveImage(mosaicImageName, mosaicImage)

    # cropping images in the right sliding
    mosaicImage = inputImage.copy()
    for mosaicLin in range(1, numberOfMosaicLines - 1):
        for mosaicCol in range(1, numberOfMosaicColuns - 1):

            # setting indicator of image cropping
            croppingImageOfROI = False
            croppingImageOfSegmentedImage = False

            # defining the two points of the cropped image
            linP1, colP1, linP2, colP2 = getP1AndP2OfRightSlidingCrop(mosaicLin, mosaicCol,
                                                                      sizeSquareImage,
                                                                      imageWidth,
                                                                      imageHeight)

            # selecting mosaic according by ROI
            if isROI(roi, mosaicLin, mosaicCol):
                croppingImageOfROI = True
                # percentageBackgroundDesired = 0
                # if isLeaf(segmentedInputImage, linP1, colP1, linP2, colP2, percentageBackgroundDesired):
                #     croppingImageOfROI = True
            else:
                percentageBackgroundDesired = 10
                if isLeaf(segmentedInputImage, linP1, colP1, linP2, colP2, percentageBackgroundDesired):
                    croppingImageOfSegmentedImage = True

            # selecting mosaic according by ROI
            if croppingImageOfROI or croppingImageOfSegmentedImage:
                # cropping mosaic image
                cropRightSlidingImage(inputImage, inputImageName, outputCroppedImagesMosaicPath, sizeSquareImage,
                                      mosaicLin, mosaicCol, mosaicImage,
                                      croppingImageOfROI, croppingImageOfSegmentedImage)

    # saving the mosaic image
    mosaicImageName = outputCroppedImagesMosaicPath + MOSAIC_PATH + inputImageName + '-mosaic-rightSliding'
    saveImage(mosaicImageName, mosaicImage)

    # cropping images in the down sliding
    mosaicImage = inputImage.copy()
    for mosaicLin in range(1, numberOfMosaicLines - 1):
        for mosaicCol in range(1, numberOfMosaicColuns - 1):
            # setting indicator of image cropping
            croppingImageOfROI = False
            croppingImageOfSegmentedImage = False

            # defining the two points of the cropped image
            linP1, colP1, linP2, colP2 = getP1AndP2OfDownSlidingCrop(mosaicLin, mosaicCol,
                                                                     sizeSquareImage,
                                                                     imageWidth,
                                                                     imageHeight)

            # selecting mosaic according by ROI
            if isROI(roi, mosaicLin, mosaicCol):
                croppingImageOfROI = True
                # percentageBackgroundDesired = 0
                # if isLeaf(segmentedInputImage, linP1, colP1, linP2, colP2, percentageBackgroundDesired):
                #     croppingImageOfROI = True
            else:
                percentageBackgroundDesired = 10
                if isLeaf(segmentedInputImage, linP1, colP1, linP2, colP2, percentageBackgroundDesired):
                    croppingImageOfSegmentedImage = True

            # selecting mosaic according by ROI
            if croppingImageOfROI or croppingImageOfSegmentedImage:
                # cropping mosaic image
                cropDownSlidingImage(inputImage, inputImageName, outputCroppedImagesMosaicPath, sizeSquareImage,
                                     mosaicLin, mosaicCol, mosaicImage,
                                     croppingImageOfROI, croppingImageOfSegmentedImage)

    # saving the mosaic image
    mosaicImageName = outputCroppedImagesMosaicPath + MOSAIC_PATH + inputImageName + '-mosaic-downSliding'
    saveImage(mosaicImageName, mosaicImage)

    # cropping images in the right and down sliding
    mosaicImage = inputImage.copy()
    for mosaicLin in range(1, numberOfMosaicLines - 1):
        for mosaicCol in range(1, numberOfMosaicColuns - 1):

            # setting indicator of image cropping
            croppingImageOfROI = False
            croppingImageOfSegmentedImage = False

            # defining the two points of the cropped image
            linP1, colP1, linP2, colP2 = getP1AndP2OfRightDownSlidingCrop(mosaicLin, mosaicCol,
                                                                          sizeSquareImage,
                                                                          imageWidth,
                                                                          imageHeight)

            # selecting mosaic according by ROI
            if isROI(roi, mosaicLin, mosaicCol):
                croppingImageOfROI = True
                # percentageBackgroundDesired = 0
                # if isLeaf(segmentedInputImage, linP1, colP1, linP2, colP2, percentageBackgroundDesired):
                #     croppingImageOfROI = True
            else:
                percentageBackgroundDesired = 10
                if isLeaf(segmentedInputImage, linP1, colP1, linP2, colP2, percentageBackgroundDesired):
                    croppingImageOfSegmentedImage = True

            # selecting mosaic according by ROI
            if croppingImageOfROI or croppingImageOfSegmentedImage:
                # cropping mosaic image
                cropRightDownSlidingImages(inputImage, inputImageName, outputCroppedImagesMosaicPath, sizeSquareImage,
                                           mosaicLin, mosaicCol, mosaicImage,
                                           croppingImageOfROI, croppingImageOfSegmentedImage)

    # saving the mosaic image
    mosaicImageName = outputCroppedImagesMosaicPath + MOSAIC_PATH + inputImageName + '-mosaic-rightDownSliding'
    saveImage(mosaicImageName, mosaicImage)


# ###########################################
# Methods of Level 3
# ###########################################

# check if element belongs to ROI or not
def isROI(roi, mosaicLin, mosaicCol):
    # return False
    lines, columns = roi.shape
    if mosaicLin >= lines or mosaicCol >= columns:
        return False

    element = roi[mosaicLin, mosaicCol]
    return True if element == 'x' else False


# check if cropped image is leaf or background
def isLeaf(segmentedImage, linP1, colP1, linP2, colP2, percentageBackgroundDesired):
    if len(segmentedImage) == 0:
        return False

    # cropping image
    croppedImage = segmentedImage[linP1:linP2, colP1:colP2]

    #  getting cropped image shape
    imageHeight, imageWidth, imageChannel = croppedImage.shape

    # checking if is leaf
    blackPixelsCounter = 0
    for lin in range(imageHeight):
        for col in range(imageWidth):
            if all(croppedImage[lin, col] == [0, 0, 0]):
                blackPixelsCounter += 1

    # calculating the proportion of black pixels (background)
    percentageBackground = (blackPixelsCounter / (imageHeight * imageWidth)) * 100

    # when background is greater than certain value in the cropped image, reject the cropped image
    if percentageBackgroundDesired == 0 and percentageBackground == 0:
        # returning the cropped image is leaf
        return True

    if percentageBackground >= percentageBackgroundDesired:
        # returning the cropped image is NOT leaf
        return False

    # returning the cropped image is leaf
    return True


# crops the image considering the horizontal and vertical bands
def cropHorizontalVerticalImage(inputImage, inputImageName, outputCroppedImagesMosaicPath, sizeSquareImage,
                                mosaicLin, mosaicCol, mosaicImage,
                                croppingImageOfROI, croppingImageOfSegmentedImage):
    # getting the image shape
    imageHeight, imageWidth, imageChannel = inputImage.shape

    # setting the name of cropped mosaic image
    sufixName = '-hv'
    croppedImageName = getCroppedImageName(inputImageName, mosaicLin, mosaicCol, sufixName)
    croppedImagePathAndImageName = outputCroppedImagesMosaicPath + croppedImageName

    # defining the two points of the cropped image
    linP1, colP1, linP2, colP2 = getP1AndP2OfHorizontalVerticalCrop(mosaicLin, mosaicCol, sizeSquareImage,
                                                                    imageWidth, imageHeight)

    # # defining the two points of the cropped image
    # linP1 = (mosaicLin - 1) * sizeSquareImage
    # colP1 = (mosaicCol - 1) * sizeSquareImage
    # linP2 = mosaicLin * sizeSquareImage
    # colP2 = mosaicCol * sizeSquareImage
    #
    # # checking the image boundaries
    # if (colP2 > imageWidth):
    #     colP2 = imageWidth
    #     colP1 = colP2 - sizeSquareImage
    #
    # if (linP2 > imageHeight):
    #     linP2 = imageHeight
    #     linP1 = linP2 - sizeSquareImage

    # cropping and saving bounding box in new image
    croppedImage = inputImage[linP1:linP2, colP1:colP2]
    croppedImageWidth = linP2 - linP1
    croppedImageHeight = colP2 - colP1

    # saving the cropped image
    saveImage(croppedImagePathAndImageName, croppedImage)

    # saving the cropped image details
    saveCroppedImageDetailsFile(outputCroppedImagesMosaicPath, inputImageName, imageHeight, imageWidth,
                                sizeSquareImage, mosaicLin, mosaicCol, linP1, colP1, linP2, colP2,
                                sufixName
                                )

    # draws grid into mosaic image
    if croppingImageOfROI:
        bgrBoxColor = [255, 0, 0]  # blue color
    else:
        bgrBoxColor = [0, 0, 255]  # red color
    thickness = 1
    mosaicImage = drawMosaicImage(mosaicImage,
                                  mosaicLin, mosaicCol,
                                  linP1, colP1, linP2, colP2,
                                  bgrBoxColor,
                                  thickness)


# crops the image considering the right sliding
def cropRightSlidingImage(inputImage, inputImageName, outputCroppedImagesMosaicPath, sizeSquareImage,
                          mosaicLin, mosaicCol, mosaicImage,
                          croppingImageOfROI, croppingImageOfSegmentedImage):
    # getting the image shape
    imageHeight, imageWidth, imageChannel = inputImage.shape

    # setting the name of cropped mosaic image
    sufixName = '-slidRight'
    croppedImageName = getCroppedImageName(inputImageName, mosaicLin, mosaicCol, sufixName)
    croppedImagePathAndImageName = outputCroppedImagesMosaicPath + croppedImageName

    # defining the two points of the cropped image
    linP1, colP1, linP2, colP2 = getP1AndP2OfRightSlidingCrop(mosaicLin, mosaicCol, sizeSquareImage,
                                                              imageWidth, imageHeight)

    # # setting the slide size
    # sizeSlide = int(sizeSquareImage / 2)
    #
    # # defining the two points of the cropped image
    # linP1 = (mosaicLin - 1) * sizeSquareImage
    # colP1 = (mosaicCol - 1) * sizeSquareImage + sizeSlide
    # linP2 = mosaicLin * sizeSquareImage
    # colP2 = mosaicCol * sizeSquareImage + sizeSlide

    # cropping and saving bounding box in new image
    croppedImage = inputImage[linP1:linP2, colP1:colP2]
    croppedImageWidth = linP2 - linP1
    croppedImageHeight = colP2 - colP1

    # saving the cropped image
    saveImage(croppedImagePathAndImageName, croppedImage)

    # saving the cropped image details
    saveCroppedImageDetailsFile(outputCroppedImagesMosaicPath, inputImageName, imageHeight, imageWidth,
                                sizeSquareImage, mosaicLin, mosaicCol, linP1, colP1, linP2, colP2,
                                sufixName
                                )

    # draws grid into mosaic image
    if croppingImageOfROI:
        bgrBoxColor = [255, 0, 0]  # blue color
    else:
        bgrBoxColor = [0, 0, 255]  # red color
    thickness = 1
    mosaicImage = drawMosaicImage(mosaicImage,
                                  mosaicLin, mosaicCol,
                                  linP1, colP1, linP2, colP2,
                                  bgrBoxColor,
                                  thickness)


# crops the image considering the down sliding
def cropDownSlidingImage(inputImage, inputImageName, outputCroppedImagesMosaicPath, sizeSquareImage,
                         mosaicLin, mosaicCol, mosaicImage,
                         croppingImageOfROI, croppingImageOfSegmentedImage):
    # getting the image shape
    imageHeight, imageWidth, imageChannel = inputImage.shape

    # setting the name of cropped mosaic image
    sufixName = '-slidDown'
    croppedImageName = getCroppedImageName(inputImageName, mosaicLin, mosaicCol, sufixName)
    croppedImagePathAndImageName = outputCroppedImagesMosaicPath + croppedImageName

    # defining the two points of the cropped image
    linP1, colP1, linP2, colP2 = getP1AndP2OfDownSlidingCrop(mosaicLin, mosaicCol, sizeSquareImage,
                                                             imageWidth, imageHeight)

    # # setting the slide size
    # sizeSlide = int(sizeSquareImage / 2)
    #
    # # defining the two points of the cropped image
    # linP1 = (mosaicLin - 1) * sizeSquareImage + sizeSlide
    # colP1 = (mosaicCol - 1) * sizeSquareImage
    # linP2 = mosaicLin * sizeSquareImage + sizeSlide
    # colP2 = mosaicCol * sizeSquareImage

    # cropping and saving bounding box in new image
    croppedImage = inputImage[linP1:linP2, colP1:colP2]
    croppedImageWidth = linP2 - linP1
    croppedImageHeight = colP2 - colP1

    # saving the cropped image
    saveImage(croppedImagePathAndImageName, croppedImage)

    # saving the cropped image details
    saveCroppedImageDetailsFile(outputCroppedImagesMosaicPath, inputImageName, imageHeight, imageWidth,
                                sizeSquareImage, mosaicLin, mosaicCol, linP1, colP1, linP2, colP2,
                                sufixName
                                )

    # draws grid into mosaic image
    if croppingImageOfROI:
        bgrBoxColor = [255, 0, 0]  # blue color
    else:
        bgrBoxColor = [0, 0, 255]  # red color
    thickness = 1
    mosaicImage = drawMosaicImage(mosaicImage,
                                  mosaicLin, mosaicCol,
                                  linP1, colP1, linP2, colP2,
                                  bgrBoxColor,
                                  thickness)


# crops the sliding image
def cropRightDownSlidingImages(inputImage, inputImageName, outputCroppedImagesMosaicPath, sizeSquareImage,
                               mosaicLin, mosaicCol, mosaicImage,
                               croppingImageOfROI, croppingImageOfSegmentedImage):
    # getting the image shape
    imageHeight, imageWidth, imageChannel = inputImage.shape

    # setting the name of cropped mosaic image
    sufixName = '-slidRightDown'
    croppedImageName = getCroppedImageName(inputImageName, mosaicLin, mosaicCol, sufixName)
    croppedImagePathAndImageName = outputCroppedImagesMosaicPath + croppedImageName

    # defining the two points of the cropped image
    linP1, colP1, linP2, colP2 = getP1AndP2OfRightDownSlidingCrop(mosaicLin, mosaicCol, sizeSquareImage,
                                                                  imageWidth, imageHeight)

    # # setting the slide size
    # sizeSlide = int(sizeSquareImage / 2)
    #
    # # defining the two points of the cropped image
    # linP1 = (mosaicLin - 1) * sizeSquareImage + sizeSlide
    # colP1 = (mosaicCol - 1) * sizeSquareImage + sizeSlide
    # linP2 = mosaicLin * sizeSquareImage + sizeSlide
    # colP2 = mosaicCol * sizeSquareImage + sizeSlide

    # cropping and saving bounding box in new image
    croppedImage = inputImage[linP1:linP2, colP1:colP2]
    croppedImageWidth = linP2 - linP1
    croppedImageHeight = colP2 - colP1

    # saving the cropped image
    saveImage(croppedImagePathAndImageName, croppedImage)

    # saving the cropped image details
    saveCroppedImageDetailsFile(outputCroppedImagesMosaicPath, inputImageName, imageHeight, imageWidth,
                                sizeSquareImage, mosaicLin, mosaicCol, linP1, colP1, linP2, colP2,
                                sufixName
                                )

    # draws grid into mosaic image
    if croppingImageOfROI:
        bgrBoxColor = [255, 0, 0]  # blue color
    else:
        bgrBoxColor = [0, 0, 255]  # red color
    thickness = 1
    mosaicImage = drawMosaicImage(mosaicImage,
                                  mosaicLin, mosaicCol,
                                  linP1, colP1, linP2, colP2,
                                  bgrBoxColor,
                                  thickness)


# ###########################################
# Methods of Level 4
# ###########################################

def getP1AndP2OfHorizontalVerticalCrop(mosaicLin, mosaicCol, sizeSquareImage, imageWidth, imageHeight):
    # defining the two points of the cropped image
    linP1 = (mosaicLin - 1) * sizeSquareImage
    colP1 = (mosaicCol - 1) * sizeSquareImage
    linP2 = mosaicLin * sizeSquareImage
    colP2 = mosaicCol * sizeSquareImage

    # checking the image boundaries
    if colP2 > imageWidth:
        colP2 = imageWidth
        colP1 = colP2 - sizeSquareImage

    if linP2 > imageHeight:
        linP2 = imageHeight
        linP1 = linP2 - sizeSquareImage

    # returing the two points
    return linP1, colP1, linP2, colP2


def getP1AndP2OfRightSlidingCrop(mosaicLin, mosaicCol, sizeSquareImage, imageWidth, imageHeight):
    # setting the slide size
    sizeSlide = int(sizeSquareImage / 2)

    # defining the two points of the cropped image
    linP1 = (mosaicLin - 1) * sizeSquareImage
    colP1 = (mosaicCol - 1) * sizeSquareImage + sizeSlide
    linP2 = mosaicLin * sizeSquareImage
    colP2 = mosaicCol * sizeSquareImage + sizeSlide

    # returing the two points
    return linP1, colP1, linP2, colP2


def getP1AndP2OfDownSlidingCrop(mosaicLin, mosaicCol, sizeSquareImage, imageWidth, imageHeight):
    # setting the slide size
    sizeSlide = int(sizeSquareImage / 2)

    # defining the two points of the cropped image
    linP1 = (mosaicLin - 1) * sizeSquareImage + sizeSlide
    colP1 = (mosaicCol - 1) * sizeSquareImage
    linP2 = mosaicLin * sizeSquareImage + sizeSlide
    colP2 = mosaicCol * sizeSquareImage

    # returing the two points
    return linP1, colP1, linP2, colP2


def getP1AndP2OfRightDownSlidingCrop(mosaicLin, mosaicCol, sizeSquareImage, imageWidth, imageHeight):
    # setting the slide size
    sizeSlide = int(sizeSquareImage / 2)

    # defining the two points of the cropped image
    linP1 = (mosaicLin - 1) * sizeSquareImage + sizeSlide
    colP1 = (mosaicCol - 1) * sizeSquareImage + sizeSlide
    linP2 = mosaicLin * sizeSquareImage + sizeSlide
    colP2 = mosaicCol * sizeSquareImage + sizeSlide

    # returing the two points
    return linP1, colP1, linP2, colP2


# define the cropped name
def getCroppedImageName(inputImageName, mosaicLin, mosaicCol, sufixName):
    # setting the name of cropped mosaic image
    mosaicLinName = '{:03d}'.format(mosaicLin)
    mosaicColName = '{:03d}'.format(mosaicCol)
    croppedImageName = inputImageName + '-r' + mosaicLinName + '-c' + mosaicColName + sufixName
    return croppedImageName


# save the cropped image
def saveImage(croppedImagePathAndImageName, croppedImage):
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


def drawMosaicImage(image, mosaicLin, mosaicCol, linP1, colP1, linP2, colP2, bgrBoxColor, thickness):
    # Start coordinate, here (5, 5)
    # represents the top left corner of rectangle
    startPoint = (colP1, linP1)

    # Ending coordinate, here (220, 220)
    # represents the bottom right corner of rectangle
    endPoint = (colP2, linP2)

    # Using cv2.rectangle() method
    # Draw a rectangle with blue line borders of thickness of 2 px
    image = cv2.rectangle(image, startPoint, endPoint, bgrBoxColor, thickness)

    # setting bounding box label with the class name and confidence
    label = '(' + str(mosaicLin) + ',' + str(mosaicCol) + ')'
    cv2.putText(image, label,
                (colP1 + 32, linP1 + 32),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, bgrBoxColor, 2)

    # returning the image with bounding box draw
    return image


# segment the image by morphological operations
def segmentByDibio(inputOriginalImagesPath):
    segmentedImage = cv2.imread(inputOriginalImagesPath + 'segmentedImage/P1040801-slic0.jpg')
    return segmentedImage


# segment the image by morphological operations
def segmentByMorphological(inputImage, inputImageName, outputImagesMosaicPath):
    height = 480
    width = 640

    # #################################################################
    # Step 1: threshold image
    # #################################################################

    # convert to hsv
    hsvImage = cv2.cvtColor(inputImage, cv2.COLOR_BGR2HSV)
    # imageWindowName = inputImageName + '-hsvImage'
    # showImageInWindow(hsvImage, imageWindowName, width, height, False)

    # mask of green (36,25,25) ~ (86, 255,255)
    # mask = cv2.inRange(hsvImage, (0, 100, 100), (220, 255, 255))
    mask = cv2.inRange(hsvImage, (40, 40, 40), (70, 255, 255))
    # imageWindowName = inputImageName + '-threshold'
    # showImageInWindow(mask, imageWindowName, width, height, False)

    # #################################################################
    # Step 2: removes noise of the image
    # #################################################################

    # noise removal by opening
    # openingKernel = np.ones((3, 3), np.uint8)
    openingKernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, openingKernel, iterations=2)
    # imageWindowName = inputImageName + '-opening'
    # showImageInWindow(opening, imageWindowName, width, height, False)

    # #################################################################
    # Step 3: get sure foreground area of "opening image" by dilation
    # #################################################################
    dilatingKernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    foregroundImage = cv2.morphologyEx(opening, cv2.MORPH_DILATE, dilatingKernel, iterations=10)
    # imageWindowName = inputImageName + '-foregroundImage-by-dilating-3x3'
    # showImageInWindow(foregroundImage, imageWindowName, width, height, False)

    # dilatingKernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    # foregroundImage = cv2.morphologyEx(foregroundImage, cv2.MORPH_DILATE, dilatingKernel, iterations=5)
    # imageWindowName = inputImageName + '-foregroundImage-by-dilating-5x5'
    # showImageInWindow(foregroundImage, imageWindowName, width, height, False)

    # #################################################################
    # Step 4: multiply the foreground image by input image
    # #################################################################
    imageHeight, imageWidth, imageChannel = inputImage.shape
    resultImage = inputImage.copy()
    resultImage[:, :] = [0, 0, 0]

    # show just the foreground pixels
    for lin in range(0, imageHeight):
        for col in range(0, imageWidth):
            if foregroundImage[lin, col] > 0:
                resultImage[lin, col] = inputImage[lin, col]

    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # saving the result image
    resultImageName = outputImagesMosaicPath + inputImageName + '-just-leaf'
    saveImage(resultImageName, resultImage)

    # returning the result image
    return resultImage


def segmentBySuperPixel(inputImage, inputImageName, outputImagesMosaicPath):
    float_image = img_as_float(inputImage)
    segments_slic = slic(float_image, n_segments=3, compactness=10)

    for index in np.unique(segments_slic):
        segmentedImage = float_image
        segmentedImage[segments_slic == index] = 0.0
        # cv2.imwrite("P1040801-slic{}.jpg".format(index), img_as_ubyte(segmentedImage))

    # saving the result image
    resultImageName = outputImagesMosaicPath + inputImageName + '-just-leaf'
    saveImage(resultImageName, segmentedImage)

    # returning the segmented image
    return segmentedImage


# ###########################################
# Main method
# ###########################################
if __name__ == '__main__':
    # IMAGE_MOSAIC_PATH = 'E:/desenvolvimento/projetos/DoctoralProjects/ImageMosaicProjectImages/'
    # INPUT_ORIGINAL_IMAGES_PATH = \
    #     'E:/desenvolvimento/projetos/DoctoralProjects/ImageMosaicProjectImages/01. input original images/'
    # OUTPUT_CROPPED_IMAGES_MOSAIC_PATH = \
    #     'E:/desenvolvimento/projetos/DoctoralProjects/ImageMosaicProjectImages/02. output cropped images mosaic/'

    # IMAGE_MOSAIC_PATH = 'E:/desenvolvimento/projetos/DoctoralProjects/WhiteFlyExperiment/'
    EXPERIMENT_ROOT_PATH = 'E:/desenvolvimento/projetos/DoctoralProjects/Whitefly_Biology_Group_3.1/'
    EXPERIMENT_IDENTIFICATION_PATH = 'B3R1/'
    INPUT_ORIGINAL_IMAGES_PATH = EXPERIMENT_ROOT_PATH + EXPERIMENT_IDENTIFICATION_PATH + '02.01 - Detection - Original Images/'
    INPUT_SEGMENTED_ORIGINAL_IMAGES_PATH = EXPERIMENT_ROOT_PATH + EXPERIMENT_IDENTIFICATION_PATH + '02.02 - Detection - Segmented Original Images/'
    INPUT_REGION_OF_INTEREST_PATH = EXPERIMENT_ROOT_PATH + EXPERIMENT_IDENTIFICATION_PATH + '02.03 - Detection - Region Of Interest (ROI)/'
    OUTPUT_CROPPED_IMAGES_MOSAIC_PATH = EXPERIMENT_ROOT_PATH + EXPERIMENT_IDENTIFICATION_PATH + '02.04 - Detection - Cropped Images of the Mosaic/'

    print('Creates Images Mosaic')
    print('---------------------------------')
    print('')
    print('Experiment root path         : ', EXPERIMENT_ROOT_PATH)
    print('Input images path            : ', INPUT_ORIGINAL_IMAGES_PATH)
    print('Input segmented images path  : ', INPUT_SEGMENTED_ORIGINAL_IMAGES_PATH)
    print('Input Region Of Interest     : ', INPUT_REGION_OF_INTEREST_PATH)
    print('Mosaic images path           : ', OUTPUT_CROPPED_IMAGES_MOSAIC_PATH)
    print('')

    # setting the size square image to crop with a fixed size (height and width) used in the YOLOv4
    sizeSquareImage = 128

    # processing the annotated images
    processInputImages(EXPERIMENT_ROOT_PATH,
                       INPUT_ORIGINAL_IMAGES_PATH,
                       INPUT_SEGMENTED_ORIGINAL_IMAGES_PATH,
                       INPUT_REGION_OF_INTEREST_PATH,
                       OUTPUT_CROPPED_IMAGES_MOSAIC_PATH,
                       sizeSquareImage)

    # end of processing
    print('End of processing')
