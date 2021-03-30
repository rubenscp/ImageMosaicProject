"""
Project: Merge a mosaic of images from images of any size.
Author: Rubens de Castro Pereira
Advisor: Dibio Leandro Borges
Date: 04/03/2021
Version: 1.0.0
"""

# Importing needed libraries
import os
import json
import cv2
import pathlib
from shutil import copyfile

from Entity.BoundingBox import BoundingBox
from Entity.CroppedImageDetails import CroppedImageDetails
from Entity.DetectedObjectsCroppedImage import DetectedObjectsCroppedImage
from Entity.BoundingBoxOfDetectedObject import BoundingBoxOfDetectedObject

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
def processInputImages(inputOriginalImagesPath, outputCroppedImagesMosaicPath, inputDetectedCroppedImagesPath,
                       outputMergedImagesPath, sizeSquareImage, confidenceThreshold):
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

        # merge all cropped images into one imagem
        processDetectionResultsOfOneImage(inputImage, inputImageName, sizeSquareImage, outputCroppedImagesMosaicPath,
                                          inputDetectedCroppedImagesPath, outputMergedImagesPath, confidenceThreshold)

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


# merges all cropped images into on image
def processDetectionResultsOfOneImage(inputImage, inputImageName, sizeSquareImage, outputCroppedImagesMosaicPath,
                                      inputDetectedCroppedImagesPath, outputMergedImagesPath, confidenceThreshold):
    # initializing list of all detected objects of one image
    detectedObjectsCroppedImagesList = []
    allBoundingBoxOfDetectedObjectsList = []
    allBoundingBoxOfDetectedObjectsThresholdedList = []

    # get image shape
    # imageHeight, imageWidth, imageChannel = inputImage.shape

    # getting all detected cropped images according by original image
    detectedCroppedImages = list(pathlib.Path(inputDetectedCroppedImagesPath).glob(inputImageName + '*.jpg'))
    detectedCroppedImages.sort()

    # updating each detected cropped image in original image
    for detectedCroppedImagePath in detectedCroppedImages:
        # getting the file name
        detectedCroppedImageNameJpg = os.path.basename(detectedCroppedImagePath)
        detectedCroppedImageName = os.path.splitext(detectedCroppedImageNameJpg)[0]

        print('Processing detected cropped image: ', detectedCroppedImageName)

        # getting the list of detected objects bouding boxes
        detectionLogFileName = inputDetectedCroppedImagesPath + detectedCroppedImageName + '-detection-log.txt'
        detectedObjectsBoundingBoxesList = getDetectedObjectsList(detectionLogFileName,
                                                                  detectedCroppedImageName,
                                                                  confidenceThreshold)

        # getting the list of all detected objects of the image
        if len(detectedObjectsBoundingBoxesList) > 0:
            # adding list of detected objects of one image
            # detectedObjectsCroppedImagesList.extend(detectedObjectsBoundingBoxesList)

            # getting the details of cropped image
            croppedImageDetails = getCroppedImageDetails(outputCroppedImagesMosaicPath, detectedCroppedImageName)

            # defining list of detected objects in the cropped image
            detectedObjectsCroppedImage = DetectedObjectsCroppedImage(croppedImageDetails,
                                                                      detectedObjectsBoundingBoxesList)

            # adding list of detected objects of one image
            detectedObjectsCroppedImagesList.append(detectedObjectsCroppedImage)

            # adding in list of all detected objects (one by one)
            for detectedObjectBoundingBox in detectedObjectsBoundingBoxesList:
                allBoundingBoxOfDetectedObjectsList.append(
                    BoundingBoxOfDetectedObject(croppedImageDetails, detectedObjectBoundingBox))

    # removing detected bounding boxes with value less than confidence threshold and
    for boundingBoxOfDetectedObject in allBoundingBoxOfDetectedObjectsList:
        # selecting just the detected bounding boxes with confidence greater or equal confidence threshold
        if boundingBoxOfDetectedObject.boundingBox.confidence >= confidenceThreshold:
            # calculating all coordinates of bounding boxes according by original images
            boundingBoxOfDetectedObject.setCoordinatesInOriginalImage()

            # adding the boudin box od detected objects into the list
            allBoundingBoxOfDetectedObjectsThresholdedList.append(boundingBoxOfDetectedObject)

    # for boundingBoxOfDetectedObject in allBoundingBoxOfDetectedObjectsThresholdedList:
    #     if boundingBoxOfDetectedObject.boundingBox.confidence < confidenceThreshold:
    #         print(boundingBoxOfDetectedObject.boundingBox.className, boundingBoxOfDetectedObject.boundingBox.confidence)

    # # calculating all coordinates of bounding boxes according by original images
    # for boundingBoxOfDetectedObject in allBoundingBoxOfDetectedObjectsThresholdedList:
    #     boundingBoxOfDetectedObject.setCoordinatesInOriginalImage()

    # evaluating the bounding boxes to get the final bounding boxes
    validBoundingBoxesList = getFinalBoundingBoxes(allBoundingBoxOfDetectedObjectsThresholdedList)

    # evaluating and defining the bounding boxes of the detected objects
    for validBoundingBox in validBoundingBoxesList:
        # defining bounding box parameters
        # bgrColorBoundingBox = (0, 0, 255)
        bgrColorBoundingBox = getBoundingBoxColor(validBoundingBox.className)
        thicknessBoundingBox = 2
        inputImage = drawBoundingBox(inputImage,
                                     validBoundingBox,
                                     bgrColorBoundingBox,
                                     thicknessBoundingBox)

    # evaluating and defining the bounding boxes of the detected objects
    # for detectedObjectsCroppedImage in detectedObjectsCroppedImagesList:
    #     for detectedObjectBoundingBox in detectedObjectsCroppedImage.detectedObjectsBoundingBoxesList:
    #         # defining bounding box parameters
    #         # bgrColorBoundingBox = (0, 0, 255)
    #         bgrColorBoundingBox = getBoundingBoxColor(detectedObjectBoundingBox.className)
    #         thicknessBoundingBox = 2
    #         inputImage = drawBoundingBox(inputImage,
    #                                      detectedObjectsCroppedImage.croppedImageDetails,
    #                                      detectedObjectBoundingBox,
    #                                      bgrColorBoundingBox,
    #                                      thicknessBoundingBox)

    # saving the result image
    finalImageName = outputMergedImagesPath + inputImageName + '-final' + \
                     '-[confidence-' + str(confidenceThreshold) + '%]'
    saveResultImage(finalImageName, inputImage)


# ###########################################
# Methods of Level 3
# ###########################################

# get the bounding boxes of all detected objects of one the image
def getDetectedObjectsList(detectionLogFileName, imageName, confidenceThreshold):
    # defining the detected objects list
    detectedObjectsList = []

    # open log detection file
    detectionLogFile = open(detectionLogFileName, "r")

    # reading next line
    line = detectionLogFile.readline()

    # setting control
    foundBoundingBoxes = False

    # searching bounding boxes
    while line != '':

        # looking for image name (jpg)
        if not foundBoundingBoxes and (line.lower().find('jpg') == -1 and line.lower().find('jpeg') == -1):
            line = detectionLogFile.readline()
            continue

        # reading next line
        line = detectionLogFile.readline()

        # check if finished the search
        if line == '':
            break

        # setting found bounding boxes
        foundBoundingBoxes = True

        # adjusting string line
        line = line.replace('\t', ' ')
        line = line.replace('\t', ' ')
        line = line.replace('\t', ' ')
        line = line.replace('\t', ' ')
        line = line.replace('\n', ' ')
        line = line.replace('(', '')
        line = line.replace(')', '')
        line = line.replace('  ', ' ')
        line = line.replace('  ', ' ')
        line = line.replace('  ', ' ')
        line = line.replace('  ', ' ')
        line = line.replace('  ', ' ')
        line = line.replace('  ', ' ')
        line = line.replace('  ', ' ')
        line = line.replace('  ', ' ')
        line = line.replace('  ', ' ')
        line = line.replace('  ', ' ')
        line = line.replace('  ', ' ')

        # getting the array of values
        values = line.split(' ')

        # get fields of bounding box
        className = values[0].replace(':', '')
        className = className[2:]
        confidence = int(values[1].replace('%', ''))
        linP1 = int(values[5])
        colP1 = int(values[3])
        linP2 = linP1 + int(values[9])
        colP2 = colP1 + int(values[7])

        print(line)
        print('detected fields', className, confidence, linP1, colP1, linP2, colP2)

        # # evaluating the confidence
        # if confidence < confidenceThreshold:
        #     return []

        # creating a new bounding box instance
        detectedObjectBoundingBox = BoundingBox(linP1, colP1, linP2, colP2, className, confidence)

        # adding new item to the list
        detectedObjectsList.append(detectedObjectBoundingBox)

        # # reading next line
        # line = detectionLogFileName.readline()
        #
        # # check if finished the search
        # if line.find('net.optimized') != -1 or line == '':
        #     break

    # returning the detected objects list
    return detectedObjectsList


def getCroppedImageDetails(outputCroppedImagesMosaicPath, detectedCroppedImageName):
    # getting the details about cropped image
    imageDetailsFilename = outputCroppedImagesMosaicPath + detectedCroppedImageName + '-details.txt'
    with open(imageDetailsFilename) as json_file:
        # getting the json object
        imageDetails = json.load(json_file)

    # getting the json details
    croppedImagePath = imageDetails['croppedImagePath']
    originalImageName = imageDetails['originalImageName']
    originalImageHeight = int(imageDetails['originalImageHeight'])
    originalImageWidth = int(imageDetails['originalImageWidth'])
    croppedImageName = imageDetails['croppedImageName']
    sizeSquareImage = int(imageDetails['sizeSquareImage'])
    mosaicLin = int(imageDetails['mosaicLin'])
    mosaicCol = int(imageDetails['mosaicCol'])
    linP1 = int(imageDetails['linP1'])
    colP1 = int(imageDetails['colP1'])
    linP2 = int(imageDetails['linP2'])
    colP2 = int(imageDetails['colP2'])

    # creating a new cropped image detials instance
    croppedImageDetails = CroppedImageDetails(
        croppedImagePath,
        originalImageName,
        originalImageHeight,
        originalImageWidth,
        croppedImageName,
        sizeSquareImage,
        mosaicLin,
        mosaicCol,
        linP1,
        colP1,
        linP2,
        colP2
    )

    # return the cropped image details instance
    return croppedImageDetails


# define the color of bounding box to object class
def getBoundingBoxColor(className):
    blue = [255, 0, 0]
    green = [0, 255, 0]
    red = [0, 0, 255]
    yellow = [0, 255, 255]
    magenta = [255, 0, 255]
    cyan = [255, 255, 0]
    lilas = [127, 0, 63]

    if className == 'exuvia':
        return blue
    elif className == 'instar1':
        return green
    elif className == 'instar2':
        return red
    elif className == 'instar3':
        return magenta
    elif className == 'instar4':
        return cyan
    elif className == 'adulta':
        return yellow
    elif className == 'ovo':
        return lilas


# get the final bounding boxes
def getFinalBoundingBoxes(allBoundingBoxOfDetectedObjectsList):
    # initializing list of bounding boxes valid
    validBoundingBoxesList = []

    for boundingBoxOfDetectedObject in allBoundingBoxOfDetectedObjectsList:

        # evaluating if the item was processed
        if boundingBoxOfDetectedObject.processed:
            continue

        # if boundingBoxOfDetectedObject.croppedImageDetails.croppedImageName == 'P1040801-r005-c013-slidRight' \
        #         or boundingBoxOfDetectedObject.croppedImageDetails.croppedImageName == 'P1040801-r005-c014-hv' \
        #         or boundingBoxOfDetectedObject.croppedImageDetails.croppedImageName == 'P1040801-r005-c014-slidDown' \
        #         or boundingBoxOfDetectedObject.croppedImageDetails.croppedImageName == 'P1040801-r005-c014-slidRight':
        #     x = 0

        # getting all bouding boxes tha overlap the bounding box to process
        # overlappedBoundingBoxes = getOverlappedBoundingBoxes(allBoundingBoxOfDetectedObjectsList,
        #                                                      boundingBoxOfDetectedObject)
        # overlappedBoundingBoxes = getOverlappedBoundingBoxesByIntersectionOfStraights(
        #     allBoundingBoxOfDetectedObjectsList,
        #     boundingBoxOfDetectedObject)
        overlappedBoundingBoxes = getOverlappedBoundingBoxesBySeparatorAxis(
            allBoundingBoxOfDetectedObjectsList,
            boundingBoxOfDetectedObject)

        # setting current bounding box as processed
        boundingBoxOfDetectedObject.processed = True

        # adding the current bounding box into the list
        overlappedBoundingBoxes.append(boundingBoxOfDetectedObject)

        # creating a new bounding box instance
        bestBoundingBox = BoundingBox(boundingBoxOfDetectedObject.linPoint1InOriginalImage,
                                      boundingBoxOfDetectedObject.colPoint1InOriginalImage,
                                      boundingBoxOfDetectedObject.linPoint2InOriginalImage,
                                      boundingBoxOfDetectedObject.colPoint2InOriginalImage,
                                      boundingBoxOfDetectedObject.boundingBox.className,
                                      boundingBoxOfDetectedObject.boundingBox.confidence)

        # selecting the bounding box with the greater confidence value
        for overlappedBoundingBox in overlappedBoundingBoxes:
            if overlappedBoundingBox.boundingBox.confidence > bestBoundingBox.confidence:
                bestBoundingBox.className = overlappedBoundingBox.boundingBox.className
                bestBoundingBox.confidence = overlappedBoundingBox.boundingBox.confidence
                bestBoundingBox.linPoint1 = overlappedBoundingBox.linPoint1InOriginalImage
                bestBoundingBox.colPoint1 = overlappedBoundingBox.colPoint1InOriginalImage
                bestBoundingBox.linPoint2 = overlappedBoundingBox.linPoint2InOriginalImage
                bestBoundingBox.colPoint2 = overlappedBoundingBox.colPoint2InOriginalImage

        if boundingBoxOfDetectedObject.croppedImageDetails.croppedImageName == 'P1040801-r005-c016-slidRightDown' \
                or boundingBoxOfDetectedObject.croppedImageDetails.croppedImageName == 'P1040801-r005-c016-slidRightDown' \
                or boundingBoxOfDetectedObject.croppedImageDetails.croppedImageName == 'P1040801-r005-c017-slidDown':
            x = 0

        if len(overlappedBoundingBoxes) > 1:  # has overlapped bounding boxes

            for overlappedBoundingBox in overlappedBoundingBoxes:

                if bestBoundingBox.className == overlappedBoundingBox.boundingBox.className:

                    # evaluating the confidence of bounding box
                    # if overlappedBoundingBox.boundingBox.confidence > bestBoundingBox.confidence:
                    #     bestBoundingBox.confidence = overlappedBoundingBox.boundingBox.confidence

                    # evaluating the coordinates of bounding box
                    if overlappedBoundingBox.linPoint1InOriginalImage < bestBoundingBox.linPoint1:
                        bestBoundingBox.linPoint1 = overlappedBoundingBox.linPoint1InOriginalImage

                    if overlappedBoundingBox.colPoint1InOriginalImage < bestBoundingBox.colPoint1:
                        bestBoundingBox.colPoint1 = overlappedBoundingBox.colPoint1InOriginalImage

                    if overlappedBoundingBox.linPoint2InOriginalImage > bestBoundingBox.linPoint2:
                        bestBoundingBox.linPoint2 = overlappedBoundingBox.linPoint2InOriginalImage

                    if overlappedBoundingBox.colPoint2InOriginalImage > bestBoundingBox.colPoint2:
                        bestBoundingBox.colPoint2 = overlappedBoundingBox.colPoint2InOriginalImage

        # adding valid bound box
        validBoundingBoxesList.append(bestBoundingBox)

        # # setting the item processed
        # boundingBoxOfDetectedObject.processed = True

    # returning result
    return validBoundingBoxesList


def drawBoundingBox(inputImage, boundingBox, bgrColorBoundingBox, thicknessBoundingBox):
    # Start coordinate, here (5, 5)
    # represents the top left corner of rectangle
    # startPoint = (boundingBox.linPoint1, boundingBox.colPoint1)
    # startPoint = (linP1, colP1)
    startPoint = (boundingBox.colPoint1, boundingBox.linPoint1)

    # Ending coordinate, here (220, 220)
    # represents the bottom right corner of rectangle
    # endPoint = (boundingBox.linPoint2, boundingBox.colPoint2)
    # endPoint = (linP2, colP2)
    endPoint = (boundingBox.colPoint2, boundingBox.linPoint2)

    # Blue color in BGR
    color = bgrColorBoundingBox

    # Line thickness of 2 px
    thickness = thicknessBoundingBox

    # Using cv2.rectangle() method
    # Draw a rectangle with blue line borders of thickness of 2 px
    inputImage = cv2.rectangle(inputImage, startPoint, endPoint, color, thickness)

    # setting bounding box label with the class name and confidence
    label = boundingBox.className + ' (' + str(boundingBox.confidence) + '%)'
    cv2.putText(inputImage, label,
                (boundingBox.colPoint1, boundingBox.linPoint1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    # returning the image with bounding box draw
    return inputImage


# ###########################################
# Methods of Level 4
# ###########################################

# define the cropped name
def getCroppedImageName(inputImageName, mosaicLin, mosaicCol):
    # setting the name of cropped mosaic image
    mosaicLinName = '{:03d}'.format(mosaicLin)
    mosaicColName = '{:03d}'.format(mosaicCol)
    croppedImageName = inputImageName + '-r' + mosaicLinName + '-c' + mosaicColName
    return croppedImageName


# save the image
def saveResultImage(croppedImagePathAndImageName, resultImage):
    cv2.imwrite(croppedImagePathAndImageName + '.jpg', resultImage)
    print(croppedImagePathAndImageName)


# get all bounding boxes that overlapping
def getOverlappedBoundingBoxes(allBoundingBoxOfDetectedObjectsList, boundingBoxOfDetectedObject):
    # initializing objects
    overlappedBoundingBoxesOfDetectedObjectList = []

    # if boundingBoxOfDetectedObject.croppedImageDetails.croppedImageName == 'P1040801-r005-c016-slidRightDown' \
    #         or boundingBoxOfDetectedObject.croppedImageDetails.croppedImageName == 'P1040801-r005-c016-slidRightDown' \
    #         or boundingBoxOfDetectedObject.croppedImageDetails.croppedImageName == 'P1040801-r005-c017-slidDown':
    #     x = 0

    if boundingBoxOfDetectedObject.croppedImageDetails.croppedImageName == 'P1040801-r005-c016-slidRight':
        x = 0
    if boundingBoxOfDetectedObject.croppedImageDetails.croppedImageName == 'P1040801-r005-c016-slidRightDown':
        x = 0
    if boundingBoxOfDetectedObject.croppedImageDetails.croppedImageName == 'P1040801-r005-c017-slidDown':
        x = 0

    for itemBoundingBoxOfDetectedObject in allBoundingBoxOfDetectedObjectsList:

        # checking if the bounding box is the same
        if (
                boundingBoxOfDetectedObject.linPoint1InOriginalImage == itemBoundingBoxOfDetectedObject.linPoint1InOriginalImage
                and boundingBoxOfDetectedObject.colPoint1InOriginalImage == itemBoundingBoxOfDetectedObject.colPoint1InOriginalImage
                and boundingBoxOfDetectedObject.linPoint2InOriginalImage == itemBoundingBoxOfDetectedObject.linPoint2InOriginalImage
                and boundingBoxOfDetectedObject.colPoint2InOriginalImage == itemBoundingBoxOfDetectedObject.colPoint2InOriginalImage
        ):
            continue

        # # checking if the classes are the same
        # if not boundingBoxOfDetectedObject.boundingBox.className == itemBoundingBoxOfDetectedObject.boundingBox.className:
        #     continue

        # setting the size of image crop error (pixel) to be consider in the checking
        imageCropError = 2

        # ########################################################################
        # checking if the first bounding box is overlapping into the second
        # ########################################################################
        # point 1
        if checkPointBelongsToBoundingBox(boundingBoxOfDetectedObject.linPoint1InOriginalImage,
                                          boundingBoxOfDetectedObject.colPoint1InOriginalImage,
                                          itemBoundingBoxOfDetectedObject.linPoint1InOriginalImage,
                                          itemBoundingBoxOfDetectedObject.colPoint1InOriginalImage,
                                          itemBoundingBoxOfDetectedObject.linPoint2InOriginalImage,
                                          itemBoundingBoxOfDetectedObject.colPoint2InOriginalImage,
                                          imageCropError):
            itemBoundingBoxOfDetectedObject.processed = True
            overlappedBoundingBoxesOfDetectedObjectList.append(itemBoundingBoxOfDetectedObject)
            continue

        # point 2
        if checkPointBelongsToBoundingBox(boundingBoxOfDetectedObject.linPoint1InOriginalImage,
                                          boundingBoxOfDetectedObject.colPoint2InOriginalImage,
                                          itemBoundingBoxOfDetectedObject.linPoint1InOriginalImage,
                                          itemBoundingBoxOfDetectedObject.colPoint1InOriginalImage,
                                          itemBoundingBoxOfDetectedObject.linPoint2InOriginalImage,
                                          itemBoundingBoxOfDetectedObject.colPoint2InOriginalImage,
                                          imageCropError):
            itemBoundingBoxOfDetectedObject.processed = True
            overlappedBoundingBoxesOfDetectedObjectList.append(itemBoundingBoxOfDetectedObject)
            continue

        # point 3
        if checkPointBelongsToBoundingBox(boundingBoxOfDetectedObject.linPoint2InOriginalImage,
                                          boundingBoxOfDetectedObject.colPoint1InOriginalImage,
                                          itemBoundingBoxOfDetectedObject.linPoint1InOriginalImage,
                                          itemBoundingBoxOfDetectedObject.colPoint1InOriginalImage,
                                          itemBoundingBoxOfDetectedObject.linPoint2InOriginalImage,
                                          itemBoundingBoxOfDetectedObject.colPoint2InOriginalImage,
                                          imageCropError):
            itemBoundingBoxOfDetectedObject.processed = True
            overlappedBoundingBoxesOfDetectedObjectList.append(itemBoundingBoxOfDetectedObject)
            continue

        # point 4
        if checkPointBelongsToBoundingBox(boundingBoxOfDetectedObject.linPoint2InOriginalImage,
                                          boundingBoxOfDetectedObject.colPoint2InOriginalImage,
                                          itemBoundingBoxOfDetectedObject.linPoint1InOriginalImage,
                                          itemBoundingBoxOfDetectedObject.colPoint1InOriginalImage,
                                          itemBoundingBoxOfDetectedObject.linPoint2InOriginalImage,
                                          itemBoundingBoxOfDetectedObject.colPoint2InOriginalImage,
                                          imageCropError):
            itemBoundingBoxOfDetectedObject.processed = True
            overlappedBoundingBoxesOfDetectedObjectList.append(itemBoundingBoxOfDetectedObject)
            continue

        # ########################################################################
        # checking if the second bounding box is overlapping into the first
        # ########################################################################
        # point 4
        if checkPointBelongsToBoundingBox(itemBoundingBoxOfDetectedObject.linPoint1InOriginalImage,
                                          itemBoundingBoxOfDetectedObject.colPoint1InOriginalImage,
                                          boundingBoxOfDetectedObject.linPoint1InOriginalImage,
                                          boundingBoxOfDetectedObject.colPoint1InOriginalImage,
                                          boundingBoxOfDetectedObject.linPoint2InOriginalImage,
                                          boundingBoxOfDetectedObject.colPoint2InOriginalImage,
                                          imageCropError):
            itemBoundingBoxOfDetectedObject.processed = True
            overlappedBoundingBoxesOfDetectedObjectList.append(itemBoundingBoxOfDetectedObject)
            continue

        # point 5
        if checkPointBelongsToBoundingBox(itemBoundingBoxOfDetectedObject.linPoint1InOriginalImage,
                                          itemBoundingBoxOfDetectedObject.colPoint2InOriginalImage,
                                          boundingBoxOfDetectedObject.linPoint1InOriginalImage,
                                          boundingBoxOfDetectedObject.colPoint1InOriginalImage,
                                          boundingBoxOfDetectedObject.linPoint2InOriginalImage,
                                          boundingBoxOfDetectedObject.colPoint2InOriginalImage,
                                          imageCropError):
            itemBoundingBoxOfDetectedObject.processed = True
            overlappedBoundingBoxesOfDetectedObjectList.append(itemBoundingBoxOfDetectedObject)
            continue

        # point 6
        if checkPointBelongsToBoundingBox(itemBoundingBoxOfDetectedObject.linPoint2InOriginalImage,
                                          itemBoundingBoxOfDetectedObject.colPoint1InOriginalImage,
                                          boundingBoxOfDetectedObject.linPoint1InOriginalImage,
                                          boundingBoxOfDetectedObject.colPoint1InOriginalImage,
                                          boundingBoxOfDetectedObject.linPoint2InOriginalImage,
                                          boundingBoxOfDetectedObject.colPoint2InOriginalImage,
                                          imageCropError):
            itemBoundingBoxOfDetectedObject.processed = True
            overlappedBoundingBoxesOfDetectedObjectList.append(itemBoundingBoxOfDetectedObject)
            continue

        # point 7
        if checkPointBelongsToBoundingBox(itemBoundingBoxOfDetectedObject.linPoint2InOriginalImage,
                                          itemBoundingBoxOfDetectedObject.colPoint2InOriginalImage,
                                          boundingBoxOfDetectedObject.linPoint1InOriginalImage,
                                          boundingBoxOfDetectedObject.colPoint1InOriginalImage,
                                          boundingBoxOfDetectedObject.linPoint2InOriginalImage,
                                          boundingBoxOfDetectedObject.colPoint2InOriginalImage,
                                          imageCropError):
            itemBoundingBoxOfDetectedObject.processed = True
            overlappedBoundingBoxesOfDetectedObjectList.append(itemBoundingBoxOfDetectedObject)
            continue

    # checking if all bounding boxes are the same class of the bounding box required
    # x = 0
    # for overlappedBoundingBoxOfDetectedObject in overlappedBoundingBoxesOfDetectedObjectList:
    #     if boundingBoxOfDetectedObject.boundingBox.className != overlappedBoundingBoxOfDetectedObject.boundingBox.className:
    #         x = 0

    # if len(overlappedBoundingBoxesOfDetectedObjectList) > 0:
    #     x = 0

    if boundingBoxOfDetectedObject.croppedImageDetails.croppedImageName == 'P1040801-r005-c016-slidRight':
        x = 0
    if boundingBoxOfDetectedObject.croppedImageDetails.croppedImageName == 'P1040801-r005-c016-slidRightDown':
        x = 0
    if boundingBoxOfDetectedObject.croppedImageDetails.croppedImageName == 'P1040801-r005-c017-slidDown':
        x = 0

    # returning the overlapped bouding boxes
    return overlappedBoundingBoxesOfDetectedObjectList


# get all bounding boxes that overlapping by lines
def getOverlappedBoundingBoxesByIntersectionOfStraights(allBoundingBoxOfDetectedObjectsList,
                                                        boundingBoxOfDetectedObject):
    # initializing objects
    overlappedBoundingBoxesOfDetectedObjectList = []

    # if boundingBoxOfDetectedObject.croppedImageDetails.croppedImageName == 'P1040801-r005-c016-slidRightDown' \
    #         or boundingBoxOfDetectedObject.croppedImageDetails.croppedImageName == 'P1040801-r005-c016-slidRightDown' \
    #         or boundingBoxOfDetectedObject.croppedImageDetails.croppedImageName == 'P1040801-r005-c017-slidDown':
    #     x = 0

    if boundingBoxOfDetectedObject.croppedImageDetails.croppedImageName == 'P1040801-r005-c016-slidRight':
        x = 0
    if boundingBoxOfDetectedObject.croppedImageDetails.croppedImageName == 'P1040801-r005-c016-slidRightDown':
        x = 0
    if boundingBoxOfDetectedObject.croppedImageDetails.croppedImageName == 'P1040801-r005-c017-slidDown':
        x = 0

    for itemBoundingBoxOfDetectedObject in allBoundingBoxOfDetectedObjectsList:

        # checking if the bounding box is the same
        if (
                boundingBoxOfDetectedObject.linPoint1InOriginalImage == itemBoundingBoxOfDetectedObject.linPoint1InOriginalImage
                and boundingBoxOfDetectedObject.colPoint1InOriginalImage == itemBoundingBoxOfDetectedObject.colPoint1InOriginalImage
                and boundingBoxOfDetectedObject.linPoint2InOriginalImage == itemBoundingBoxOfDetectedObject.linPoint2InOriginalImage
                and boundingBoxOfDetectedObject.colPoint2InOriginalImage == itemBoundingBoxOfDetectedObject.colPoint2InOriginalImage
        ):
            continue

        # ########################################################################
        # checking intersection using the side lines
        # ########################################################################

        # Intesection 1
        if checkByIntersectionOfLines(boundingBoxOfDetectedObject.linPoint1InOriginalImage,
                                      boundingBoxOfDetectedObject.colPoint1InOriginalImage,
                                      boundingBoxOfDetectedObject.linPoint2InOriginalImage,
                                      boundingBoxOfDetectedObject.colPoint1InOriginalImage,
                                      itemBoundingBoxOfDetectedObject.linPoint1InOriginalImage,
                                      itemBoundingBoxOfDetectedObject.colPoint1InOriginalImage,
                                      itemBoundingBoxOfDetectedObject.linPoint1InOriginalImage,
                                      itemBoundingBoxOfDetectedObject.colPoint2InOriginalImage):
            itemBoundingBoxOfDetectedObject.processed = True
            overlappedBoundingBoxesOfDetectedObjectList.append(itemBoundingBoxOfDetectedObject)
            continue

        # Intesection 2
        if checkByIntersectionOfLines(boundingBoxOfDetectedObject.linPoint1InOriginalImage,
                                      boundingBoxOfDetectedObject.colPoint1InOriginalImage,
                                      boundingBoxOfDetectedObject.linPoint2InOriginalImage,
                                      boundingBoxOfDetectedObject.colPoint1InOriginalImage,
                                      itemBoundingBoxOfDetectedObject.linPoint2InOriginalImage,
                                      itemBoundingBoxOfDetectedObject.colPoint1InOriginalImage,
                                      itemBoundingBoxOfDetectedObject.linPoint2InOriginalImage,
                                      itemBoundingBoxOfDetectedObject.colPoint2InOriginalImage):
            itemBoundingBoxOfDetectedObject.processed = True
            overlappedBoundingBoxesOfDetectedObjectList.append(itemBoundingBoxOfDetectedObject)
            continue

        # Intesection 3
        if checkByIntersectionOfLines(boundingBoxOfDetectedObject.linPoint1InOriginalImage,
                                      boundingBoxOfDetectedObject.colPoint2InOriginalImage,
                                      boundingBoxOfDetectedObject.linPoint2InOriginalImage,
                                      boundingBoxOfDetectedObject.colPoint2InOriginalImage,
                                      itemBoundingBoxOfDetectedObject.linPoint1InOriginalImage,
                                      itemBoundingBoxOfDetectedObject.colPoint1InOriginalImage,
                                      itemBoundingBoxOfDetectedObject.linPoint1InOriginalImage,
                                      itemBoundingBoxOfDetectedObject.colPoint2InOriginalImage):
            itemBoundingBoxOfDetectedObject.processed = True
            overlappedBoundingBoxesOfDetectedObjectList.append(itemBoundingBoxOfDetectedObject)
            continue

        # Intesection 4
        if checkByIntersectionOfLines(boundingBoxOfDetectedObject.linPoint1InOriginalImage,
                                      boundingBoxOfDetectedObject.colPoint2InOriginalImage,
                                      boundingBoxOfDetectedObject.linPoint2InOriginalImage,
                                      boundingBoxOfDetectedObject.colPoint2InOriginalImage,
                                      itemBoundingBoxOfDetectedObject.linPoint2InOriginalImage,
                                      itemBoundingBoxOfDetectedObject.colPoint1InOriginalImage,
                                      itemBoundingBoxOfDetectedObject.linPoint2InOriginalImage,
                                      itemBoundingBoxOfDetectedObject.colPoint2InOriginalImage):
            itemBoundingBoxOfDetectedObject.processed = True
            overlappedBoundingBoxesOfDetectedObjectList.append(itemBoundingBoxOfDetectedObject)
            continue

        # Intesection 5
        if checkByIntersectionOfLines(boundingBoxOfDetectedObject.linPoint1InOriginalImage,
                                      boundingBoxOfDetectedObject.colPoint1InOriginalImage,
                                      boundingBoxOfDetectedObject.linPoint1InOriginalImage,
                                      boundingBoxOfDetectedObject.colPoint2InOriginalImage,
                                      itemBoundingBoxOfDetectedObject.linPoint1InOriginalImage,
                                      itemBoundingBoxOfDetectedObject.colPoint2InOriginalImage,
                                      itemBoundingBoxOfDetectedObject.linPoint2InOriginalImage,
                                      itemBoundingBoxOfDetectedObject.colPoint2InOriginalImage):
            itemBoundingBoxOfDetectedObject.processed = True
            overlappedBoundingBoxesOfDetectedObjectList.append(itemBoundingBoxOfDetectedObject)
            continue

        # Intesection 6
        if checkByIntersectionOfLines(boundingBoxOfDetectedObject.linPoint1InOriginalImage,
                                      boundingBoxOfDetectedObject.colPoint1InOriginalImage,
                                      boundingBoxOfDetectedObject.linPoint1InOriginalImage,
                                      boundingBoxOfDetectedObject.colPoint2InOriginalImage,
                                      itemBoundingBoxOfDetectedObject.linPoint1InOriginalImage,
                                      itemBoundingBoxOfDetectedObject.colPoint1InOriginalImage,
                                      itemBoundingBoxOfDetectedObject.linPoint2InOriginalImage,
                                      itemBoundingBoxOfDetectedObject.colPoint1InOriginalImage):
            itemBoundingBoxOfDetectedObject.processed = True
            overlappedBoundingBoxesOfDetectedObjectList.append(itemBoundingBoxOfDetectedObject)
            continue

        # Intesection 7
        if checkByIntersectionOfLines(boundingBoxOfDetectedObject.linPoint2InOriginalImage,
                                      boundingBoxOfDetectedObject.colPoint1InOriginalImage,
                                      boundingBoxOfDetectedObject.linPoint2InOriginalImage,
                                      boundingBoxOfDetectedObject.colPoint2InOriginalImage,
                                      itemBoundingBoxOfDetectedObject.linPoint1InOriginalImage,
                                      itemBoundingBoxOfDetectedObject.colPoint2InOriginalImage,
                                      itemBoundingBoxOfDetectedObject.linPoint2InOriginalImage,
                                      itemBoundingBoxOfDetectedObject.colPoint2InOriginalImage):
            itemBoundingBoxOfDetectedObject.processed = True
            overlappedBoundingBoxesOfDetectedObjectList.append(itemBoundingBoxOfDetectedObject)
            continue

        # Intesection 8
        if checkByIntersectionOfLines(boundingBoxOfDetectedObject.linPoint2InOriginalImage,
                                      boundingBoxOfDetectedObject.colPoint1InOriginalImage,
                                      boundingBoxOfDetectedObject.linPoint2InOriginalImage,
                                      boundingBoxOfDetectedObject.colPoint2InOriginalImage,
                                      itemBoundingBoxOfDetectedObject.linPoint1InOriginalImage,
                                      itemBoundingBoxOfDetectedObject.colPoint1InOriginalImage,
                                      itemBoundingBoxOfDetectedObject.linPoint2InOriginalImage,
                                      itemBoundingBoxOfDetectedObject.colPoint1InOriginalImage):
            itemBoundingBoxOfDetectedObject.processed = True
            overlappedBoundingBoxesOfDetectedObjectList.append(itemBoundingBoxOfDetectedObject)
            continue

    if boundingBoxOfDetectedObject.croppedImageDetails.croppedImageName == 'P1040801-r005-c016-slidRight':
        x = 0
    if boundingBoxOfDetectedObject.croppedImageDetails.croppedImageName == 'P1040801-r005-c016-slidRightDown':
        x = 0
    if boundingBoxOfDetectedObject.croppedImageDetails.croppedImageName == 'P1040801-r005-c017-slidDown':
        x = 0

    # returning the overlapped bouding boxes
    return overlappedBoundingBoxesOfDetectedObjectList


# get all bounding boxes that overlapping by lines
def getOverlappedBoundingBoxesBySeparatorAxis(allBoundingBoxOfDetectedObjectsList, boundingBoxOfDetectedObject):
    # initializing objects
    overlappedBoundingBoxesOfDetectedObjectList = []

    # setting the size of image crop error (pixel) to be consider in the checking
    imageCropError = 2

    # if boundingBoxOfDetectedObject.croppedImageDetails.croppedImageName == 'P1040801-r005-c016-slidRightDown' \
    #         or boundingBoxOfDetectedObject.croppedImageDetails.croppedImageName == 'P1040801-r005-c016-slidRightDown' \
    #         or boundingBoxOfDetectedObject.croppedImageDetails.croppedImageName == 'P1040801-r005-c017-slidDown':
    #     x = 0

    # if boundingBoxOfDetectedObject.croppedImageDetails.croppedImageName == 'P1040801-r005-c016-slidRight':
    #     x = 0
    # if boundingBoxOfDetectedObject.croppedImageDetails.croppedImageName == 'P1040801-r005-c016-slidRightDown':
    #     x = 0
    # if boundingBoxOfDetectedObject.croppedImageDetails.croppedImageName == 'P1040801-r005-c017-slidDown':
    #     x = 0

    for itemBoundingBoxOfDetectedObject in allBoundingBoxOfDetectedObjectsList:

        # checking if the bounding box is the same
        if (
                boundingBoxOfDetectedObject.linPoint1InOriginalImage == itemBoundingBoxOfDetectedObject.linPoint1InOriginalImage
                and boundingBoxOfDetectedObject.colPoint1InOriginalImage == itemBoundingBoxOfDetectedObject.colPoint1InOriginalImage
                and boundingBoxOfDetectedObject.linPoint2InOriginalImage == itemBoundingBoxOfDetectedObject.linPoint2InOriginalImage
                and boundingBoxOfDetectedObject.colPoint2InOriginalImage == itemBoundingBoxOfDetectedObject.colPoint2InOriginalImage
        ):
            continue

        # process only bounding box of same class
        if boundingBoxOfDetectedObject.boundingBox.className != itemBoundingBoxOfDetectedObject.boundingBox.className:
            continue

        if checkBySeparatorAxis(boundingBoxOfDetectedObject.linPoint1InOriginalImage,
                                boundingBoxOfDetectedObject.colPoint1InOriginalImage,
                                boundingBoxOfDetectedObject.linPoint2InOriginalImage,
                                boundingBoxOfDetectedObject.colPoint2InOriginalImage,
                                itemBoundingBoxOfDetectedObject.linPoint1InOriginalImage,
                                itemBoundingBoxOfDetectedObject.colPoint1InOriginalImage,
                                itemBoundingBoxOfDetectedObject.linPoint2InOriginalImage,
                                itemBoundingBoxOfDetectedObject.colPoint2InOriginalImage,
                                imageCropError):
            itemBoundingBoxOfDetectedObject.processed = True
            overlappedBoundingBoxesOfDetectedObjectList.append(itemBoundingBoxOfDetectedObject)
            continue

    if boundingBoxOfDetectedObject.croppedImageDetails.croppedImageName == 'P1040801-r005-c016-slidRight':
        x = 0
    if boundingBoxOfDetectedObject.croppedImageDetails.croppedImageName == 'P1040801-r005-c016-slidRightDown':
        x = 0
    if boundingBoxOfDetectedObject.croppedImageDetails.croppedImageName == 'P1040801-r005-c017-slidDown':
        x = 0

    # returning the overlapped bouding boxes
    return overlappedBoundingBoxesOfDetectedObjectList


# ###########################################
# Methods of Level 4
# ###########################################


def checkPointBelongsToBoundingBox(linPointToEvaluate, colPointToEvaluate,
                                   linPoint1OfBoundingBox, colPoint1OfBoundingBox,
                                   linPoint2OfBoundingBox, colPoint2OfBoundingBox, cropError):
    # checking if the vertex point belongs to the bounding box
    if (linPoint1OfBoundingBox - cropError) <= linPointToEvaluate <= (linPoint2OfBoundingBox + cropError) and \
            (colPoint1OfBoundingBox - cropError) <= colPointToEvaluate <= (colPoint2OfBoundingBox + cropError):
        return True

    # return the point (lin, col) does not belong to the bounding box
    return False


def checkByIntersectionOfLines(linStartLine1, colStartLine1, linEndLine1, colEndLine1,
                               linStartLine2, colStartLine2, linEndLine2, colEndLine2):
    #  calculating if exists an intersection between the two lines
    result = (colEndLine2 - colStartLine2) * (linEndLine1 - linStartLine1) - \
             (linEndLine2 - linStartLine2) * (colEndLine1 - colStartLine1)

    # evaluating the result
    if result == 0.0:
        # there is an intersection between the two lines
        return False

    # there is not an intersection between the two lines
    return True


def checkBySeparatorAxis(linStart1, colStart1, linEnd1, colEnd1, linStart2, colStart2, linEnd2, colEnd2,
                         imageCropError):
    # initializing partial results
    overlapVertical = False
    overlapHorizontal = False

    # adjusting the coordinates using the image crop error
    linStart1 -= imageCropError
    colStart1 -= imageCropError
    linEnd1 += imageCropError
    colEnd1 += imageCropError
    linStart2 -= imageCropError
    colStart2 -= imageCropError
    linEnd2 += imageCropError
    colEnd2 += imageCropError

    # evaluating
    if linStart1 <= linStart2 <= linEnd1 or \
            linStart2 <= linEnd1 <= linEnd2:
        overlapVertical = True

    if colStart2 <= colStart1 <= colEnd2 or \
            colStart1 <= colStart2 <= colEnd1 or \
            colStart2 <= colEnd1 <= colEnd2:
        overlapHorizontal = True

    if linStart2 <= linStart1 <= linEnd2 or \
            linStart1 <= linEnd2 <= linEnd1 or \
            linStart2 <= linEnd1 <= linEnd2:
        overlapVertical = True

    if colStart1 <= colStart2 <= colEnd1 or \
            colStart2 <= colEnd1 <= colEnd2:
        overlapHorizontal = True

    # calculating the final result
    result = overlapVertical and overlapHorizontal

    # return the resul
    return result


# ###########################################
# Main method
# ###########################################
if __name__ == '__main__':
    INPUT_ORIGINAL_IMAGES_PATH = \
        'E:/desenvolvimento/projetos/DoctoralProjects/ImageMosaicProjectImages/01. input original images/'
    OUTPUT_CROPPED_IMAGES_MOSAIC_PATH = \
        'E:/desenvolvimento/projetos/DoctoralProjects/ImageMosaicProjectImages/02. output cropped images mosaic/'
    INPUT_DETECTED_CROPPED_IMAGES_PATH = \
        'E:/desenvolvimento/projetos/DoctoralProjects/ImageMosaicProjectImages/03. input detected cropped images/'
    OUTPUT_MERGED_IMAGES_PATH = \
        'E:/desenvolvimento/projetos/DoctoralProjects/ImageMosaicProjectImages/04. output merged images/'

    # setting the size square image to crop with a fixed size (height and width) used in the YOLOv4
    sizeSquareImage = 128

    # the confidence parameters expressed in percent (%)
    initialConfidenceThreshold = 30
    finalConfidenceThreshold = 90
    stepConfidenceThreshold = 10

    print('Detection post-processing')
    print('---------------------------')
    print('')
    print('Input images path    : ', INPUT_ORIGINAL_IMAGES_PATH)
    print('Mosaic images path  : ', OUTPUT_CROPPED_IMAGES_MOSAIC_PATH)
    print('')

    for confidenceThreshold in range(initialConfidenceThreshold,
                                     finalConfidenceThreshold + stepConfidenceThreshold,
                                     stepConfidenceThreshold):
        # processing the annotated images
        processInputImages(INPUT_ORIGINAL_IMAGES_PATH, OUTPUT_CROPPED_IMAGES_MOSAIC_PATH,
                           INPUT_DETECTED_CROPPED_IMAGES_PATH, OUTPUT_MERGED_IMAGES_PATH,
                           sizeSquareImage, confidenceThreshold)

    # end of processing
    print('End of processing')
