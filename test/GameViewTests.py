##  @file GameViewTests.py
#   @author Joseph Ciurej
#   @date Spring 2014
#
#   Test File for the "GameView" Type
#
#   @TODO
#   High Priority
#   - 
#   Low Priority
#   - Update the functionality to set all functions within the `PG.display`
#     module as mocked (see http://stackoverflow.com/a/139258).

import unittest
import mock
import pygame as PG

import src
from src.GameView import *
from src.GameWorld import *

##  Container class for the test suite that tests the functionality of the
#   "GameView" type.
class GameViewTests( unittest.TestCase ):
    ### Test Set Up/Tear Down ###

    @classmethod
    def setUpClass( cls ):
        PG.display.init = mock.MagicMock()
        PG.display.quit = mock.MagicMock()

        PG.display.set_mode = mock.MagicMock()
        PG.display.set_caption = mock.MagicMock()
        PG.display.flip = mock.MagicMock()

    def setUp( self ):
        pass

    def tearDown( self ):
        pass

    ### Testing Functions ###

    def test_test( self ):
        view = GameView()
        self.assertEqual( True, True, "" )

