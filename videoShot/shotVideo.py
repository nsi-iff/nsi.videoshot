from opencv.highgui import cvCreateFileCapture, cvQueryFrame, cvSaveImage, cvGetCaptureProperty, CV_CAP_PROP_FPS
from opencv.cv import cvCloneImage
from opencv.adaptors import Ipl2PIL
from imageManipulation import ImageManipulation
from politics import  HistogramPolitic
import os

class InitExtract(object):


    def createCapture(self, file_name):
        capture = cvCreateFileCapture(file_name)
        return capture

    def pass_frames(self, capture, frames_bloc, fator):
        for i in range(frames_bloc * fator - 2):
            cvQueryFrame(capture)
        return capture

    def initFrameCapture(self, capture):    
        for i in range(25):
            frame = cvQueryFrame(capture)
        return frame
                        
class ShotVideo(object):
 
 
    lastSaved = 0
    number_frame = 0
    block = True
    _list = []
    
    def initLoadFrames(self, frameA, frameB):
        vetFrames = [Ipl2PIL(frameA),Ipl2PIL(frameB),0]
        return vetFrames
    
    def contFrames(self,capture):
        frame = cvQueryFrame(capture)
        total_frames = 1
        while frame <> None:
            frame = cvQueryFrame(capture)
            total_frames+=1
        return total_frames
        
    def atualizeVetImg(self, vetImg, frame):
        vetImg.pop(0)
        vetImg.append(frame)
        return vetImg
    
    def saveTransition(self, file_name_save, frames_bloc, vetImg):
        self.lastSaved = self.number_frame        
        vetImg[1].save(file_name_save + 'trans_time_' + str(round(self.number_frame / self.fps, 2)) + '.jpg' , 'JPEG')
        self._list.append(self.number_frame / self.fps)
                  
    def atualizeVar(self, frameA, frameB, frameC, capture):
        frameA = cvCloneImage(frameB)
        frameB = cvCloneImage(frameC) 
        frameC = cvQueryFrame(capture)
        return frameA, frameB, frameC
        
    def passFrame(self,capture):
        frameA = cvQueryFrame(capture)
        frameB = cvQueryFrame(capture)
        frameC = cvQueryFrame(capture)
        return frameA, frameB, frameC
        
    def shotDetect(self,queue, capture, sensitivity, number_frame, frames_bloc, file_name, file_name_save, file_video_save, ncpu, ncpus): 
        self.number_frame = number_frame
        self.fps = cvGetCaptureProperty(capture, CV_CAP_PROP_FPS)
        histogramPolitic = HistogramPolitic()
        imageManipulation = ImageManipulation()
        frameA, frameB, frameC = self.passFrame(capture) 
        vetImg = self.initLoadFrames(frameA, frameB)
        frameAHistogram = imageManipulation.createHistogramBoxes(vetImg, 0)
        frameBHistogram = imageManipulation.createHistogramBoxes(vetImg, 1)
        limiar = histogramPolitic.calculateSensitivity(sensitivity, vetImg[0])   
        while not(frameC is None) and (self.number_frame<= frames_bloc):
            vetImg = self.atualizeVetImg(vetImg, Ipl2PIL(frameC))
            frameCHistogram = imageManipulation.createHistogramBoxes(vetImg, 2)
            if histogramPolitic.verifyTransition(frameAHistogram, frameBHistogram, frameCHistogram, limiar) and (self.number_frame - self.lastSaved) > 20:         
                self.saveTransition(file_name_save, frames_bloc, vetImg) 
            frameA, frameB, frameC = self.atualizeVar(frameA, frameB, frameC, capture) 	
            frameAHistogram = frameBHistogram
            frameBHistogram = frameCHistogram
            self.number_frame += 1
        if (ncpu == ncpus):
            self._list.append(frames_bloc / self.fps)
        elif (ncpu == 1):
            self._list.insert(0, 0)
        queue.put(self._list)
    

