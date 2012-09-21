import os
import shutil
import sys
import time
import commands

import Image
from cutVideo import CutVideo
from opencv.highgui import cvSaveImage, cvGetCaptureProperty, CV_CAP_PROP_FRAME_COUNT, CV_CAP_PROP_FPS, cvQueryFrame
from multiprocessing import Process, cpu_count, Queue   

from process import VideoProcess
from shotVideo import InitExtract
from temporary import Temporary

def get_video_duration(filePath):
        time = commands.getoutput("ffmpeg -i " + filePath + " 2>&1 | grep Duration")
        time = time[12:20].split(':')
        return (int(time[0]) * 3600) + (int(time[1]) * 60) + (int(time[2]))

def create_directory(output_segmentation_directory, file_name_save, file_video_save, file_audio_save):
	for files in (output_segmentation_directory, file_name_save, file_video_save, file_audio_save):
		try:
			shutil.rmtree(files)
		except:
			pass
		os.mkdir(files)
	
def convert_video_to_ogg(file_input_name, temporary_directory):
	os.system("ffmpeg -i " + file_input_name + " -acodec libvorbis -vcodec libtheora " + temporary_directory +"/video_converted.ogg > /dev/null 2>&1")	

def get_output_audio(file_audio_save, ogg_video_path):
	os.system("cd " + file_audio_save + "&& oggSplit " + ogg_video_path + " > /dev/null")
	codec_list_ex = ['theora_','vorbis_']
	ogg_paths = []
	list_files = []
	for i in range(len(codec_list_ex)):
		list_files.append(filter(lambda _file: _file.startswith(codec_list_ex[i]), os.listdir(file_audio_save))[0])
		ogg_paths.append(os.path.join(file_audio_save, list_files[i]))
	os.system("rm -f " + ogg_paths[0])
	os.system("mv " + ogg_paths[1] + " " + file_audio_save + "/" + "audio_video.oga" )

def video_shot(args):
	captures = {}
	cut_list = []
	cut_video = CutVideo()
	init_extract = InitExtract()
	ncpus = cpu_count()
	queue_list = []
	sensitivity = 0.35
	start_time = time.time()
	temporary = Temporary()
	video_process = VideoProcess()
	try:
		file_input_name = args[args.index('-i') + 1]
		output_directory = args[args.index('-o') + 1]
	except ValueError:
		sys.exit('Usage: videoShot -i <inputFile> -o <outputDirectory>')
	temporary_directory = temporary.createDirectory()
	print "Converting video to ogg..."
	convert_video_to_ogg(file_input_name, temporary_directory)
	ogg_video_path = temporary_directory + "/video_converted.ogg"
	output_segmentation_directory = output_directory + '/segmentation_video/'
	file_name_save = (output_segmentation_directory + '/transitions_video/')
	file_video_save = (output_segmentation_directory + '/parts_videos/')
	file_audio_save = (output_segmentation_directory + '/video_audio/')
	create_directory(output_segmentation_directory, file_name_save, file_video_save, file_audio_save)
	file_input_name = ogg_video_path
	capture = init_extract.createCapture(file_input_name)
	fps = cvGetCaptureProperty(capture, CV_CAP_PROP_FPS)
	total_frames = round(get_video_duration(ogg_video_path) * fps, 0)
	frames_bloc = int(total_frames / ncpus)
	captures[1] = init_extract.createCapture(file_input_name)
	cvSaveImage(file_name_save + 'trans_time_1.jpg', init_extract.initFrameCapture(captures[1]))
	for i in range(2, ncpus + 1):
		captures[i] = init_extract.createCapture(file_input_name)
		captures[i] = init_extract.pass_frames(captures[i], frames_bloc, i - 1)
	print "Finding transitions..."
	video_process.create_video_process(captures, sensitivity, frames_bloc, file_input_name, file_name_save, file_video_save, ncpus, queue_list)   
	for i in range(ncpus):
		cut_list.extend(queue_list[i].get())
	cut_list = [round(x,6) for x in cut_list]        
	time_cut_list = cut_video.position_cut_list(cut_list, ncpus)
	print "Generating Segments..."
	video_process.create_cut_process(file_input_name, file_video_save, time_cut_list, ncpus)
	get_output_audio(file_audio_save, ogg_video_path)
	print "Segmentation completed in : %.2f s" % (time.time() - start_time) 
	       
