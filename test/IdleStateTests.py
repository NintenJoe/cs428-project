##  @file IdleStateTests.py
#   @author Joseph Ciurej
#   @date Spring 2014
#
#   Test File for the "IdleState" Type
#
#   @TODO
#   - Write the implementation in this file!

import unittest
import src
from src.IdleState import *
from src.PhysicalState import *

##  Container class for the test suite that tests the functionality of the
#   "IdleState" type.
class IdleStateTest( unittest.TestCase ):
    ### Testing Constants ###

    ##  The name identifier for the test idle state used for testing.
    STATE_NAME = "test"

    ##  The time delta that will be used to test physical state updating.
    TIME_DELTA = 1.0

    ### Test Set Up/Tear Down ###

    def setUp( self ):
        self._state = IdleState( IdleStateTest.STATE_NAME )

    def tearDown( self ):
        self._state = None

    ### Testing Functions ###

    def test_constructor( self ):
        self.assertEqual( self._state.get_name(), "idle_" + IdleStateTest.STATE_NAME,
            "Idle state constructor improperly initializes name of the state." )
        self.assertEqual( self._state.get_active_time(), 0.0,
            "Idle state constuctor improperly sets initial active state time." )


    def test_step_simulation( self ):
        first_change = self._state.simulate_step( IdleStateTest.TIME_DELTA )
        second_change = self._state.simulate_step( IdleStateTest.TIME_DELTA )

        self.assertTrue( first_change == second_change,
            "Simulating a step in an idle state results in different changes over time." )
        self.assertEqual( first_change, PhysicalState(),
            "Each step simulated in an idle state results in a non-empty physical delta." )


    def test_arrival_simulation( self ):
        self._state.simulate_step( IdleStateTest.TIME_DELTA )
        self._state.simulate_step( IdleStateTest.TIME_DELTA )

        self.assertEqual( self._state.simulate_arrival(), PhysicalState(),
            "Simulating an arrival at an idle state results in a non-empty physical delta." )


    def test_departure_simulation( self ):
        self._state.simulate_step( IdleStateTest.TIME_DELTA )
        self._state.simulate_step( IdleStateTest.TIME_DELTA )

        self.assertEqual( self._state.simulate_departure(), PhysicalState(),
            "Simulating a departure from an idle state results in a non-empty physical delta." )

