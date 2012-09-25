import os
import commands
import tempfile
import shutil
import unittest
from should_dsl import should
from videoShot import videoSegmentation


class VideoSegmentationSpec(unittest.TestCase):

	def get_mimetype(self, path_file):
		return commands.getoutput('mimetype ' + path_file).split(':')[-1][1:]

	def test_video_convert(self):
		temp = tempfile.mkdtemp()
		input_video_path = os.path.join(os.getcwd(), 'resources/test-part.avi')
		videoSegmentation.convert_video_to_ogg(input_video_path, temp)
		output_video_path = os.path.join(temp, '/video_converted.ogg')
		self.get_mimetype(output_video_path) |should| equal_to('video/x-theora+ogg')
		shutil.rmtree(temp)

	def test_get_output_audio(self):
		path_audio_save = tempfile.mkdtemp()
		input_video_path = os.path.join(os.getcwd(), 'resources/test-part.ogv')
		videoSegmentation.get_output_audio(path_audio_save, input_video_path)
		path_audio_file = os.path.join(path_audio_save, 'audio_video.oga')
		self.get_mimetype(path_audio_file) |should| equal_to('audio/x-vorbis+ogg')
		shutil.rmtree(path_audio_save)		