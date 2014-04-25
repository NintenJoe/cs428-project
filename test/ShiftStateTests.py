##  @file ShiftStateTests.py
#   @author Nick Jeffrey
#   @date Spring 2014
#
#   Test File for the "ShiftState" Type
#
#   @TODO
#   - 

import unittest
import src
from src.ShiftState import *
from src.SimulationDelta import *

##  Container class for the test suite that tests the functionality of the
#   "ShiftState" type.
class ShiftStateTests( unittest.TestCase ):
    ### Testing Constants ###

    ##  The name identifier for the test shift state used for testing.
    STATE_NAME = "test"

    ##  The time delta that will be used to test physical state updating.
    TIME_DELTA = 1.0

    ### Test Set Up/Tear Down ###

    def setUp( self ):
        self._state = ShiftState( ShiftStateTests.STATE_NAME, 0.0, 0.0 )
        self._state2 = ShiftState( ShiftStateTests.STATE_NAME, 1, 2 )

    def tearDown( self ):
        self._state = None
        self._state2 = None

    ### Testing Functions ###

    def test_constructor( self ):
        self.assertEqual( self._state.get_name(), "idle_" + ShiftStateTests.STATE_NAME,
            "Shift state constructor improperly initializes name of the state." )
        self.assertEqual( self._state.get_active_time(), 0.0,
            "Shift state constuctor improperly sets initial active state time." )
        self.assertEqual( self._state._xchange, 0.0,
            "Shift state constuctor improperly sets initial x change." )
        self.assertEqual( self._state._ychange, 0.0,
            "Shift state constuctor improperly sets initial y change." )


    def test_step_simulation( self ):
        first_change = self._state.simulate_step( ShiftStateTests.TIME_DELTA )
        second_change = self._state.simulate_step( ShiftStateTests.TIME_DELTA )

        self.assertTrue( first_change == second_change,
            "Simulating a step in a Shift state results in different changes over time." )
        self.assertEqual( first_change, SimulationDelta(),
            "Each step simulated in a Shift state results in a non-empty physical delta." )


    def test_arrival_simulation( self ):
        self._state.simulate_step( ShiftStateTests.TIME_DELTA )
        self._state.simulate_step( ShiftStateTests.TIME_DELTA )

        self.assertEqual( self._state.simulate_arrival(), SimulationDelta(),
            "Simulating an arrival at a Shift state with no shift results in a non-zero delta." )

        self._state2.simulate_step( ShiftStateTests.TIME_DELTA )
        self._state2.simulate_step( ShiftStateTests.TIME_DELTA )

        self.assertEqual( self._state2.simulate_arrival().get_entity_delta().get_volume().get_position(), (1,2),
            "Simulating an arrival at a Shift state with shift results in a zero delta." )


    def test_departure_simulation( self ):
        self._state.simulate_step( ShiftStateTests.TIME_DELTA )
        self._state.simulate_step( ShiftStateTests.TIME_DELTA )

        self.assertEqual( self._state.simulate_departure(), SimulationDelta(),
            "Simulating a departure from a Shift state with no shift results in a non-zero delta." )

        self._state2.simulate_step( ShiftStateTests.TIME_DELTA )
        self._state2.simulate_step( ShiftStateTests.TIME_DELTA )

        self.assertEqual( self._state2.simulate_departure().get_entity_delta().get_volume().get_position(), (-1,-2),
            "Simulating a departure from a Shift state with shift results in a zero delta." )

