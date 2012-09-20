import os
import shutil
import Image
import time
from shotVideo import ShotVideo, InitExtract
from cutVideo import CutVideo
from opencv.highgui import cvSaveImage, cvGetCaptureProperty, CV_CAP_PROP_FRAME_COUNT, cvQueryFrame
from multiprocessing import Process, cpu_count, Queue 

class VideoProcess(object):
 
    
    def create_video_process(self, captures, sensitivity, frames_bloc, FileName, fileNameSave, fileVideoSave, file_atual, ncpus, queue_list):
        shotvideo = ShotVideo()
        processos = {}
        for i in range(1, ncpus + 1):
            queue_list.append(Queue())
            if i == 1:
                number_frame = 27
            else:
                number_frame = frames_bloc * (i - 1)	    	
            processos[i] = Process(target = shotvideo.shotDetect, args = (queue_list[i-1],captures[i], \
                sensitivity, number_frame, frames_bloc * i + 1, FileName, fileNameSave, fileVideoSave, file_atual, i, ncpus))
        self.start_video_process(processos,ncpus)
    
    def start_video_process(self,processos,ncpus):
        for i in range(1,ncpus+1):   
            processos[i].start()
        for i in range(1,ncpus+1):   
            processos[i].join()
            
    def create_cut_process(self,FileName,fileVideoSave,file_atual,corte,ncpus):
        cutvideo = CutVideo()
        processos2 = {}
        for i in range(1,ncpus+1):
            processos2[i]=Process(target=cutvideo.cut_video, args=(FileName, fileVideoSave, file_atual,corte[i-1],i))  
        self.start_cut_process(processos2,ncpus)
 
    def start_cut_process(self,processos2,ncpus):
        for i in range(1,ncpus+1):   
            processos2[i].start()
        for i in range(1,ncpus+1):   
            processos2[i].join()
    
    
