import os
import Image
import unittest
from should_dsl import should
from videoShot import policies


class HistogramPolicySpec(unittest.TestCase):

	def setUp(self):
		self.policy = policies.HistogramPolicy()

	def test_calculate_sizebox(self):
		frame_path = os.path.join(os.getcwd(), 'resources/image.jpg')
		frame = Image.open(frame_path)
		self.policy.calculateSizeBox(frame, 2, 2) |should| equal_to([100, 119])

	def test_calculateSensitivity(self):
		frame_path = os.path.join(os.getcwd(), 'resources/image.jpg')
		frame = Image.open(frame_path)
		self.policy.calculateSensitivity(0.1, frame) |should| equal_to(4760)