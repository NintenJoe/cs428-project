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
from src.InputController import *
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
        self.assertIsInstance(self.player._mntl_state.get_current_state(), IdleState)

    def test_player_update( self ):
        self.player.update(1)
        self.assertIsInstance(self.player._mntl_state.get_current_state(), IdleState)

    def test_player_transition( self ):
        self.player.notify_of( Event(EventType.KEYDOWN, {"key" : InputController.MOVE_UP}) )
        self.player.update(1)
        self.assertIsInstance(self.player._mntl_state.get_current_state(), MoveState)

    def test_player_collision( self ):
        self.player.notify_of( Event(EventType.KEYDOWN, {"key" : InputController.MOVE_UP}) )
        self.player.update(1)
        self.assertIsInstance(self.player._mntl_state.get_current_state(), MoveState)
        self.player.notify_of( Event(EventType.COLLISION, {}) )
        self.player.update(1)
        self.assertIsInstance(self.player._mntl_state.get_current_state(), IdleState)

    def test_player_stop( self ):
        self.player.notify_of( Event(EventType.KEYDOWN, {"key" : InputController.MOVE_UP}) )
        self.player.update(1)
        self.assertIsInstance(self.player._mntl_state.get_current_state(), MoveState)
        self.player.notify_of( Event(EventType.KEYUP, {"key" : InputController.MOVE_UP}) )
        self.player.update(1)
        self.assertIsInstance(self.player._mntl_state.get_current_state(), IdleState)

    def test_player_movement( self ):
        self.player.notify_of( Event(EventType.KEYDOWN, {"key" : InputController.MOVE_RIGHT}) )
        self.player.update(1)
        self.assertIsInstance(self.player._mntl_state.get_current_state(), MoveState)
        self.player.notify_of( Event(EventType.KEYDOWN, {"key" : InputController.MOVE_UP}) )
        self.player.update(1)
        self.assertIsInstance(self.player._mntl_state.get_current_state(), MoveState)
        self.player.notify_of( Event(EventType.KEYUP, {"key" : InputController.MOVE_RIGHT}) )
        self.player.update(1)
        self.assertIsInstance(self.player._mntl_state.get_current_state(), IdleState)