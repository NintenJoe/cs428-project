##	@file FunctionTests.py
#	@author Joseph Ciurej
#	@date Winter 2014
#
#	Test File for the Global Functions in "Globals"
#
#	@TODO
#	- Write more implementation in this file!

import unittest
import os, sys
CURRENT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src")
sys.path.append(os.path.dirname(CURRENT_DIR))
import src
from src.Globals import *

##	Test case containment class for all of the test cases used in testing the
#	library functions of the 'gamelib' library.
class FunctionTests(unittest.TestCase):
	##	Ensures that the 'clamp' function properly returns a value that's 
	#	within the bounds defined by the function call.
	def test_clamp_within_bounds(self):
		result = src.Globals.clamp(1.5, 1, 2)

		self.assertEqual(result, 1.5, "Incorrect clamp value for value in bounds.")

	##	Ensures taht the 'clamp' function properly returns the lower limit for
	#	a submitted values that's below the lower limit value.
	def test_clamp_below_bounds(self):
		result = src.Globals.clamp(0, 1, 2)

		self.assertEqual(result, 1, "Incorrect clamp value for value below bounds.")

	##	Ensures taht the 'clamp' function properly returns the upper limit for
	#	a submitted values that's above the upper limit value.
	def test_clamp_above_bounds(self):
		result = src.Globals.clamp(3, 1, 2)

		self.assertEqual(result, 2, "Incorrect clamp value for value above bounds.")

	##	Asserts that the lerp function properly returns the linearly interpolated
	#	value based on the given delta.
	def test_lerp(self):
		result = src.Globals.lerp(0, 1, 0.5)

		self.assertEqual(result, 0.5, "Linear interpolation equation is incorrect.")
