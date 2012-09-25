import os
import Image
import unittest
from should_dsl import should
from videoShot import policies


class VideoSegmentationSpec(unittest.TestCase):

	def test_calculate_sizebox(self):
		policy = policies.HistogramPolicy()
		frame_path = os.path.join(os.getcwd(), 'resources/image.jpg')
		frame = Image.open(frame_path)
		policy.calculateSizeBox(frame, 2, 2) |should| equal_to([100, 119])