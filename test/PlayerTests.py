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
        self.assertIsInstance(self.player._ephm_state._state, IdleState)

    def test_player_update( self ):
        self.player.update(1)
        self.assertIsInstance(self.player._ephm_state._state, IdleState)

    def test_player_transition( self ):
        self.player.notify_of( Event(EventType.KEYDOWN, {"key" : "up"}) )
        self.player.update(1)
        self.assertIsInstance(self.player._ephm_state._state, MoveState)