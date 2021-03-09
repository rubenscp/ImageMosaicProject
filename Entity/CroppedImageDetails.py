# Cropped Image Details Class


class CroppedImageDetails:
    def __init__(self,
                 croppedImagePath=None,
                 originalImageName=None,
                 originalImageHeight=None,
                 originalImageWidth=None,
                 croppedImageName=None,
                 sizeSquareImage=None,
                 mosaicLin=None,
                 mosaicCol=None,
                 linP1=None,
                 colP1=None,
                 linP2=None,
                 colP2=None):
        self.croppedImagePath = croppedImagePath
        self.originalImageName = originalImageName
        self.originalImageHeight = originalImageHeight
        self.originalImageWidth = originalImageWidth
        self.croppedImageName = croppedImageName
        self.sizeSquareImage = sizeSquareImage
        self.mosaicLin = mosaicLin
        self.mosaicCol = mosaicCol
        self.linP1 = linP1
        self.colP1 = colP1
        self.linP2 = linP2
        self.colP2 = colP2
