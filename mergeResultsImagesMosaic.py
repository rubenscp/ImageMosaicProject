"""
Project: Create a mosaic of results images from images of any size.
Author: Rubens de Castro Pereira
Advisor: Dibio Leandro Borges
Date: 18/02/2021
Version: 1.0.0
"""

# Importing needed libraries

import os
from shutil import copyfile
import math

# from re import _expand

import cv2

# from Entity.BoundingBox import BoundingBox
# from Entity.DetectedObject import DetectedObject

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
def processInputImages(inputImagesPath, mosaicImagesPath, sizeSquareImage):
    # defining counters
    totalOfImages = 0

    # processing each image of the folder
    for fileName in os.listdir(inputImagesPath):

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
        inputImage = cv2.imread(inputImagesPath + fileName)
        if inputImage is not None:
            # creating new file
            id = inputImageName[1:]
            imageHeight, imageWidth, imageChannel = inputImage.shape
            print(
                'Image: ' + inputImageName + "  shape: " + " height:" + str(imageHeight) + " width:" + str(
                    imageWidth))

        # create the mosaic of images
        cropImagesMosaic(inputImage, inputImageName, sizeSquareImage, mosaicImagesPath)

        # # open file of image annotations
        # imageAnnotationsFile = open(inputImagesPath + imageName + ".txt", "r")
        #
        # # reading next line
        # line = imageAnnotationsFile.readline()
        #
        # # defining id of bounding box
        # idBoundingBox = 0
        #
        # # close file
        # imageAnnotationsFile.close()

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


# crops the bounding box image
def cropImagesMosaic(inputImage, inputImageName, sizeSquareImage, mosaicImagesPath):
    # get image shape
    imageHeight, imageWidth, imageChannel = inputImage.shape

    # calculating number of mosaic
    numberOfMosaicLines = math.ceil(imageHeight / sizeSquareImage)
    numberOfMosaicColuns = math.ceil(imageWidth / sizeSquareImage)

    # cropping images in the horizontal and vertical
    for mosaicLin in range(1, numberOfMosaicLines):
        for mosaicCol in range(1, numberOfMosaicColuns):
            # setting the name of cropped mosaic image
            # mosaicLinName = '{:03d}'.format(mosaicLin)
            # mosaicColName = '{:03d}'.format(mosaicCol)
            # croppedImageName = inputImageName + '-L' + mosaicLinName + '-C' + mosaicColName
            # print(mosaicLinName, mosaicColName, inputImageName, croppedImageName)

            # cropping mosaic image
            cropImage(inputImage, inputImageName, mosaicImagesPath, sizeSquareImage, mosaicLin, mosaicCol)

            # croppedImage = 0
            # point1OriginalLinOfcroppedImage = 0
            # point1OriginalColOfcroppedImage = 0
            # point2OriginalLinOfcroppedImage = 0
            # point2OriginalColOfcroppedImage = 0
            #
            # croppedImagePathAndImageName = 'ccccc'

            # saving cropped mosaic image
            # saveCroppedImage(croppedImagePathAndImageName, croppedImage)


# copy classes file
# def copyClassesFile(annotatedImagesPath, croppedImagesPath, className):
#     croppedImagesPathAndClassFile = croppedImagesPath + className + "/" + "classes.txt"
#     if not os.path.isfile(croppedImagesPathAndClassFile):
#         copyfile(annotatedImagesPath + 'classes.txt', croppedImagesPathAndClassFile)
#

# crops the image
def cropImage(inputImage, inputImageName, mosaicImagesPath, sizeSquareImage, mosaicLin, mosaicCol):
    # setting the name of cropped mosaic image
    mosaicLinName = '{:03d}'.format(mosaicLin)
    mosaicColName = '{:03d}'.format(mosaicCol)
    croppedImageName = inputImageName + '-r' + mosaicLinName + '-c' + mosaicColName
    croppedImagePathAndImageName = mosaicImagesPath + croppedImageName
    print(mosaicLinName, mosaicColName, inputImageName, croppedImageName)

    # defining the two points of the cropped image
    linP1 = (mosaicLin - 1) * 128
    colP1 = (mosaicCol - 1) * 128
    linP2 = mosaicLin * 128
    colP2 = mosaicCol * 128

    # evaluating the final of image

    # # calculating the new coordinates of cropped image
    # if objectPosition == 'center':
    #     linP1, colP1, linP2, colP2 = calculateNewCoordinatesOfBoundingBoxInCenter(annotatedBoundingBox)
    #
    # # evaluating if is possible create the cropped bounding box
    # if (linP1 < 0 or colP1 < 0 or linP2 < 0 or colP2 < 0):
    #     return False

    # cropping and saving bounding box in new image
    croppedImage = inputImage[linP1:linP2, colP1:colP2]
    croppedImageWidth = linP2 - linP1
    croppedImageHeight = colP2 - colP1

    # # setting the full path and image name
    # croppedImagePathAndImageName = getCroppedBoundingBoxImageName(croppedImagesPath, imageName,
    # className, idBoundingBox, objectPosition)

    # saving the cropped image
    saveCroppedImage(croppedImagePathAndImageName, croppedImage)

    # # saving cropped annotation file
    # saveCroppedBoundingBoxAnnotationFile(croppedImageWidth, croppedImageHeight, croppedImagePathAndImageName,
    #                                      annotatedBoundingBox, linP1, colP1, linP2, colP2)

    # return True


# ###########################################
# Methods of Level 3
# ###########################################


# def createDirectory(croppedImagesPath, className):
#     fullPathName = croppedImagesPath + className
#     directory = os.path.dirname(fullPathName)
#     if not os.path.exists(fullPathName):
#         os.makedirs(fullPathName)


# # calculates the new coordinates of the cropped image of bounding box
# def calculateNewCoordinatesOfBoundingBoxInCenter(annotatedBoundingBox):
#     # defining rectangle to crop the original image
#     linP1 = annotatedBoundingBox.linPoint1
#     colP1 = annotatedBoundingBox.colPoint1
#     linP2 = annotatedBoundingBox.linPoint2
#     colP2 = annotatedBoundingBox.colPoint2
#
#     # calculating the dimensions of cropped image
#     heightBoundingBox = linP2 - linP1
#     widthBoundingBox = colP2 - colP1
#
#     # calculating the new position of bounding box according the position
#     heightDifference = sizeSquareImage - heightBoundingBox
#     widthDifference = sizeSquareImage - widthBoundingBox
#     halfOfHeightDifference = int(heightDifference / 2.0)
#     halfOfWidthDifference = int(widthDifference / 2.0)
#
#     # setting the new coordinates
#     linP1 = linP1 - halfOfHeightDifference
#     colP1 = colP1 - halfOfWidthDifference
#     linP2 = linP2 + halfOfHeightDifference
#     colP2 = colP2 + halfOfWidthDifference
#
#     # fine adjusting in the positions
#     if (linP2 - linP1) % 32 != 0:
#         linP2 += 1
#     if (colP2 - colP1) % 32 != 0:
#         colP2 += 1
#
#     return linP1, colP1, linP2, colP2


# # get the name of cropped image
# def getCroppedBoundingBoxImageName(croppedImagesPath, originalImageName, className, idBoundingBox, objectPosition):
#     return croppedImagesPath + className + "/" \
#            + originalImageName + '-' + className + '-bbox-' + str(idBoundingBox) + '-' + objectPosition


# save the cropped image
def saveCroppedImage(croppedImagePathAndImageName, croppedImage):
    # croppedImageName = croppedImagePathAndImageName
    cv2.imwrite(croppedImagePathAndImageName + '.jpg', croppedImage)
    print(croppedImagePathAndImageName)


# save the bounding box image
def saveCroppedBoundingBoxAnnotationFile(croppedImageWidth, croppedImageHeight,
                                         croppedImagePathAndImageName,
                                         annotatedBoundingBox, linP1, colP1, linP2, colP2):
    # setting annotation file
    yoloAnnotationsFile = open(croppedImagePathAndImageName + '.txt', 'a+')

    # setting new bounding box in yolo format
    croppedLinP1 = annotatedBoundingBox.linPoint1 - linP1
    croppedColP1 = annotatedBoundingBox.colPoint1 - colP1
    croppedLinP2 = annotatedBoundingBox.linPoint2 - linP1
    croppedColP2 = annotatedBoundingBox.colPoint2 - colP1
    croppedBoundingBox = BoundingBox(croppedLinP1, croppedColP1, croppedLinP2, croppedColP2,
                                     annotatedBoundingBox.className)

    # getting the bounding box coordinates in  Yolo format
    linOfCentrePoint, colOfCentrePoint, widthOfCentrePoint, heightOfCentrePoint = croppedBoundingBox.getYoloAnnotation(
        croppedImageWidth, croppedImageHeight)

    # setting line to write
    line = str(DetectedObject.getValueOf(croppedBoundingBox.className)) + ' ' \
           + "{:.6f}".format(colOfCentrePoint) + ' ' \
           + "{:.6f}".format(linOfCentrePoint) + ' ' \
           + "{:.6f}".format(widthOfCentrePoint) + ' ' \
           + "{:.6f}".format(heightOfCentrePoint) \
           + LINE_FEED

    # write line
    yoloAnnotationsFile.write(line)

    # closing annotation file
    yoloAnnotationsFile.close()


# ###########################################
# Main method
# ###########################################
if __name__ == '__main__':
    INPUT_IMAGES_PATHS = \
        'E:/desenvolvimento/projetos/DoctoralProjects/ImageMosaicProjectImages/input_images/'
    MOSAIC_IMAGES_PATH = \
        'E:/desenvolvimento/projetos/DoctoralProjects/ImageMosaicProjectImages/output_images_mosaic/'

    print('Images Mosaic')
    print('---------------------------------')
    print('')
    print('Input images path    : ', INPUT_IMAGES_PATHS)
    print('Mosaic images path  : ', MOSAIC_IMAGES_PATH)
    print('')

    # setting the size square image to crop with a fixed size (height and width) used in the YOLOv4
    sizeSquareImage = 128

    # processing the annotated images
    processInputImages(INPUT_IMAGES_PATHS, MOSAIC_IMAGES_PATH, sizeSquareImage)

    # end of processing
    print('End of processing')
