import Image

class HistogramPolitic(object):
    
    
    def calculateSizeBox ( self, frame, totalHorizontalDivisions = 4, totalVerticalDivisions = 4 ):
        sizeBox = [0,0]
        sizeBox[0] = frame.size[0] / totalHorizontalDivisions  
        sizeBox[1] = frame.size[1] / totalVerticalDivisions   
        return sizeBox
    
    def calculateBoxesHistogramDiference( self, histogram1, histogram2 ):
        diferenceHistogram = []
        for box in range(len(histogram1)):
            diferenceHistogram.append(0)
            for bin in range(0,256):
                diferenceHistogram[box] = diferenceHistogram[box] + (abs(histogram1[box][ bin ] - histogram2[box][ bin ]))
        diferenceHistogram.sort()
        diferenceHistogram = diferenceHistogram[0:8]
        return diferenceHistogram

    def potentialShot( self, diferenceList, sensitivity):
        diferenceSum = sum(diferenceList)             
        return sensitivity < diferenceSum

    def verifyTransition(self, frameAHistogram, frameBHistogram, frameCHistogram, sensitivity):
        backwardDiference = self.calculateBoxesHistogramDiference( frameAHistogram, frameBHistogram )
        forwardDiference = self.calculateBoxesHistogramDiference( frameBHistogram, frameCHistogram )
        if not( self.potentialShot( forwardDiference, sensitivity ) ) and ( self.potentialShot( backwardDiference, sensitivity ) ):
                return True
        return False

    def calculateSensitivity ( self, sensitivityPercentage, frame ):
        totalBoxPixels = frame.size[0] * frame.size[1]
        sensitivity = int( totalBoxPixels * sensitivityPercentage )
        return sensitivity
