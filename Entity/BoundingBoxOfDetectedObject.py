# Bouding Box of detected object Class


class BoundingBoxOfDetectedObject:
    def __init__(self,
                 croppedImageDetails=None,
                 boundingBox=None,
                 linPoint1InOriginalImage=None,
                 colPoint1InOriginalImage=None,
                 linPoint2InOriginalImage=None,
                 colPoint2InOriginalImage=None,
                 processed=False):
        self.croppedImageDetails = croppedImageDetails
        self.boundingBox = boundingBox
        self.linPoint1InOriginalImage = linPoint1InOriginalImage
        self.colPoint1InOriginalImage = colPoint1InOriginalImage
        self.linPoint2InOriginalImage = linPoint2InOriginalImage
        self.colPoint2InOriginalImage = colPoint2InOriginalImage
        self.processed = processed

    def setCoordinatesInOriginalImage(self):
        #  calculating the final coordinates of the bounding box in the original image
        self.linPoint1InOriginalImage = self.croppedImageDetails.linP1 + self.boundingBox.linPoint1
        self.colPoint1InOriginalImage = self.croppedImageDetails.colP1 + self.boundingBox.colPoint1
        self.linPoint2InOriginalImage = self.croppedImageDetails.linP1 + self.boundingBox.linPoint2
        self.colPoint2InOriginalImage = self.croppedImageDetails.colP1 + self.boundingBox.colPoint2
