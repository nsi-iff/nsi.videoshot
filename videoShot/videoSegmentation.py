import os
import shutil
import sys
import Image
import time
from shotVideo import InitExtract, ShotVideo
from cutVideo import CutVideo
from opencv.highgui import cvSaveImage, cvGetCaptureProperty, CV_CAP_PROP_FRAME_COUNT, cvQueryFrame
from multiprocessing import Process, cpu_count, Queue   
from process import VideoProcess

 
def videoShot(args):
	w = time.time()
	file_atual = os.getcwd()
	initExtract = InitExtract()
	videoprocess = VideoProcess()
	shotvideo = ShotVideo()
	cutvideo = CutVideo()
	captures = {}
	cut_list=[]
	sensitivity = 0.35
	ncpus = cpu_count()
	queue_list=[]
	try:
		FileName = args[args.index('-i') + 1]
		output = args[args.index('-o') + 1]
	except ValueError:
		sys.exit('Usage: videoShot -i <inputFile> -o <outputDirectory>')
	fileNameSave = (output + '/transitions_' + 'video' + '/')
	fileVideoSave = (output + '/parts_' + 'video'+'/')
	for files in (fileNameSave, fileVideoSave):
		try:
			shutil.rmtree(files)
		except:
			pass
		os.mkdir(files)
	capture = initExtract.createCapture(FileName)
	total_frames = cvGetCaptureProperty(capture, CV_CAP_PROP_FRAME_COUNT)
	# if utilizado para quando o video nao possui o metadado de total frame
	if total_frames == 0:
		total_frames = shotvideo.contFrames(capture)
	frames_bloc = int(total_frames / ncpus)
	captures[1] = initExtract.createCapture(FileName)
	cvSaveImage(fileNameSave + 'trans_time_1.jpg', initExtract.initFrameCapture(captures[1]))
	for i in range(2, ncpus + 1):
		captures[i] = initExtract.createCapture(FileName)
		captures[i] = initExtract.pass_frames(captures[i], frames_bloc, i - 1)
	j = time.time()		
	videoprocess.create_video_process(captures,sensitivity,frames_bloc,FileName,fileNameSave,fileVideoSave,file_atual,ncpus,queue_list)   
	for i in range(ncpus):
		cut_list.extend(queue_list[i].get())
	cut_list = [round(x,6) for x in cut_list]        
	corte = cutvideo.position_cut_list(cut_list,ncpus)
	videoprocess.create_cut_process(FileName,fileVideoSave,file_atual,corte,ncpus)
	print "A segmentacao foi concluida em : %.2f segundos " % (time.time() - w) 
	       
