from politics import HistogramPolitic
from opencv.cv import cvCanny, cvCreateImage, cvCvtColor, cvGetSize 
from opencv.cv import IPL_DEPTH_8U, CV_BGR2GRAY
from opencv.adaptors import Ipl2PIL

class ImageManipulation(object):
    
    
    def createHistogramBoxes( self, vetImg, frame, totalHorizontalDivisions = 4, totalVerticalDivisions = 4 ):
        cropHistogram = []
        histogramPolitic = HistogramPolitic()
        sizeBox = histogramPolitic.calculateSizeBox ( vetImg[frame] )
        for horizontalDivision in range( totalHorizontalDivisions ):
            for verticalDivision in range( totalVerticalDivisions ):
                x1Point = horizontalDivision * sizeBox[0]
                y1Point = verticalDivision * sizeBox[1]
                x2Point = x1Point + sizeBox[0] - 1
                y2Point = y1Point + sizeBox[1] - 1
                box = (x1Point, y1Point, x2Point, y2Point)
                cropHistogram.append( vetImg[ frame ].crop(box).convert("L").histogram() )
        return cropHistogram
  
