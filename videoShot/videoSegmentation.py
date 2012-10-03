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

def convert_video_to_ogg(file_input_name, temporary_directory):
    file_input_name = file_input_name.replace(" ", "\ ")
    os.system("ffmpeg -i " + file_input_name + " -acodec libvorbis -vcodec libtheora " + temporary_directory +"/video_converted.ogg > /dev/null 2>&1")  

def create_directory(directories):
    for files in (directories):
        try:
            shutil.rmtree(files)
        except:
            pass
        os.mkdir(files)
    
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

def get_video_duration(filePath):
    filePath = filePath.replace(" ", "\ ")
    time = commands.getoutput("ffmpeg -i " + filePath + " 2>&1 | grep Duration")
    time = time[12:20].split(':')
    return (int(time[0]) * 3600) + (int(time[1]) * 60) + (int(time[2]))

def get_videos_path(tempdir):
    list_videos = filter(lambda _file: _file.startswith('video__'), os.listdir(tempdir))
    list_videos.sort()
    list_path = []
    for n in range(len(list_videos)):
        list_path.append(str(os.path.join(tempdir, list_videos[n])))
    return list_path

def split_video(temporary_directory, ncpus, video_duration, ogg_video_path):
    remainder = video_duration % ncpus 
    cut_time = (video_duration - remainder) / ncpus
    cut_list = []
    for n in range(ncpus):
        cut_list.append(cut_time * n)
    cut_list.append(video_duration)
    for n in range(ncpus):
        os.system('ffmpeg -i ' + ogg_video_path + ' -acodec copy -vcodec copy -ss ' + str(cut_list[n]) + ' -t ' + str(cut_list[n+1] - cut_list[n]) + ' ' + temporary_directory + '/video__' + str(n+1) + '.ogv > /dev/null 2>&1')

def get_video_thumbnails(videos_path, thumbnails_save_path, size='160x120'):
    for n, video_path in enumerate(os.listdir(videos_path)):
        os.system("cd " + videos_path + " && ffmpeg  -itsoffset -4  -i " + video_path + " -vcodec mjpeg -vframes 1 -an -f rawvideo -s " + 
                size + " " + thumbnails_save_path + "/thumbnail" + str(n) + ".jpg > /dev/null 2>&1")

def video_shot(args):
    start_time = time.time()
    captures = {}
    cut_list = []
    cut_video = CutVideo()
    init_extract = InitExtract()
    ncpus = cpu_count()
    queue_list = []
    sensitivity = 0.35
    temporary = Temporary()
    video_process = VideoProcess()
    try:
        file_input_name = args[args.index('-i') + 1]
        output_directory = args[args.index('-o') + 1]
    except ValueError:
        sys.exit('Usage: videoShot -i <inputFile> -o <outputDirectory>')
    temporary_directory = temporary.createDirectory()
    print "Converting video to ogg..."
    start_time2 = time.time()
    convert_video_to_ogg(file_input_name, temporary_directory)
    start_time3 = time.time()
    ogg_video_path = os.path.join(temporary_directory, "video_converted.ogg")
    output_segmentation_directory = output_directory + '/segmentation_video/'
    file_name_save = (output_segmentation_directory + '/transitions_video/')
    file_video_save = (output_segmentation_directory + '/parts_videos/')
    file_audio_save = (output_segmentation_directory + '/video_audio/')
    thumbnails_save_path = (output_segmentation_directory + '/thumbnails/')
    create_directory([output_segmentation_directory, file_name_save, file_video_save, file_audio_save, thumbnails_save_path])
    file_input_name = ogg_video_path
    capture = init_extract.createCapture(file_input_name)
    video_duration = get_video_duration(ogg_video_path)
    fps = cvGetCaptureProperty(capture, CV_CAP_PROP_FPS)
    total_frames = round(video_duration * fps, 0)
    frames_bloc = int(total_frames / ncpus)
    split_video(temporary_directory, ncpus, video_duration, ogg_video_path)
    list_videos_path = get_videos_path(temporary_directory)
    captures[1] = init_extract.createCapture(list_videos_path[0])
    cvSaveImage(file_name_save + 'trans_time_1.jpg', init_extract.initFrameCapture(captures[1]))
    for i in range(2, ncpus + 1):
        captures[i] = init_extract.createCapture(list_videos_path[i-1])
    print "Finding transitions..."
    video_process.create_video_process(captures, sensitivity, frames_bloc, file_input_name, file_name_save, file_video_save, ncpus, queue_list)   
    for i in range(ncpus):
        cut_list.extend(queue_list[i].get())
    cut_list = [round(x,6) for x in cut_list]        
    time_cut_list = cut_video.position_cut_list(cut_list, ncpus)
    print "Generating Segments..."
    video_process.create_cut_process(file_input_name, file_video_save, time_cut_list, ncpus)
    get_output_audio(file_audio_save, ogg_video_path)
    get_video_thumbnails(file_video_save, thumbnails_save_path)
    temporary.removeDirectory(temporary_directory)
    print 
    print "Conversion Time: %.2f s" % (start_time3 - start_time2)
    print "Segmentation Time: %.2f s" % ((time.time() - start_time) - (start_time3 - start_time2)) 
    print "Segmentation completed in : %.2f s" % (time.time() - start_time) 
           
