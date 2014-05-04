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
from src.Globals import *
from src.Entity import *
from src.IdleState import *
from src.MoveState import *

class PlayerTest( unittest.TestCase ):

    ### Test Set Up/Tear Down ###

    def setUp( self ):
        self.player = Entity("player")

    def tearDown( self ):
        self.player = None

    ### Testing Functions ###

    def test_player_constructor( self ):
        self.assertIsInstance(self.player._mntl_state.get_current_state(), IdleState,
            "Player does not begin in correct state")

    def test_player_update( self ):
        self.player.update(1)
        self.assertIsInstance(self.player._mntl_state.get_current_state(), IdleState,
            "Player transitions when it should not")

    def test_player_transition( self ):
        self.player.notify_of( Event(EventType.KEYDOWN, {"key" : MOVE_UP}) )
        self.player.update(1)
        self.assertIsInstance(self.player._mntl_state.get_current_state(), MoveState,
            "Player does not transition from idle into move on key up pressed")

    def test_player_collision( self ):
        self.player.notify_of( Event(EventType.KEYDOWN, {"key" : MOVE_UP}) )
        self.player.update(1)
        self.assertIsInstance(self.player._mntl_state.get_current_state(), MoveState,
            "Player does not transition from idle into move on key up pressed")
        self.player.notify_of( Event(EventType.COLLISION, {}) )
        self.player.update(1)
        self.assertIsInstance(self.player._mntl_state.get_current_state(), IdleState,
            "Player does not transition from move into idle on collision")

    def test_player_stop( self ):
        self.player.notify_of( Event(EventType.KEYDOWN, {"key" : MOVE_UP}) )
        self.player.update(1)
        self.assertIsInstance(self.player._mntl_state.get_current_state(), MoveState,
            "Player does not transition from idle into move on key up pressed")
        self.player.notify_of( Event(EventType.KEYUP, {"key" : MOVE_UP}) )
        self.player.update(1)
        self.assertIsInstance(self.player._mntl_state.get_current_state(), IdleState,
            "Player does not transition from move into idle on key up released")

    def test_player_movement( self ):
        self.player.notify_of( Event(EventType.KEYDOWN, {"key" : MOVE_RIGHT}) )
        self.player.update(1)
        self.assertIsInstance(self.player._mntl_state.get_current_state(), MoveState,
            "Player does not transition from idle into move on key right pressed")
        self.player.notify_of( Event(EventType.KEYDOWN, {"key" : MOVE_UP}) )
        self.player.update(1)
        self.assertIsInstance(self.player._mntl_state.get_current_state(), MoveState,
            "Player does not transition from move into move on key up pressed")
        self.player.notify_of( Event(EventType.KEYUP, {"key" : MOVE_RIGHT}) )
        self.player.update(1)
        self.assertIsInstance(self.player._mntl_state.get_current_state(), MoveState,
            "Player does not transition from move into move on key right pressed")
