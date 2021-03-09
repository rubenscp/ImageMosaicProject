# BoundingBox Class
from Entity.Pixel import Pixel


class BoundingBox:
    def __init__(self, linPoint1=None, colPoint1=None, linPoint2=None, colPoint2=None, className='', confidence=0):
        self.linPoint1 = linPoint1
        self.colPoint1 = colPoint1
        self.linPoint2 = linPoint2
        self.colPoint2 = colPoint2
        self.className = className
        self.confidence = confidence

    def toString(self):
        text = 'Class: ' + self.className + ' P1: (' + str(self.linPoint1) + ',' + str(
            self.colPoint1) + ')  P2: (' + str(self.linPoint2) + ',' + str(
            self.colPoint2) + ')' + '  confidence: ' + str(self.confidence)
        return text

    def isBelongs(self, pixel: Pixel):
        # checking if pixel is in the bounding box
        if all([
            pixel.lin >= self.linPoint1,
            pixel.lin <= self.linPoint2,
            pixel.col >= self.colPoint1,
            pixel.col <= self.colPoint2
        ]):
            return True

        # if pixel.lin >= self.linPoint1 and pixel.lin <= self.linPoint2 and pixel.col >= self.colPoint1 and pixel.col <= self.colPoint2:

        # obtaining the new bounding box coordinates using neighbor of one pixel
        newLinPoint1 = self.linPoint1 - 1
        newColPoint1 = self.colPoint1 - 1
        newLinPoint2 = self.linPoint2 + 1
        newColPoint2 = self.colPoint2 + 1

        # checking if pixel is neighbor of 1 pixel of the bounding box
        if pixel.lin >= newLinPoint1 and pixel.lin <= newLinPoint2 and \
                pixel.col >= newColPoint1 and pixel.col <= newColPoint2:
            return True

        # the current pixel does not belong to none bounding box
        return False

    def getYoloAnnotation(self, width, height):
        heightOfCentrePoint = self.linPoint2 - self.linPoint1
        widthOfCentrePoint = self.colPoint2 - self.colPoint1
        linOfCentrePoint = (self.linPoint1 + (heightOfCentrePoint / 2.0)) / height
        colOfCentrePoint = (self.colPoint1 + (widthOfCentrePoint / 2.0)) / width
        heightOfCentrePoint /= height
        widthOfCentrePoint /= width
        return linOfCentrePoint, colOfCentrePoint, widthOfCentrePoint, heightOfCentrePoint

    def setYoloAnnotation(self, imageHeight, imageWidth, colOfCentrePoint, linOfCentrePoint, heightOfCentrePoint,
                          widthOfCentrePoint, idBoundingBox, idClass):
        # setting class name
        self.setClassName(idClass)

        # calculates the coordinates of the two points

        # unnormalizing values
        heightOfBoundingBox = heightOfCentrePoint * imageHeight
        widthOfBoundingBox = widthOfCentrePoint * imageWidth
        lin = linOfCentrePoint * imageHeight
        col = colOfCentrePoint * imageWidth

        # getting the points coordiniates
        self.linPoint1 = int(lin - (heightOfBoundingBox / 2.0))
        self.colPoint1 = int(col - (widthOfBoundingBox / 2.0))
        self.linPoint2 = int(lin + (heightOfBoundingBox / 2.0))
        self.colPoint2 = int(col + (widthOfBoundingBox / 2.0))

        # print('Yolo annotations: ', imageWidth, imageHeight, linOfCentrePoint, colOfCentrePoint, widthOfCentrePoint,
        #       heightOfCentrePoint)
        # print('BB:', idBoundingBox, 'Two points coordinates: ', self.linPoint1, self.colPoint1, self.linPoint2,
        #       self.colPoint2, self.className, )
        return

    def expandBoudingBox(self, expandedPixels):
        self.linPoint1 -= expandedPixels
        self.colPoint1 -= expandedPixels
        self.linPoint2 += expandedPixels
        self.colPoint2 += expandedPixels

    def setClassName(self, idClass):
        if idClass == 0:
            self.className = 'exuvia'
        elif idClass == 1:
            self.className = 'instar1'
        elif idClass == 2:
            self.className = 'instar2'
        elif idClass == 3:
            self.className = 'instar3'
        elif idClass == 4:
            self.className = 'instar4'
        elif idClass == 5:
            self.className = 'adulta'
        elif idClass == 6:
            self.className = 'ovo'
        elif idClass == 7:
            self.className = 'instar1ou2'
        elif idClass == 8:
            self.className = 'instar3ou4'
