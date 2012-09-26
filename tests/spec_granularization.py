import os
import tempfile
import Image
import unittest
from should_dsl import should
from videoShot import videoSegmentation


class SegmentationSpec(unittest.TestCase):

	def test_granularization(self):
		temp = tempfile.mkdtemp()
		input_video_path = os.path.join(os.getcwd(), 'resources/test.avi')
		videoSegmentation.video_shot(['videoShot', '-i', input_video_path, '-o', temp])
		len(os.listdir(os.path.join(temp + '/segmentation_video/parts_videos'))) |should| equal_to(7)
		len(os.listdir(os.path.join(temp + '/segmentation_video/thumbnails'))) |should| equal_to(7)
		len(os.listdir(os.path.join(temp + '/segmentation_video/transitions_video'))) |should| equal_to(23)
		len(os.listdir(os.path.join(temp + '/segmentation_video/video_audio'))) |should| equal_to(1)