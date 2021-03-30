"""
Project: Create a mosaic of images from images of any size.
Author: Rubens de Castro Pereira
Advisor: Dibio Leandro Borges
Date: 18/03/2021
Version: 1.0.0
"""

# Importing needed libraries
import os
# import math
import json
import cv2
import cv2.cv2 as cv
# from shutil import copyfile
import numpy as np

# ###########################################
# Constants
# ###########################################
from setuptools.command.dist_info import dist_info

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
        # segmentByWatershedOriginal(inputImage, inputImageName, outputCroppedImagesMosaicPath)

        # segments the image
        # segmentByWatershedAdjusted(inputImage, inputImageName, outputCroppedImagesMosaicPath)

        # segments the image
        segmentByMorphological(inputImage, inputImageName, outputCroppedImagesMosaicPath)

        # segments the image
        # segementByConvexHull(inputImage, inputImageName, sizeSquareImage, outputCroppedImagesMosaicPath)

        # segments the image
        # segementByColorSpace(inputImage, inputImageName, sizeSquareImage, outputCroppedImagesMosaicPath)

        # segments the image
        # segementByColorThresholding(inputImage, inputImageName, outputCroppedImagesMosaicPath)

        # segments the image
        # imageResult = segmentByGreenColorThresholding(inputImage, inputImageName, outputCroppedImagesMosaicPath)

        x = 0

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
# def segementByContours(inputImage, inputImageName, sizeSquareImage, outputCroppedImagesMosaicPath):
#     # get image shape
#     # imageHeight, imageWidth, imageChannel = inputImage.shape
#
#     # Grayscale
#     gray = cv2.cvtColor(inputImage, cv2.COLOR_BGR2GRAY)
#
#     # Find Canny edges
#     edged = cv2.Canny(gray, 30, 200)
#     cv2.waitKey(0)
#
#     # Finding Contours
#     # Use a copy of the image e.g. edged.copy()
#     # since findContours alters the image
#     contours, hierarchy = cv2.findContours(edged,
#                                            cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
#
#     # showing image
#     imageWindowName = 'Canny'
#     showImageInWindow(edged, imageWindowName, width, height, True)
#     # cv2.waitKey(0)
#
#     print("Number of Contours found = " + str(len(contours)))
#
#     # Draw all contours
#     # -1 signifies drawing all contours
#     cv2.drawContours(inputImage, contours, -1, (0, 255, 0), 3)
#
#     # showing image
#     imageWindowName = 'Contours'
#     showImageInWindow(inputImage, imageWindowName, width, height, True)
#     cv2.waitKey(0)
#
#     cv2.destroyAllWindows()


# segments the original image to define the ROI (Region Of Interest)
# https://towardsdatascience.com/extracting-regions-of-interest-from-images-dacfd05a41ba
# def segementByGaussianBlurAndCanny(inputImage, inputImageName, sizeSquareImage, outputCroppedImagesMosaicPath):
#     # Grayscale
#     gray = cv2.cvtColor(inputImage, cv2.COLOR_BGR2GRAY)
#
#     # Gaussian Blur
#     gray = cv2.GaussianBlur(inputImage, (11, 11), 0)
#     # showing image
#     imageWindowName = 'GaussianBlur'
#     showImageInWindow(gray, imageWindowName, width, height, True)
#     # cv2.waitKey(0)
#
#     # Find Canny edges
#     edged = cv2.Canny(gray, 30, 200)
#     # cv2.waitKey(0)
#
#     # Finding Contours
#     # Use a copy of the image e.g. edged.copy()
#     # since findContours alters the image
#     contours, hierarchy = cv2.findContours(edged,
#                                            cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
#
#     # showing image
#     imageWindowName = 'Canny'
#     showImageInWindow(edged, imageWindowName, width, height, True)
#     # cv2.waitKey(0)
#
#     print("Number of Contours found = " + str(len(contours)))
#
#     # Draw all contours
#     # -1 signifies drawing all contours
#     cv2.drawContours(inputImage, contours, -1, (0, 255, 0), 3)
#
#     # showing image
#     imageWindowName = 'Canny'
#     showImageInWindow(inputImage, imageWindowName, width, height, True)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
#

# https://docs.opencv.org/master/d3/db4/tutorial_py_watershed.html
def segmentByWatershedOriginal(inputImage, inputImageName, outputCroppedImagesMosaicPath):
    height = 480
    width = 640

    # Grayscale
    gray = cv2.cvtColor(inputImage, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # showing image
    imageWindowName = 'color converted to gray'
    showImageInWindow(gray, imageWindowName, width, height, False)
    imageWindowName = 'ret'
    showImageInWindow(ret, imageWindowName, width, height, False)
    imageWindowName = 'threshold'
    showImageInWindow(thresh, imageWindowName, width, height, False)
    # cv2.waitKey(0)

    # noise removal
    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
    imageWindowName = 'opening'
    showImageInWindow(opening, imageWindowName, width, height, False)
    cv2.waitKey(0)

    # sure background area
    sure_bg = cv2.dilate(opening, kernel, iterations=3)
    imageWindowName = 'dilate sure_bg'
    showImageInWindow(sure_bg, imageWindowName, width, height, False)
    # cv2.waitKey(0)

    # Finding sure foreground area
    dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
    imageWindowName = 'distanceTransform '
    showImageInWindow(dist_transform, imageWindowName, width, height, False)

    # ret, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)
    x = dist_transform.max()
    ret, sure_fg = cv2.threshold(dist_transform, 0.2 * dist_transform.max(), 255, 0)
    imageWindowName = 'distanceTransform - ret'
    showImageInWindow(ret, imageWindowName, width, height, False)
    imageWindowName = 'distanceTransform - threshold sure_bg'
    showImageInWindow(sure_bg, imageWindowName, width, height, False)
    # cv2.waitKey(0)

    # Finding unknown region
    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg, sure_fg)
    imageWindowName = 'subtract'
    showImageInWindow(unknown, imageWindowName, width, height, False)

    # Marker labelling
    ret, markers = cv2.connectedComponents(sure_fg)

    # Add one to all labels so that sure background is not 0, but 1
    markers = markers + 1

    # Now, mark the region of unknown with zero
    markers[unknown == 255] = 0
    markers = cv2.watershed(inputImage, markers)
    inputImage[markers == -1] = [255, 0, 0]
    imageWindowName = 'watershed'
    showImageInWindow(inputImage, imageWindowName, width, height, True)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


# https://docs.opencv.org/master/d3/db4/tutorial_py_watershed.html
# https://stackoverflow.com/questions/47483951/how-to-define-a-threshold-value-to-detect-only-green-colour-objects-in-an-image
# https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_morphological_ops/py_morphological_ops.html
def segmentByWatershedAdjusted(inputImage, inputImageName, outputCroppedImagesMosaicPath):
    height = 480
    width = 640

    # #################################################################
    # Step 1: threshold image
    # #################################################################

    # convert to hsv
    hsvImage = cv2.cvtColor(inputImage, cv2.COLOR_BGR2HSV)
    imageWindowName = inputImageName + '-hsvImage'
    showImageInWindow(hsvImage, imageWindowName, width, height, False)

    # mask of green (36,25,25) ~ (86, 255,255)
    # mask = cv2.inRange(hsvImage, (26, 25, 25), (86, 255, 255))
    # mask = cv2.inRange(hsvImage, (40, 40, 40), (70, 255, 255))
    mask = cv2.inRange(hsvImage, (0, 100, 100), (200, 255, 255))
    imageWindowName = inputImageName + '-threshold'
    showImageInWindow(mask, imageWindowName, width, height, True)

    # #################################################################
    # Step 2: removes noise of the image
    # #################################################################

    # noise removal by opening
    # openingKernel = np.ones((3, 3), np.uint8)
    openingKernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, openingKernel, iterations=2)
    imageWindowName = inputImageName + '-opening'
    showImageInWindow(opening, imageWindowName, width, height, True)

    # #################################################################
    # Step 3: get sure background area of "opening image" by dilating
    # #################################################################
    dilatingKernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    backgroundImage = cv2.morphologyEx(opening, cv2.MORPH_DILATE, dilatingKernel, iterations=3)
    imageWindowName = inputImageName + '-backgroundImage-by-dilating'
    showImageInWindow(backgroundImage, imageWindowName, width, height, True)

    # #################################################################
    # Step 4: get sure foreground area of "opening image" by erosion
    # #################################################################
    erosionKernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    foregroundImage = cv2.morphologyEx(opening, cv2.MORPH_ERODE, erosionKernel, iterations=3)
    imageWindowName = inputImageName + '-foregroundImage-by-erosion'
    showImageInWindow(foregroundImage, imageWindowName, width, height, True)

    # # #################################################################
    # # Step 4: get sure foreground area of "opening image" by dilation
    # # #################################################################
    # dilatingKernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    # foregroundImage = cv2.morphologyEx(opening, cv2.MORPH_DILATE, dilatingKernel, iterations=10)
    # imageWindowName = inputImageName + '-foregroundImage-by-dilating-3x3'
    # showImageInWindow(foregroundImage, imageWindowName, width, height, True)
    #
    # dilatingKernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    # foregroundImage = cv2.morphologyEx(foregroundImage, cv2.MORPH_DILATE, dilatingKernel, iterations=10)
    # imageWindowName = inputImageName + '-foregroundImage-by-dilating-5x5'
    # showImageInWindow(foregroundImage, imageWindowName, width, height, True)

    # #################################################################
    # Step 5: Find unknown region by subtraction the
    #         background of foreground images
    # #################################################################
    foregroundImage = np.uint8(foregroundImage)
    unknown = cv.subtract(backgroundImage, foregroundImage)
    imageWindowName = inputImageName + '-unknown'
    showImageInWindow(unknown, imageWindowName, width, height, True)

    # #################################################################
    # Step 6: marking the unknown region with 0
    # #################################################################
    # Marker labelling
    ret, markers = cv2.connectedComponents(foregroundImage)
    # Add one to all labels so that sure background is not 0, but 1
    markers = markers + 1
    # Now, mark the region of unknown with zero
    markers[unknown == 255] = 0
    # # applying color map in the input image
    # inputImageColorMap = cv2.applyColorMap(markers, cv2.COLORMAP_JET)
    # imageWindowName = inputImageName + '-markers'
    # showImageInWindow(inputImageColorMap, imageWindowName, width, height, True)

    # #################################################################
    # Step 7: applying watershed into the input image using markers
    # #################################################################

    markersResult = cv.watershed(inputImage, markers)
    inputImage[markersResult == -1] = [255, 0, 0]
    imageWindowName = inputImageName + '-watershed'
    showImageInWindow(inputImage, imageWindowName, width, height, True)

    cv2.waitKey(0)

    # # #################################################################
    # # Step 4: get sure foreground area of "opening image" by erosion
    # # #################################################################
    # erosionKernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    # foregroundImage = cv2.morphologyEx(opening, cv2.MORPH_ERODE, erosionKernel, iterations=3)
    # imageWindowName = inputImageName + '-foregroundImage-by-erosion'
    # showImageInWindow(foregroundImage, imageWindowName, width, height, True)

    # # #################################################################
    # # Step 4: removes small holes in the image
    # # #################################################################
    # # closingKernel = np.ones((5, 5), np.uint8)
    # closingKernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    # closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, closingKernel, iterations=3)
    # imageWindowName = inputImageName + '-closing'
    # showImageInWindow(closing, imageWindowName, width, height, True)

    cv2.waitKey(0)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

# colorizer.org
def segmentByMorphological(inputImage, inputImageName, outputImagesMosaicPath):
    height = 480
    width = 640

    # #################################################################
    # Step 1: threshold image
    # #################################################################

    # convert to hsv
    hsvImage = cv2.cvtColor(inputImage, cv2.COLOR_BGR2HSV)
    imageWindowName = inputImageName + '-hsvImage'
    showImageInWindow(hsvImage, imageWindowName, width, height, True)

    # mask of green (36,25,25) ~ (86, 255,255)
    # mask = cv2.inRange(hsvImage, (40, 40, 40), (70, 255, 255))
    mask = cv2.inRange(hsvImage, (0, 100, 100), (220, 255, 255))
    imageWindowName = inputImageName + '-threshold'
    showImageInWindow(mask, imageWindowName, width, height, True)

    # #################################################################
    # Step 2: removes noise of the image
    # #################################################################

    # noise removal by opening
    # openingKernel = np.ones((3, 3), np.uint8)
    openingKernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, openingKernel, iterations=2)
    imageWindowName = inputImageName + '-opening'
    showImageInWindow(opening, imageWindowName, width, height, True)

    # #################################################################
    # Step 3: get sure foreground area of "opening image" by dilation
    # #################################################################
    dilatingKernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    foregroundImage = cv2.morphologyEx(opening, cv2.MORPH_DILATE, dilatingKernel, iterations=10)
    imageWindowName = inputImageName + '-foregroundImage-by-dilating-3x3'
    showImageInWindow(foregroundImage, imageWindowName, width, height, True)

    dilatingKernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    foregroundImage = cv2.morphologyEx(foregroundImage, cv2.MORPH_DILATE, dilatingKernel, iterations=5)
    imageWindowName = inputImageName + '-foregroundImage-by-dilating-5x5'
    showImageInWindow(foregroundImage, imageWindowName, width, height, True)

    # #################################################################
    # Step 4: multiply the foreground image by input image
    # #################################################################
    imageHeight, imageWidth, imageChannel = inputImage.shape
    # resultImage = np.zeros((imageHeight, imageWidth), np.uint8)
    resultImage = inputImage.copy()
    # for lin in range(0, imageHeight):
    #     for col in range(0, imageWidth):
    #         resultImage[lin, col] = [0, 0, 0]
    resultImage[:, :] = [0, 0, 0]

    # show just the foreground pixels
    for lin in range(0, imageHeight):
        for col in range(0, imageWidth):
            if foregroundImage[lin, col] > 0:
                resultImage[lin, col] = inputImage[lin, col]

    # show all pixels between the leaf boundaries
    # for lin in range(0, imageHeight):
    #     # initializing the auxiliary indexes
    #     leftCol = 0
    #     rightCol = imageWidth
    #     for col in range(0, imageWidth):
    #         if foregroundImage[lin, col] > 0:
    #             leftCol = col
    #             break
    #     for col in range(imageWidth - 1, 0, -1):
    #         if foregroundImage[lin, col] > 0:
    #             rightCol = col
    #             break
    #     # for col in range(leftCol, rightCol):
    #     #     resultImage[lin, col] = inputImage[lin, col]
    #     resultImage[lin, leftCol:rightCol] = inputImage[lin, leftCol:rightCol]

    # resultImage[foregroundImage > 0] = inputImage
    imageWindowName = inputImageName + '-resultImage'
    showImageInWindow(resultImage, imageWindowName, width, height, True)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # saving the result image
    resultImageName = outputImagesMosaicPath + inputImageName + '-just-leaf'
    saveResultImage(resultImageName, resultImage)


# https://circuitdigest.com/tutorial/image-segmentation-using-opencv
def segementByConvexHull(inputImage, inputImageName, sizeSquareImage, outputCroppedImagesMosaicPath):
    # converting color image into gray image
    gray = cv2.cvtColor(inputImage, cv2.COLOR_BGR2GRAY)

    # Threshold the image
    ret, thresh = cv2.threshold(gray, 176, 255, 0)

    # Find contours
    _, contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

    # Sort the contours by area and then remove the largest frame contour
    n = len(contours) - 1
    contours = sorted(contours, key=cv2.contourArea, reverse=False)[:n]

    # Iterate through the contours and draw convex hull
    for contour in contours:
        hull = cv2.convexHull(contour)
        cv2.drawContours(inputImage, [hull], 0, (0, 255, 0), 2)
        cv2.imshow('convex hull', inputImage)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


# https://realpython.com/python-opencv-color-spaces/
# def segementByColorSpace(inputImage, inputImageName, sizeSquareImage, outputCroppedImagesMosaicPath):
#     flags = [i for i in dir(cv2) if i.startswith('COLOR_')]
#
#     inputImage = cv2.cvtColor(inputImage, cv2.COLOR_BGR2RGB)
#     imageWindowName = 'colorSpace'
#     showImageInWindow(inputImage, imageWindowName, width, height, True)
#
#     cv2.waitKey(0)
#
#     x = 0


# https://ckyrkou.medium.com/color-thresholding-in-opencv-91049607b06d
def segmentByColorThresholding(inputImage, inputImageName, outputCroppedImagesMosaicPath):
    # setting the size parameters of thw window
    height = 300
    width = 400

    # The order of the colors is blue, green, red
    # lower_color_bounds = cv2.Scalar(100, 0, 0)
    # upper_color_bounds = cv2.Scalar(225, 80, 80)
    lower_color_bounds = (100, 0, 0)
    upper_color_bounds = (225, 80, 80)

    # converting color image into gray image
    gray = cv2.cvtColor(inputImage, cv2.COLOR_BGR2GRAY)
    imageWindowName = 'color converted to gray'
    showImageInWindow(gray, imageWindowName, width, height, True)

    mask = cv2.inRange(inputImage, lower_color_bounds, upper_color_bounds)
    imageWindowName = 'mask thresholded'
    showImageInWindow(mask, imageWindowName, width, height, True)

    mask_rgb = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    imageWindowName = 'mask gray converted to color'
    showImageInWindow(mask_rgb, imageWindowName, width, height, True)

    # updating input image with the mask
    inputImage = inputImage & mask_rgb

    imageWindowName = 'result'
    showImageInWindow(inputImage, imageWindowName, width, height, True)

    cv2.waitKey(0)


# https://stackoverflow.com/questions/47483951/how-to-define-a-threshold-value-to-detect-only-green-colour-objects-in-an-image
def segmentByGreenColorThresholding(inputImage, inputImageName, outputCroppedImagesMosaicPath):
    # setting the size parameters of thw window
    height = 480
    width = 640

    imageWindowName = inputImageName + '-original'
    showImageInWindow(inputImage, imageWindowName, width, height, False)

    ## convert to hsv
    hsvImage = cv2.cvtColor(inputImage, cv2.COLOR_BGR2HSV)
    imageWindowName = inputImageName + '-hsvImage'
    showImageInWindow(hsvImage, imageWindowName, width, height, False)

    # mask of green (36,25,25) ~ (86, 255,255)
    # mask = cv2.inRange(hsv, (36, 25, 25), (86, 255,255))
    # mask = cv2.inRange(hsvImage, (36, 25, 25), (70, 255, 255))
    mask = cv2.inRange(hsvImage, (40, 40, 40), (70, 255, 255))
    imageWindowName = inputImageName + '-mask'
    showImageInWindow(mask, imageWindowName, width, height, True)

    # noise removal by opening
    openingKernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, openingKernel, iterations=3)
    imageWindowName = inputImageName + '-opening'
    showImageInWindow(opening, imageWindowName, width, height, True)

    # closing
    # closingKernel = np.ones((3, 3), np.uint8)
    # closing = cv2.morphologyEx(opening, cv2.MORPH_OPEN, closingKernel, iterations=3)
    # imageWindowName = inputImageName + '-closing'
    # showImageInWindow(closing, imageWindowName, width, height, True)

    # sure background area
    # dilateKernel = np.ones((9, 9), np.uint8)
    # dilated = cv2.dilate(opening, dilateKernel, iterations=10)
    # imageWindowName = inputImageName + '-dilated'
    # showImageInWindow(opening, imageWindowName, width, height, True)

    # slice the green
    imask = mask > 0
    green = np.zeros_like(inputImage, np.uint8)
    green[imask] = inputImage[imask]
    imageWindowName = inputImageName + '-result'
    showImageInWindow(green, imageWindowName, width, height, True)

    # cv2.waitKey(0)

    return green


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


# save the image
def saveResultImage(fullPathAndImageName, image):
    # adjusting the file name
    fullPathAndImageName += '.jpg'

    # removing old file
    removeFile(fullPathAndImageName)

    # save image
    cv2.imwrite(fullPathAndImageName, image)
    print(fullPathAndImageName)


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
# Methods of Level 5
# ###########################################


# remove file
def removeFile(fullPathAndFileName):
    if os.path.exists(fullPathAndFileName):
        os.remove(fullPathAndFileName)


# ###########################################
# Main method
# ###########################################
if __name__ == '__main__':
    INPUT_ORIGINAL_IMAGES_PATH = \
        'E:/desenvolvimento/projetos/DoctoralProjects/ImageMosaicProjectImages/01. input original images/'
    OUTPUT_CROPPED_IMAGES_MOSAIC_PATH = \
        'E:/desenvolvimento/projetos/DoctoralProjects/ImageMosaicProjectImages/01.2 input images with just leaf/'

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

    # stop processing to view the results
    cv2.waitKey(0)

    # end of processing
    print('End of processing')
