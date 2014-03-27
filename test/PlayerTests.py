##  @file PlayerTests.py
#   @author Nick Jeffrey
#   @date Spring 2014
#
#   Test File for the "Player" Type
#
#   @TODO
#   - Cover at least 90% of code in Player and Entity
import unittest
import src
from src.Player import *

class PlayerTest( unittest.TestCase ):

    ### Test Set Up/Tear Down ###

    def setUp( self ):
        self.player = Player("player")

    def tearDown( self ):
        self.player = None

    ### Testing Functions ###

    def test_player_constructor( self ):
        pass