"""
Project: Crops multiple bounding boxes of exuvia, instars and adults and creates new images to each object anottated.
Author: Rubens de Castro Pereira
Advisor: Dibio Leandro Borges
Date: 14/01/2021
Version: 1.0.0
"""

#
# Create all bounding boxes files in the Yolo format where each annotated object produces until 9(nine) new cropped images
# with the object positioned in different positions.

# Importing needed libraries

import os
from shutil import copyfile

# from re import _expand

import cv2

from Entity.BoundingBox import BoundingBox
from Entity.DetectedObject import DetectedObject

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


# process all annotated images
def processAnnotatedImages(annotatedImagesPath, croppedImagesPath, sizeSquareImage):
    # defining counters
    totalOfImages = 0
    totalOfBoundingBoxes = 0
    totalOfExuviaBoundingBoxesImages = 0
    totalOfInstar1BoundingBoxesImages = 0
    totalOfInstar2BoundingBoxesImages = 0
    totalOfInstar3BoundingBoxesImages = 0
    totalOfInstar4BoundingBoxesImages = 0
    totalOfAdultaBoundingBoxesImages = 0
    totalOfOvoBoundingBoxesImages = 0
    totalOfInstar1ou2BoundingBoxesImages = 0
    totalOfInstar3ou4BoundingBoxesImages = 0

    numberOfInstar1 = 0
    numberOfInstar2 = 0
    numberOfInstar3 = 0
    numberOfInstar4 = 0

    for fileName in os.listdir(annotatedImagesPath):

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
        imageName = fileName[:jpegPosition - 1]

        # adding image counter
        totalOfImages += 1

        # reading image
        print('')
        print('Reading image:', fileName)
        annotatedImage = cv2.imread(annotatedImagesPath + fileName)
        if annotatedImage is not None:
            # creating new file
            id = imageName[1:]
            annotatedImageHeight, annotatedImageWidth, annotatedImageChannel = annotatedImage.shape
            print(
                'Image: ' + imageName + "  shape: " + " height:" + str(annotatedImageHeight) + " width:" + str(
                    annotatedImageWidth))

        # open file of image annotations
        imageAnnotationsFile = open(annotatedImagesPath + imageName + ".txt", "r")

        # reading next line
        line = imageAnnotationsFile.readline()

        # defining id of bounding box
        idBoundingBox = 0

        # processing the file of ground truth data
        counter = 0
        while line != '':
            # increment counter
            counter += 1

            # getting the array of values
            values = line.split(' ')
            # print(values)

            idBoundingBox += 1
            imageWidth = 0
            imageHeight = 0
            idClass = int(values[0])
            colOfCentrePoint = float(values[1])
            linOfCentrePoint = float(values[2])
            heightOfCentrePoint = float(values[3])
            widthOfCentrePoint = float(values[4])

            # creating a new bounding box instance
            annotatedBoundingBox = BoundingBox(0, 0, 0, 0, '')
            annotatedBoundingBox.setYoloAnnotation(annotatedImageHeight, annotatedImageWidth, colOfCentrePoint,
                                                   linOfCentrePoint, widthOfCentrePoint, heightOfCentrePoint,
                                                   idBoundingBox,
                                                   idClass)

            # counting number of instars
            if annotatedBoundingBox.className == 'instar1':
                numberOfInstar1 += 1
            if annotatedBoundingBox.className == 'instar2':
                numberOfInstar2 += 1
            if annotatedBoundingBox.className == 'instar3':
                numberOfInstar3 += 1
            if annotatedBoundingBox.className == 'instar4':
                numberOfInstar4 += 1

            # merging classes
            if (annotatedBoundingBox.className == 'instar1' or annotatedBoundingBox.className == 'instar2'):
                if numberOfInstar1 > 65 or numberOfInstar2 > 65:
                    # reading next line
                    line = imageAnnotationsFile.readline()
                    continue
                annotatedBoundingBox.className = 'instar1ou2'

            if (annotatedBoundingBox.className == 'instar3' or annotatedBoundingBox.className == 'instar4'):
                if numberOfInstar3 > 65 or numberOfInstar4 > 65:
                    # reading next line
                    line = imageAnnotationsFile.readline()
                    continue
                annotatedBoundingBox.className = 'instar3ou4'

            print(imageName,
                  'bb', idBoundingBox,
                  'height', (annotatedBoundingBox.linPoint2 - annotatedBoundingBox.linPoint1),
                  'width', (annotatedBoundingBox.colPoint2 - annotatedBoundingBox.colPoint1))

            # cropping bounding box
            cropBoundingBox(annotatedImage, annotatedBoundingBox, sizeSquareImage, croppedImagesPath, imageName,
                            annotatedBoundingBox.className, str(idBoundingBox),
                            'center')
            cropBoundingBox(annotatedImage, annotatedBoundingBox, sizeSquareImage, croppedImagesPath, imageName,
                            annotatedBoundingBox.className, str(idBoundingBox),
                            'north')
            cropBoundingBox(annotatedImage, annotatedBoundingBox, sizeSquareImage, croppedImagesPath, imageName,
                            annotatedBoundingBox.className, str(idBoundingBox),
                            'south')
            cropBoundingBox(annotatedImage, annotatedBoundingBox, sizeSquareImage, croppedImagesPath, imageName,
                            annotatedBoundingBox.className, str(idBoundingBox),
                            'east')
            cropBoundingBox(annotatedImage, annotatedBoundingBox, sizeSquareImage, croppedImagesPath, imageName,
                            annotatedBoundingBox.className, str(idBoundingBox),
                            'west')
            cropBoundingBox(annotatedImage, annotatedBoundingBox, sizeSquareImage, croppedImagesPath, imageName,
                            annotatedBoundingBox.className, str(idBoundingBox),
                            'northeast')
            cropBoundingBox(annotatedImage, annotatedBoundingBox, sizeSquareImage, croppedImagesPath, imageName,
                            annotatedBoundingBox.className, str(idBoundingBox),
                            'northwest')
            cropBoundingBox(annotatedImage, annotatedBoundingBox, sizeSquareImage, croppedImagesPath, imageName,
                            annotatedBoundingBox.className, str(idBoundingBox),
                            'southeast')
            cropBoundingBox(annotatedImage, annotatedBoundingBox, sizeSquareImage, croppedImagesPath, imageName,
                            annotatedBoundingBox.className, str(idBoundingBox),
                            'southwest')

            # copying  classes name file
            copyClassesFile(annotatedImagesPath, croppedImagesPath, annotatedBoundingBox.className)

            # counting total bounding boxes
            totalOfBoundingBoxes += 1

            # counting bounding boxes
            if annotatedBoundingBox.className == 'exuvia':
                totalOfExuviaBoundingBoxesImages += 1
            elif annotatedBoundingBox.className == 'instar1':
                totalOfInstar1BoundingBoxesImages += 1
            elif annotatedBoundingBox.className == 'instar2':
                totalOfInstar2BoundingBoxesImages += 1
            elif annotatedBoundingBox.className == 'instar3':
                totalOfInstar3BoundingBoxesImages += 1
            elif annotatedBoundingBox.className == 'instar4':
                totalOfInstar4BoundingBoxesImages += 1
            elif annotatedBoundingBox.className == 'adulta':
                totalOfAdultaBoundingBoxesImages += 1
            elif annotatedBoundingBox.className == 'ovo':
                totalOfOvoBoundingBoxesImages += 1
            elif annotatedBoundingBox.className == 'instar1ou2':
                totalOfInstar1ou2BoundingBoxesImages += 1
            elif annotatedBoundingBox.className == 'instar3ou4':
                totalOfInstar3ou4BoundingBoxesImages += 1

            # -----------------
            # reading next line
            # -----------------
            line = imageAnnotationsFile.readline()

        # close file
        imageAnnotationsFile.close()

    # printing statistics
    print('')
    print('Estatísticas do Processamento:')
    print('------------------------------')
    print('Total de imagens                 : ', totalOfImages)
    print('Total de bounding boxes          : ', totalOfBoundingBoxes)
    print('Total de imagens de exuvia       : ', totalOfExuviaBoundingBoxesImages)
    print('Total de imagens de instar1      : ', totalOfInstar1BoundingBoxesImages)
    print('Total de imagens de instar2      : ', totalOfInstar2BoundingBoxesImages)
    print('Total de imagens de instar3      : ', totalOfInstar3BoundingBoxesImages)
    print('Total de imagens de instar4      : ', totalOfInstar4BoundingBoxesImages)
    print('Total de imagens de adultas      : ', totalOfAdultaBoundingBoxesImages)
    print('Total de imagens de ovo          : ', totalOfOvoBoundingBoxesImages)
    print('Total de imagens de instar1 ou 2 : ', totalOfInstar1ou2BoundingBoxesImages)
    print('Total de imagens de instar3 ou 4 : ', totalOfInstar3ou4BoundingBoxesImages)

    print('Máximo Height                : ', sizeSquareImage)
    print('Máximo Width                 : ', sizeSquareImage)
    print('')


# ###########################################
# Methods of Level 2
# ###########################################


# copy classes file
def copyClassesFile(annotatedImagesPath, croppedImagesPath, className):
    croppedImagesPathAndClassFile = croppedImagesPath + className + "/" + "classes.txt"
    if not os.path.isfile(croppedImagesPathAndClassFile):
        copyfile(annotatedImagesPath + 'classes.txt', croppedImagesPathAndClassFile)


# crops the bounding box image
def cropBoundingBox(annotatedImage, annotatedBoundingBox, sizeSquareImage,
                    croppedImagesPath, imageName, className, idBoundingBox, objectPosition):
    # creating the specific folder
    createDirectory(croppedImagesPath, className)

    # calculating the new coordinates of cropped image
    if objectPosition == 'center':
        linP1, colP1, linP2, colP2 = calculateNewCoordinatesOfBoundingBoxInCenter(annotatedBoundingBox)
    elif objectPosition == 'north':
        linP1, colP1, linP2, colP2 = calculateNewCoordinatesOfBoundingBoxInNorth(annotatedBoundingBox)
    elif objectPosition == 'south':
        linP1, colP1, linP2, colP2 = calculateNewCoordinatesOfBoundingBoxInSouth(annotatedBoundingBox)
    elif objectPosition == 'east':
        linP1, colP1, linP2, colP2 = calculateNewCoordinatesOfBoundingBoxInEast(annotatedBoundingBox)
    elif objectPosition == 'west':
        linP1, colP1, linP2, colP2 = calculateNewCoordinatesOfBoundingBoxInWest(annotatedBoundingBox)
    elif objectPosition == 'northeast':
        linP1, colP1, linP2, colP2 = calculateNewCoordinatesOfBoundingBoxInNortheast(annotatedBoundingBox)
    elif objectPosition == 'northwest':
        linP1, colP1, linP2, colP2 = calculateNewCoordinatesOfBoundingBoxInNorthwest(annotatedBoundingBox)
    elif objectPosition == 'southeast':
        linP1, colP1, linP2, colP2 = calculateNewCoordinatesOfBoundingBoxInSoutheast(annotatedBoundingBox)
    elif objectPosition == 'southwest':
        linP1, colP1, linP2, colP2 = calculateNewCoordinatesOfBoundingBoxInSouthwest(annotatedBoundingBox)

    # evaluating if is possible create the cropped bounding box
    if (linP1 < 0 or colP1 < 0 or linP2 < 0 or colP2 < 0):
        return False

        # cropping and saving bounding box in new image
    croppedBoundingBoxImage = annotatedImage[linP1:linP2, colP1:colP2]
    croppedImageWidth = linP2 - linP1
    croppedImageHeight = colP2 - colP1

    # setting the full path and image name
    croppedImagePathAndImageName = getCroppedBoundingBoxImageName(croppedImagesPath, imageName,
                                                                  className, idBoundingBox, objectPosition)

    # saving the cropped image
    saveCroppedBoundingBoxImage(croppedImagePathAndImageName, croppedBoundingBoxImage)

    # saving cropped annotation file
    saveCroppedBoundingBoxAnnotationFile(croppedImageWidth, croppedImageHeight, croppedImagePathAndImageName,
                                         annotatedBoundingBox, linP1, colP1, linP2, colP2)

    return True


# ###########################################
# Methods of Level 3
# ###########################################

def createDirectory(croppedImagesPath, className):
    fullPathName = croppedImagesPath + className
    directory = os.path.dirname(fullPathName)
    if not os.path.exists(fullPathName):
        os.makedirs(fullPathName)


# calculates the new coordinates of the cropped image of bounding box
def calculateNewCoordinatesOfBoundingBoxInCenter(annotatedBoundingBox):
    # defining rectangle to crop the original image
    linP1 = annotatedBoundingBox.linPoint1
    colP1 = annotatedBoundingBox.colPoint1
    linP2 = annotatedBoundingBox.linPoint2
    colP2 = annotatedBoundingBox.colPoint2

    # calculating the dimensions of cropped image
    heightBoundingBox = linP2 - linP1
    widthBoundingBox = colP2 - colP1

    # calculating the new position of bounding box according the position
    heightDifference = sizeSquareImage - heightBoundingBox
    widthDifference = sizeSquareImage - widthBoundingBox
    halfOfHeightDifference = int(heightDifference / 2.0)
    halfOfWidthDifference = int(widthDifference / 2.0)

    # setting the new coordinates
    linP1 = linP1 - halfOfHeightDifference
    colP1 = colP1 - halfOfWidthDifference
    linP2 = linP2 + halfOfHeightDifference
    colP2 = colP2 + halfOfWidthDifference

    # fine adjusting in the positions
    if (linP2 - linP1) % 32 != 0:
        linP2 += 1
    if (colP2 - colP1) % 32 != 0:
        colP2 += 1

    return linP1, colP1, linP2, colP2


# calculates the new coordinates of the cropped image of bounding box
def calculateNewCoordinatesOfBoundingBoxInNorth(annotatedBoundingBox):
    # defining rectangle to crop the original image
    linP1 = annotatedBoundingBox.linPoint1
    colP1 = annotatedBoundingBox.colPoint1
    linP2 = annotatedBoundingBox.linPoint2
    colP2 = annotatedBoundingBox.colPoint2

    # calculating the dimensions of cropped image
    heightBoundingBox = linP2 - linP1
    widthBoundingBox = colP2 - colP1

    # calculating the new position of bounding box according the position
    heightDifference = sizeSquareImage - heightBoundingBox
    widthDifference = sizeSquareImage - widthBoundingBox
    halfOfHeightDifference = int(heightDifference / 2.0)
    halfOfWidthDifference = int(widthDifference / 2.0)

    # setting the new coordinates
    linP1 = linP1
    colP1 = colP1 - halfOfWidthDifference
    linP2 = linP1 + sizeSquareImage
    colP2 = colP2 + halfOfWidthDifference

    # fine adjusting in the positions
    if (linP2 - linP1) % 32 != 0:
        linP2 += 1
    if (colP2 - colP1) % 32 != 0:
        colP2 += 1

    return linP1, colP1, linP2, colP2


# calculates the new coordinates of the cropped image of bounding box
def calculateNewCoordinatesOfBoundingBoxInSouth(annotatedBoundingBox):
    # defining rectangle to crop the original image
    linP1 = annotatedBoundingBox.linPoint1
    colP1 = annotatedBoundingBox.colPoint1
    linP2 = annotatedBoundingBox.linPoint2
    colP2 = annotatedBoundingBox.colPoint2

    # calculating the dimensions of cropped image
    heightBoundingBox = linP2 - linP1
    widthBoundingBox = colP2 - colP1

    # calculating the new position of bounding box according the position
    heightDifference = sizeSquareImage - heightBoundingBox
    widthDifference = sizeSquareImage - widthBoundingBox
    halfOfHeightDifference = int(heightDifference / 2.0)
    halfOfWidthDifference = int(widthDifference / 2.0)

    # setting the new coordinates
    linP1 = linP1 - sizeSquareImage + heightBoundingBox
    colP1 = colP1 - halfOfWidthDifference
    linP2 = linP2
    colP2 = colP2 + halfOfWidthDifference

    # fine adjusting in the positions
    if (linP2 - linP1) % 32 != 0:
        linP2 += 1
    if (colP2 - colP1) % 32 != 0:
        colP2 += 1

    return linP1, colP1, linP2, colP2


# calculates the new coordinates of the cropped image of bounding box
def calculateNewCoordinatesOfBoundingBoxInEast(annotatedBoundingBox):
    # defining rectangle to crop the original image
    linP1 = annotatedBoundingBox.linPoint1
    colP1 = annotatedBoundingBox.colPoint1
    linP2 = annotatedBoundingBox.linPoint2
    colP2 = annotatedBoundingBox.colPoint2

    # calculating the dimensions of cropped image
    heightBoundingBox = linP2 - linP1
    widthBoundingBox = colP2 - colP1

    # calculating the new position of bounding box according the position
    heightDifference = sizeSquareImage - heightBoundingBox
    widthDifference = sizeSquareImage - widthBoundingBox
    halfOfHeightDifference = int(heightDifference / 2.0)
    halfOfWidthDifference = int(widthDifference / 2.0)

    # setting the new coordinates
    linP1 = linP1 - halfOfHeightDifference
    colP1 = colP2 - sizeSquareImage
    linP2 = linP2 + halfOfHeightDifference
    colP2 = colP2

    # fine adjusting in the positions
    if (linP2 - linP1) % 32 != 0:
        linP2 += 1
    if (colP2 - colP1) % 32 != 0:
        colP2 += 1

    return linP1, colP1, linP2, colP2


# calculates the new coordinates of the cropped image of bounding box
def calculateNewCoordinatesOfBoundingBoxInWest(annotatedBoundingBox):
    # defining rectangle to crop the original image
    linP1 = annotatedBoundingBox.linPoint1
    colP1 = annotatedBoundingBox.colPoint1
    linP2 = annotatedBoundingBox.linPoint2
    colP2 = annotatedBoundingBox.colPoint2

    # calculating the dimensions of cropped image
    heightBoundingBox = linP2 - linP1
    widthBoundingBox = colP2 - colP1

    # calculating the new position of bounding box according the position
    heightDifference = sizeSquareImage - heightBoundingBox
    widthDifference = sizeSquareImage - widthBoundingBox
    halfOfHeightDifference = int(heightDifference / 2.0)
    halfOfWidthDifference = int(widthDifference / 2.0)

    # setting the new coordinates
    linP1 = linP1 - halfOfHeightDifference
    colP1 = colP1
    linP2 = linP2 + halfOfHeightDifference
    colP2 = colP1 + sizeSquareImage

    # fine adjusting in the positions
    if (linP2 - linP1) % 32 != 0:
        linP2 += 1
    if (colP2 - colP1) % 32 != 0:
        colP2 += 1

    return linP1, colP1, linP2, colP2


# calculates the new coordinates of the cropped image of bounding box
def calculateNewCoordinatesOfBoundingBoxInNortheast(annotatedBoundingBox):
    # defining rectangle to crop the original image
    linP1 = annotatedBoundingBox.linPoint1
    colP1 = annotatedBoundingBox.colPoint1
    linP2 = annotatedBoundingBox.linPoint2
    colP2 = annotatedBoundingBox.colPoint2

    # calculating the dimensions of cropped image
    heightBoundingBox = linP2 - linP1
    widthBoundingBox = colP2 - colP1

    # calculating the new position of bounding box according the position
    heightDifference = sizeSquareImage - heightBoundingBox
    widthDifference = sizeSquareImage - widthBoundingBox
    halfOfHeightDifference = int(heightDifference / 2.0)
    halfOfWidthDifference = int(widthDifference / 2.0)

    # setting the new coordinates
    linP1 = linP1
    colP1 = colP1 - sizeSquareImage + widthBoundingBox
    linP2 = linP2 + sizeSquareImage - heightBoundingBox
    colP2 = colP2

    # fine adjusting in the positions
    if (linP2 - linP1) % 32 != 0:
        linP2 += 1
    if (colP2 - colP1) % 32 != 0:
        colP2 += 1

    return linP1, colP1, linP2, colP2


# calculates the new coordinates of the cropped image of bounding box
def calculateNewCoordinatesOfBoundingBoxInNorthwest(annotatedBoundingBox):
    # defining rectangle to crop the original image
    linP1 = annotatedBoundingBox.linPoint1
    colP1 = annotatedBoundingBox.colPoint1
    linP2 = annotatedBoundingBox.linPoint2
    colP2 = annotatedBoundingBox.colPoint2

    # calculating the dimensions of cropped image
    heightBoundingBox = linP2 - linP1
    widthBoundingBox = colP2 - colP1

    # calculating the new position of bounding box according the position
    heightDifference = sizeSquareImage - heightBoundingBox
    widthDifference = sizeSquareImage - widthBoundingBox
    halfOfHeightDifference = int(heightDifference / 2.0)
    halfOfWidthDifference = int(widthDifference / 2.0)

    # setting the new coordinates
    linP1 = linP1
    colP1 = colP1
    linP2 = linP2 + sizeSquareImage - heightBoundingBox
    colP2 = colP2 + sizeSquareImage - widthBoundingBox

    # fine adjusting in the positions
    if (linP2 - linP1) % 32 != 0:
        linP2 += 1
    if (colP2 - colP1) % 32 != 0:
        colP2 += 1

    return linP1, colP1, linP2, colP2


# calculates the new coordinates of the cropped image of bounding box
def calculateNewCoordinatesOfBoundingBoxInSoutheast(annotatedBoundingBox):
    # defining rectangle to crop the original image
    linP1 = annotatedBoundingBox.linPoint1
    colP1 = annotatedBoundingBox.colPoint1
    linP2 = annotatedBoundingBox.linPoint2
    colP2 = annotatedBoundingBox.colPoint2

    # calculating the dimensions of cropped image
    heightBoundingBox = linP2 - linP1
    widthBoundingBox = colP2 - colP1

    # calculating the new position of bounding box according the position
    heightDifference = sizeSquareImage - heightBoundingBox
    widthDifference = sizeSquareImage - widthBoundingBox
    halfOfHeightDifference = int(heightDifference / 2.0)
    halfOfWidthDifference = int(widthDifference / 2.0)

    # setting the new coordinates
    linP1 = linP1 - sizeSquareImage + heightBoundingBox
    colP1 = colP1 - sizeSquareImage + widthBoundingBox
    linP2 = linP2
    colP2 = colP2

    # fine adjusting in the positions
    if (linP2 - linP1) % 32 != 0:
        linP2 += 1
    if (colP2 - colP1) % 32 != 0:
        colP2 += 1

    return linP1, colP1, linP2, colP2


# calculates the new coordinates of the cropped image of bounding box
def calculateNewCoordinatesOfBoundingBoxInSouthwest(annotatedBoundingBox):
    # defining rectangle to crop the original image
    linP1 = annotatedBoundingBox.linPoint1
    colP1 = annotatedBoundingBox.colPoint1
    linP2 = annotatedBoundingBox.linPoint2
    colP2 = annotatedBoundingBox.colPoint2

    # calculating the dimensions of cropped image
    heightBoundingBox = linP2 - linP1
    widthBoundingBox = colP2 - colP1

    # calculating the new position of bounding box according the position
    heightDifference = sizeSquareImage - heightBoundingBox
    widthDifference = sizeSquareImage - widthBoundingBox
    halfOfHeightDifference = int(heightDifference / 2.0)
    halfOfWidthDifference = int(widthDifference / 2.0)

    # setting the new coordinates
    linP1 = linP1 - sizeSquareImage + heightBoundingBox
    colP1 = colP1
    linP2 = linP2
    colP2 = colP2 + sizeSquareImage - widthBoundingBox

    # fine adjusting in the positions
    if (linP2 - linP1) % 32 != 0:
        linP2 += 1
    if (colP2 - colP1) % 32 != 0:
        colP2 += 1

    return linP1, colP1, linP2, colP2


# get the name of cropped image
def getCroppedBoundingBoxImageName(croppedImagesPath, originalImageName, className, idBoundingBox, objectPosition):
    return croppedImagesPath + className + "/" \
           + originalImageName + '-' + className + '-bbox-' + str(idBoundingBox) + '-' + objectPosition


# save the bounding box image
def saveCroppedBoundingBoxImage(croppedImagePathAndImageName, croppedImage):
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
    ANNOTATED_BOUNDING_BOXES_DATABASE_PATH = \
        'E:/desenvolvimento/projetos/DoctoralProjects/CropMultipleBoundingBoxesProjectImages/Block 30/30.1 White Fly Annotated Original Images/'
    CROPPED_BOUNDING_BOXES_DATABASE_PATH = \
        'E:/desenvolvimento/projetos/DoctoralProjects/CropMultipleBoundingBoxesProjectImages/Block 30/30.2 White Fly Cropped Images by Classes/'

    print('Cropping Annotated Bounding Boxes')
    print('---------------------------------')
    print('')
    print('Input images path    : ', ANNOTATED_BOUNDING_BOXES_DATABASE_PATH)
    print('Cropped images path  : ', CROPPED_BOUNDING_BOXES_DATABASE_PATH)
    print('')
    # deleting all images of the folder
    # os.remove(CROPPED_BOUNDING_BOXES_DATABASE_PATH + "*.*")

    # setting the size square image to crop with a fixed size (height and width) used in the YOLOv4
    sizeSquareImage = 128

    # processing the annotated images
    processAnnotatedImages(ANNOTATED_BOUNDING_BOXES_DATABASE_PATH, CROPPED_BOUNDING_BOXES_DATABASE_PATH,
                           sizeSquareImage)

    # end of processing
    print('End of processing')
