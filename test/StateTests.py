##  @file StateTests.py
#   @author Joseph Ciurej
#   @date Spring 2014
#
#   Test File for the "State" Type
#
#   @TODO
#   - Add tests for the timeout functionality added to states!

import unittest
import src
from src.State import *
from src.PhysicalState import *

##  Testing class that overrides the abstract "State" class with the most
#   basic functionality.
#class 

##  Container class for the test suite that tests the functionality of the
#   "State" type.
class StateTests( unittest.TestCase ):
    ### Test Set Up/Tear Down ###

    def setUp( self ):
        pass

    def tearDown( self ):
        pass

    ### Testing Functions ###

    def test_test( self ):
        self.assertEqual( True, True, "" )

