##  @file MoveStateTests.py
#   @author Eric Christianson
#   @date Spring 2014
#
#   Test File for the "MoveState" Type
#
#   @TODO
#   - Write the implementation in this file!

import unittest
import src
from src.MoveState import *
from src.PhysicalState import *

##  Container class for the test suite that tests the functionality of the
#   "MoveState" type.
class MoveStateTest( unittest.TestCase ):
    ### Testing Constants ###

    ##  The name identifier for the test move state used for testing.
    STATE_NAME = "test"

    ##  The time delta that will be used to test physical state updating.
    TIME_DELTA = 1.0

    ### Test Set Up/Tear Down ###

    def setUp( self ):
        self._state = MoveState( MoveStateTest.STATE_NAME, (1.0, 1.0))

    def tearDown( self ):
        self._state = None

    ### Testing Functions ###

    def test_constructor( self ):
        self.assertEqual( self._state.get_name(), "move_" + MoveStateTest.STATE_NAME,
            "Move state constructor improperly initializes name of the state." )
        self.assertEqual( self._state.get_active_time(), 0.0,
            "Move state constuctor improperly sets initial active state time." )


    def test_step_simulation( self ):
        first_change = self._state.simulate_step( MoveStateTest.TIME_DELTA )
        second_change = self._state.simulate_step( MoveStateTest.TIME_DELTA )

        self.assertTrue( first_change == second_change,
            "Simulating a step in a move state results in different changes over time." )
        self.assertEqual( first_change, PhysicalState(PG.Rect(1.0, 1.0, 0, 0), (1,1), 0.0),
            "The physical delta for each step is incorrect." )


    def test_arrival_simulation( self ):
        self._state.simulate_step( MoveStateTest.TIME_DELTA )
        self._state.simulate_step( MoveStateTest.TIME_DELTA )

        self.assertEqual( self._state.simulate_arrival(), PhysicalState(),
            "Simulating an arrival at a move state results in a non-empty physical delta." )


    def test_departure_simulation( self ):
        self._state.simulate_step( MoveStateTest.TIME_DELTA )
        self._state.simulate_step( MoveStateTest.TIME_DELTA )

        self.assertEqual( self._state.simulate_departure(), PhysicalState(),
            "Simulating a departure from a move state results in a non-empty physical delta." )

