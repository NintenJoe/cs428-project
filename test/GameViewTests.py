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

import src
from src.Globals import *
from src.GameView import *
from src.GameWorld import *

##  Container class for the test suite that tests the functionality of the
#   "GameView" type.
class GameViewTests( unittest.TestCase ):
    ### Test Set Up/Tear Down ###

    def setUp( self ):
        self._patchers = [
            mock.patch("pygame.display.set_mode"),
            mock.patch("pygame.display.set_caption"),
            mock.patch("pygame.display.flip"),
        ]
        self._setmode_mock = self._patchers[ 0 ].start()
        self._setcapt_mock = self._patchers[ 1 ].start()
        self._flip_mock = self._patchers[ 2 ].start()

        self._view = GameView()

    def tearDown( self ):
        self._view = None
        self._setmode_mock = None
        self._setcapt_mock = None
        self._flip_mock = None

        [ patcher.stop() for patcher in self._patchers ]

    ### Testing Functions ###

    def test_initialization( self ):
        self._setmode_mock.assert_called_once_with( (640, 480) )
        self._setcapt_mock.assert_called_once_with( GAME_NAME )

