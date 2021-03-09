"""
Project: Merge a mosaic of images from images of any size.
Author: Rubens de Castro Pereira
Advisor: Dibio Leandro Borges
Date: 18/02/2021
Version: 1.0.0
"""

# Importing needed libraries
import os
# import math
import json
import cv2
import pathlib
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
def processInputImages(inputOriginalImagesPath, outputCroppedImagesMosaicPath, inputDetectedCroppedImagesPath,
                       outputMergedImagesPath, sizeSquareImage):
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
        mergeImagesMosaic(inputImage, inputImageName, sizeSquareImage, outputCroppedImagesMosaicPath,
                          inputDetectedCroppedImagesPath, outputMergedImagesPath)

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
def mergeImagesMosaic(inputImage, inputImageName, sizeSquareImage, outputCroppedImagesMosaicPath,
                      inputDetectedCroppedImagesPath, outputMergedImagesPath):
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

        # reading cropped image
        detectedCroppedImage = cv2.imread(inputDetectedCroppedImagesPath + detectedCroppedImageNameJpg)

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

        # merging detected cropped image
        inputImage[linP1:linP2, colP1:colP2] = detectedCroppedImage

        x = 0

    # saving the result image
    saveCroppedImage(outputMergedImagesPath + inputImageName, inputImage)


# ###########################################
# Methods of Level 3
# ###########################################

# crops the image
# def cropImage(inputImage, inputImageName, outputCroppedImagesMosaicPath, sizeSquareImage, mosaicLin, mosaicCol):
#     # getting the image shape
#     imageHeight, imageWidth, imageChannel = inputImage.shape
#
#     # setting the name of cropped mosaic image
#     croppedImageName = getCroppedImageName(inputImageName, mosaicLin, mosaicCol)
#     croppedImagePathAndImageName = outputCroppedImagesMosaicPath + croppedImageName
#     # print(mosaicLinName, mosaicColName, inputImageName, croppedImageName)
#
#     # defining the two points of the cropped image
#     linP1 = (mosaicLin - 1) * sizeSquareImage
#     colP1 = (mosaicCol - 1) * sizeSquareImage
#     linP2 = mosaicLin * sizeSquareImage
#     colP2 = mosaicCol * sizeSquareImage
#
#     # checking the image boundaries
#     if (colP2 > imageWidth):
#         colP2 = imageWidth
#         colP1 = colP2 - sizeSquareImage
#
#     if (linP2 > imageHeight):
#         linP2 = imageHeight
#         linP1 = linP2 - sizeSquareImage
#
#     # cropping and saving bounding box in new image
#     croppedImage = inputImage[linP1:linP2, colP1:colP2]
#     croppedImageWidth = linP2 - linP1
#     croppedImageHeight = colP2 - colP1
#
#     # saving the cropped image
#     saveCroppedImage(croppedImagePathAndImageName, croppedImage)
#
#     # saving the cropped image details
#     saveCroppedImageDetailsFile(outputCroppedImagesMosaicPath, inputImageName, imageHeight, imageWidth,
#                                 sizeSquareImage, mosaicLin, mosaicCol, linP1, colP1, linP2, colP2
#                                 )


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


# save the cropped image
def saveCroppedImage(croppedImagePathAndImageName, croppedImage):
    # croppedImageName = croppedImagePathAndImageName
    cv2.imwrite(croppedImagePathAndImageName + '.jpg', croppedImage)
    print(croppedImagePathAndImageName)


# save the details of cropped image
# def saveCroppedImageDetailsFile(outputCroppedImagesMosaicPath, originalImageName, originalImageHeight,
#                                 originalImageWidth,
#                                 sizeSquareImage, mosaicLin, mosaicCol, linP1, colP1, linP2, colP2
#                                 ):
#     # setting annotation file
#     croppedImageName = getCroppedImageName(originalImageName, mosaicLin, mosaicCol)
#     croppedImagePathAndImageName = outputCroppedImagesMosaicPath + croppedImageName + '-details.txt'
#
#     # setting the details in JSON format
#     croppedImageDetails = {
#         'croppedImagePath': str(outputCroppedImagesMosaicPath),
#         'originalImageName': str(originalImageName),
#         'originalImageHeight': str(originalImageHeight),
#         'originalImageWidth': str(originalImageWidth),
#         'croppedImageName': str(croppedImageName),
#         'sizeSquareImage': str(sizeSquareImage),
#         'mosaicLin': str(mosaicLin),
#         'mosaicCol': str(mosaicCol),
#         'linP1': str(linP1),
#         'colP1': str(colP1),
#         'linP2': str(linP2),
#         'colP2': str(colP2)
#     }
#
#     # writing details file
#     with open(croppedImagePathAndImageName, 'w') as json_file:
#         json.dump(croppedImageDetails, json_file)


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

    print('Merge Images Mosaic')
    print('---------------------------------')
    print('')
    print('Input images path    : ', INPUT_ORIGINAL_IMAGES_PATH)
    print('Mosaic images path  : ', OUTPUT_CROPPED_IMAGES_MOSAIC_PATH)
    print('')

    # setting the size square image to crop with a fixed size (height and width) used in the YOLOv4
    sizeSquareImage = 128

    # processing the annotated images
    processInputImages(INPUT_ORIGINAL_IMAGES_PATH, OUTPUT_CROPPED_IMAGES_MOSAIC_PATH,
                       INPUT_DETECTED_CROPPED_IMAGES_PATH, OUTPUT_MERGED_IMAGES_PATH, sizeSquareImage)

    # end of processing
    print('End of processing')
