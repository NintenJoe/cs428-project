##  @file monsterTests.py
#   @author Nick Jeffrey
#   @date Spring 2014
#
#   Test File for the "Monster" Type
#
#   @TODO
#   - Cover at least 90% of code in Monster
import unittest
import src
from src.Monster import *

class MonsterTest( unittest.TestCase ):

    ### Test Set Up/Tear Down ###

    def setUp( self ):
        self.monster = Monster("monster")

    def tearDown( self ):
        self.monster = None

    ### Testing Functions ###

    def test_monster_constructor( self ):
        self.assertIsInstance(self.monster._mntl_state.get_current_state(), IdleState)

    def test_monster_update( self ):
        self.monster.update(1)
        self.assertIsInstance(self.monster._mntl_state.get_current_state(), IdleState)

    def test_monster_transition( self ):
        self.monster.update(self.monster.timeout)
        self.monster.update(1)
        self.assertIsInstance(self.monster._mntl_state.get_current_state(), MoveState)

    def test_monster_collision( self ):
        self.monster.update(self.monster.timeout)
        self.monster.update(1)
        self.assertIsInstance(self.monster._mntl_state.get_current_state(), MoveState)
        self.monster.notify_of( Event(EventType.COLLISION, {}) )
        self.monster.update(1)
        self.assertIsInstance(self.monster._mntl_state.get_current_state(), IdleState)

    def test_monster_movement( self ):
        self.monster.update(self.monster.timeout)
        self.monster.update(1)
        self.assertIsInstance(self.monster._mntl_state.get_current_state(), MoveState)
        self.monster.update(1)
        self.monster.update(1)
        self.monster.update(1)
        self.assertIsInstance(self.monster._mntl_state.get_current_state(), MoveState)
        self.monster.update(self.monster.timeout-4)
        self.monster.update(1)
        self.monster.update(1)
        self.assertIsInstance(self.monster._mntl_state.get_current_state(), IdleState)