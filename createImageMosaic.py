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

        # create the mosaic of images
        cropImagesMosaic(inputImage, inputImageName, sizeSquareImage, outputCroppedImagesMosaicPath)

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
def cropImagesMosaic(inputImage, inputImageName, sizeSquareImage, outputCroppedImagesMosaicPath):
    # get image shape
    imageHeight, imageWidth, imageChannel = inputImage.shape

    # calculating number of mosaic
    numberOfMosaicLines = math.ceil(imageHeight / sizeSquareImage)
    numberOfMosaicColuns = math.ceil(imageWidth / sizeSquareImage)

    # cropping images in the horizontal and vertical bands
    for mosaicLin in range(1, numberOfMosaicLines + 1):
        for mosaicCol in range(1, numberOfMosaicColuns + 1):
            # cropping mosaic image
            cropHorizontalVerticalImage(inputImage, inputImageName, outputCroppedImagesMosaicPath, sizeSquareImage,
                                        mosaicLin, mosaicCol)

    # cropping images in the right sliding
    for mosaicLin in range(1, numberOfMosaicLines - 1):
        for mosaicCol in range(1, numberOfMosaicColuns - 1):
            # cropping mosaic image
            cropRightSlidingImage(inputImage, inputImageName, outputCroppedImagesMosaicPath, sizeSquareImage,
                                  mosaicLin, mosaicCol)

    # cropping images in the down sliding
    for mosaicLin in range(1, numberOfMosaicLines - 1):
        for mosaicCol in range(1, numberOfMosaicColuns - 1):
            # cropping mosaic image
            cropDownSlidingImage(inputImage, inputImageName, outputCroppedImagesMosaicPath, sizeSquareImage,
                                 mosaicLin, mosaicCol)

    # cropping images in the right and down sliding
    for mosaicLin in range(1, numberOfMosaicLines - 1):
        for mosaicCol in range(1, numberOfMosaicColuns - 1):
            # cropping mosaic image
            cropRightDownSlidingImages(inputImage, inputImageName, outputCroppedImagesMosaicPath, sizeSquareImage,
                                       mosaicLin, mosaicCol)


# ###########################################
# Methods of Level 3
# ###########################################


# crops the image considering the horizontal and vertical bands
def cropHorizontalVerticalImage(inputImage, inputImageName, outputCroppedImagesMosaicPath, sizeSquareImage, mosaicLin,
                                mosaicCol):
    # getting the image shape
    imageHeight, imageWidth, imageChannel = inputImage.shape

    # setting the name of cropped mosaic image
    sufixName = '-hv'
    croppedImageName = getCroppedImageName(inputImageName, mosaicLin, mosaicCol, sufixName)
    croppedImagePathAndImageName = outputCroppedImagesMosaicPath + croppedImageName

    # defining the two points of the cropped image
    linP1 = (mosaicLin - 1) * sizeSquareImage
    colP1 = (mosaicCol - 1) * sizeSquareImage
    linP2 = mosaicLin * sizeSquareImage
    colP2 = mosaicCol * sizeSquareImage

    # checking the image boundaries
    if (colP2 > imageWidth):
        colP2 = imageWidth
        colP1 = colP2 - sizeSquareImage

    if (linP2 > imageHeight):
        linP2 = imageHeight
        linP1 = linP2 - sizeSquareImage

    # cropping and saving bounding box in new image
    croppedImage = inputImage[linP1:linP2, colP1:colP2]
    croppedImageWidth = linP2 - linP1
    croppedImageHeight = colP2 - colP1

    # saving the cropped image
    saveCroppedImage(croppedImagePathAndImageName, croppedImage)

    # saving the cropped image details
    saveCroppedImageDetailsFile(outputCroppedImagesMosaicPath, inputImageName, imageHeight, imageWidth,
                                sizeSquareImage, mosaicLin, mosaicCol, linP1, colP1, linP2, colP2,
                                sufixName
                                )


# crops the image considering the right sliding
def cropRightSlidingImage(inputImage, inputImageName, outputCroppedImagesMosaicPath, sizeSquareImage, mosaicLin,
                          mosaicCol):
    # getting the image shape
    imageHeight, imageWidth, imageChannel = inputImage.shape

    # setting the name of cropped mosaic image
    sufixName = '-slidRight'
    croppedImageName = getCroppedImageName(inputImageName, mosaicLin, mosaicCol, sufixName)
    croppedImagePathAndImageName = outputCroppedImagesMosaicPath + croppedImageName

    # setting the slide size
    sizeSlide = int(sizeSquareImage / 2)

    # defining the two points of the cropped image
    linP1 = (mosaicLin - 1) * sizeSquareImage
    colP1 = (mosaicCol - 1) * sizeSquareImage + sizeSlide
    linP2 = mosaicLin * sizeSquareImage
    colP2 = mosaicCol * sizeSquareImage + sizeSlide

    # cropping and saving bounding box in new image
    croppedImage = inputImage[linP1:linP2, colP1:colP2]
    croppedImageWidth = linP2 - linP1
    croppedImageHeight = colP2 - colP1

    # saving the cropped image
    saveCroppedImage(croppedImagePathAndImageName, croppedImage)

    # saving the cropped image details
    saveCroppedImageDetailsFile(outputCroppedImagesMosaicPath, inputImageName, imageHeight, imageWidth,
                                sizeSquareImage, mosaicLin, mosaicCol, linP1, colP1, linP2, colP2,
                                sufixName
                                )


# crops the image considering the down sliding
def cropDownSlidingImage(inputImage, inputImageName, outputCroppedImagesMosaicPath, sizeSquareImage, mosaicLin,
                         mosaicCol):
    # getting the image shape
    imageHeight, imageWidth, imageChannel = inputImage.shape

    # setting the name of cropped mosaic image
    sufixName = '-slidDown'
    croppedImageName = getCroppedImageName(inputImageName, mosaicLin, mosaicCol, sufixName)
    croppedImagePathAndImageName = outputCroppedImagesMosaicPath + croppedImageName

    # setting the slide size
    sizeSlide = int(sizeSquareImage / 2)

    # defining the two points of the cropped image
    linP1 = (mosaicLin - 1) * sizeSquareImage + sizeSlide
    colP1 = (mosaicCol - 1) * sizeSquareImage
    linP2 = mosaicLin * sizeSquareImage + sizeSlide
    colP2 = mosaicCol * sizeSquareImage

    # cropping and saving bounding box in new image
    croppedImage = inputImage[linP1:linP2, colP1:colP2]
    croppedImageWidth = linP2 - linP1
    croppedImageHeight = colP2 - colP1

    # saving the cropped image
    saveCroppedImage(croppedImagePathAndImageName, croppedImage)

    # saving the cropped image details
    saveCroppedImageDetailsFile(outputCroppedImagesMosaicPath, inputImageName, imageHeight, imageWidth,
                                sizeSquareImage, mosaicLin, mosaicCol, linP1, colP1, linP2, colP2,
                                sufixName
                                )


# crops the sliding image
def cropRightDownSlidingImages(inputImage, inputImageName, outputCroppedImagesMosaicPath, sizeSquareImage, mosaicLin,
                               mosaicCol):
    # getting the image shape
    imageHeight, imageWidth, imageChannel = inputImage.shape

    # setting the name of cropped mosaic image
    sufixName = '-slidRightDown'
    croppedImageName = getCroppedImageName(inputImageName, mosaicLin, mosaicCol, sufixName)
    croppedImagePathAndImageName = outputCroppedImagesMosaicPath + croppedImageName

    # setting the slide size
    sizeSlide = int(sizeSquareImage / 2)

    # defining the two points of the cropped image
    linP1 = (mosaicLin - 1) * sizeSquareImage + sizeSlide
    colP1 = (mosaicCol - 1) * sizeSquareImage + sizeSlide
    linP2 = mosaicLin * sizeSquareImage + sizeSlide
    colP2 = mosaicCol * sizeSquareImage + sizeSlide

    # cropping and saving bounding box in new image
    croppedImage = inputImage[linP1:linP2, colP1:colP2]
    croppedImageWidth = linP2 - linP1
    croppedImageHeight = colP2 - colP1

    # saving the cropped image
    saveCroppedImage(croppedImagePathAndImageName, croppedImage)

    # saving the cropped image details
    saveCroppedImageDetailsFile(outputCroppedImagesMosaicPath, inputImageName, imageHeight, imageWidth,
                                sizeSquareImage, mosaicLin, mosaicCol, linP1, colP1, linP2, colP2,
                                sufixName
                                )


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
