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

    # get image shape
    imageHeight, imageWidth, imageChannel = inputImage.shape

    # calculating number of mosaic
    # numberOfMosaicLines = math.ceil(imageHeight / sizeSquareImage)
    # numberOfMosaicColuns = math.ceil(imageWidth / sizeSquareImage)

    # getting all detected cropped images according by original image
    detectedCroppedImages = list(pathlib.Path(inputDetectedCroppedImagesPath).glob(inputImageName + '*.jpg'))

    # updating each detected cropped image in original image
    # for fileName in os.listdir(detectedCroppedImages):
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

    # evaluating and defining the bounding boxes of the detected objects
    for detectedObjectsCroppedImage in detectedObjectsCroppedImagesList:
        for detectedObjectBoundingBox in detectedObjectsCroppedImage.detectedObjectsBoundingBoxesList:
            # defining bounding box parameters
            # bgrColorBoundingBox = (0, 0, 255)
            bgrColorBoundingBox = getBoundingBoxColor(detectedObjectBoundingBox.className)
            thicknessBoundingBox = 2
            inputImage = drawBoundingBox(inputImage,
                                         detectedObjectsCroppedImage.croppedImageDetails,
                                         detectedObjectBoundingBox,
                                         bgrColorBoundingBox,
                                         thicknessBoundingBox)

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

        # evaluating the confidence
        if confidence < confidenceThreshold:
            return []

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


def drawBoundingBox(inputImage, croppedImageDetails, boundingBox, bgrColorBoundingBox, thicknessBoundingBox):
    #  calculating the final coordinates of the bounding box in the original image
    linP1 = croppedImageDetails.linP1 + boundingBox.linPoint1
    colP1 = croppedImageDetails.colP1 + boundingBox.colPoint1
    linP2 = croppedImageDetails.linP1 + boundingBox.linPoint2
    colP2 = croppedImageDetails.colP1 + boundingBox.colPoint2

    # Start coordinate, here (5, 5)
    # represents the top left corner of rectangle
    # startPoint = (boundingBox.linPoint1, boundingBox.colPoint1)
    # startPoint = (linP1, colP1)
    startPoint = (colP1, linP1)

    # Ending coordinate, here (220, 220)
    # represents the bottom right corner of rectangle
    # endPoint = (boundingBox.linPoint2, boundingBox.colPoint2)
    # endPoint = (linP2, colP2)
    endPoint = (colP2, linP2)

    # Blue color in BGR
    color = bgrColorBoundingBox

    # Line thickness of 2 px
    thickness = thicknessBoundingBox

    # Using cv2.rectangle() method
    # Draw a rectangle with blue line borders of thickness of 2 px
    inputImage = cv2.rectangle(inputImage, startPoint, endPoint, color, thickness)

    # setting bounding box label with the class name and confidence
    label = boundingBox.className + ' (' + str(boundingBox.confidence) + '%)'
    cv2.putText(inputImage, label, (colP1, linP1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

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

    # the confidence expressed in percent (%)
    confidenceThreshold = 30

    print('Merge Images Mosaic')
    print('---------------------------------')
    print('')
    print('Input images path    : ', INPUT_ORIGINAL_IMAGES_PATH)
    print('Mosaic images path  : ', OUTPUT_CROPPED_IMAGES_MOSAIC_PATH)
    print('')

    # processing the annotated images
    processInputImages(INPUT_ORIGINAL_IMAGES_PATH, OUTPUT_CROPPED_IMAGES_MOSAIC_PATH,
                       INPUT_DETECTED_CROPPED_IMAGES_PATH, OUTPUT_MERGED_IMAGES_PATH,
                       sizeSquareImage, confidenceThreshold)

    # end of processing
    print('End of processing')
