##	@file FunctionTests.py
#	@author Joseph Ciurej
#	@date Winter 2014
#
#	Test File for the Global Functions in the "Globals" Module
#
#	@TODO
#	- Write more tests to more fully evaluate the correctness of the 'lerp' 
#	  function.

import unittest
import src
from src.Globals import *

##	Test case containment class for all of the test cases used in testing the
#	library functions of the 'gamelib' library.
class FunctionTests( unittest.TestCase ):
	### Test Set Up/Tear Down ###

	def setUp( self ):
		pass

	def tearDown( self ):
		pass

	### Testing Functions ###

	def test_clamp_within_bounds( self ):
		result = clamp( 1.5, 1, 2 )

		self.assertEqual( result, 1.5, "Incorrect clamp value for value in bounds." )

	def test_clamp_below_bounds( self ):
		result = clamp( 0, 1, 2 )

		self.assertEqual( result, 1, "Incorrect clamp value for value below bounds." )

	def test_clamp_above_bounds( self ):
		result = clamp( 3, 1, 2 )

		self.assertEqual( result, 2, "Incorrect clamp value for value above bounds." )

	def test_lerp( self ):
		result = lerp( 0, 1, 0.5 )

		self.assertEqual( result, 0.5, "Linear interpolation equation is incorrect." )
