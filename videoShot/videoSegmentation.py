import os
import shutil
import sys
import time

import Image
from cutVideo import CutVideo
from opencv.highgui import cvSaveImage, cvGetCaptureProperty, CV_CAP_PROP_FRAME_COUNT, cvQueryFrame
from multiprocessing import Process, cpu_count, Queue   

from process import VideoProcess
from shotVideo import InitExtract, ShotVideo
from temporary import Temporary
 

def videoShot(args):
	w = time.time()
	file_atual = os.getcwd()
	initExtract = InitExtract()
	videoprocess = VideoProcess()
	shotvideo = ShotVideo()
	cutvideo = CutVideo()
	temporary = Temporary()
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
	temporary_directory = temporary.createDirectory()
	print "Converting video to ogg..."
	os.system("ffmpeg -i " + FileName + " -acodec libvorbis -vcodec libtheora " + temporary_directory +"/video_converted.ogg > /dev/null 2>&1")	
	video_converted = temporary_directory +"/video_converted.ogg"
	directory = output + '/segmentation_video/'
	fileNameSave = (output + '/segmentation_video/transitions_video/')
	fileVideoSave = (output + '/segmentation_video/parts_videos/')
	fileAudioSave = (output + '/segmentation_video/video_audio/')
	for files in (directory,fileNameSave, fileVideoSave, fileAudioSave):
		try:
			shutil.rmtree(files)
		except:
			pass
		os.mkdir(files)
	#Segmenta Usando o video Ogg
	FileName = video_converted
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
	print "Finding transitions..."
	videoprocess.create_video_process(captures,sensitivity,frames_bloc,FileName,fileNameSave,fileVideoSave,file_atual,ncpus,queue_list)   
	for i in range(ncpus):
		cut_list.extend(queue_list[i].get())
	cut_list = [round(x,6) for x in cut_list]        
	corte = cutvideo.position_cut_list(cut_list,ncpus)
	print "Generating Segments..."
	videoprocess.create_cut_process(FileName,fileVideoSave,file_atual,corte,ncpus)
	os.system("cd " + fileAudioSave + "&& oggSplit " + video_converted + " > /dev/null")
	ogv_file_path = filter(lambda _file: _file.startswith('theora_'), os.listdir(fileAudioSave))[0]
	oga_file_path = filter(lambda _file: _file.startswith('vorbis_'), os.listdir(fileAudioSave))[0]
	ogv_path = os.path.join(fileAudioSave,ogv_file_path)
	oga_path = os.path.join(fileAudioSave,oga_file_path)
	os.system("rm -f " + ogv_path)
	os.system("mv " + oga_path + " " + fileAudioSave + "/" + "audio_video.oga" )
	print "Segmentation completed in : %.2f s" % (time.time() - w) 
	       
