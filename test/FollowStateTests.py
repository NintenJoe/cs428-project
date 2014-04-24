##  @file FollowStateTests.py
#   @author Nick Jeffrey
#   @date Spring 2014
#
#   Test File for the "FollowState" Type
#
#   @TODO
#   - 

import unittest

import src
from src.FollowState import *
from src.PhysicalState import *
from src.SimulationDelta import *
from src.CompositeHitbox import *
from src.Event import *
from src.Entity import *

##  Container class for the test suite that tests the functionality of the
#   "FollowState" type.
class FollowStateTests( unittest.TestCase ):
    ### Testing Constants ###

    ##  The name identifier for the test follow state used for testing.
    STATE_NAME = "test"

    ##  The time delta that will be used to test physical state updating.
    TIME_DELTA = 1.0

    VELOCITY = 1.0

    ### Test Set Up/Tear Down ###

    def setUp( self ):
        self._state = FollowState( FollowStateTests.STATE_NAME, FollowStateTests.VELOCITY )
        self._follow = Entity("player")

    def tearDown( self ):
        self._state = None
        self._follow = None

    ### Testing Functions ###

    def test_constructor( self ):
        self.assertEqual( self._state.get_name(), "follow_" + FollowStateTests.STATE_NAME,
            "Follow state constructor improperly initializes name of the state." )
        self.assertEqual( self._state.get_active_time(), 0.0,
            "Follow state constuctor improperly sets initial active state time." )



    def test_arrival_simulation( self ):
        self._state.simulate_step( FollowStateTests.TIME_DELTA )
        self._state.simulate_step( FollowStateTests.TIME_DELTA )

        self.assertEqual(
            self._state.simulate_arrival(Event(EventType.COLLISION, {"objects": (Entity("test"), self._follow), "volumes": (None, None)})),
            SimulationDelta( PhysicalState(CompositeHitbox(), (0.0, 0.0), 0.0) ),
            "Simulating an arrival at a follow state results in a non-empty physical delta."
        )

        self.assertEqual(self._state._follow, self._follow)



    def test_departure_simulation( self ):
        self._state.simulate_step( FollowStateTests.TIME_DELTA )
        self._state.simulate_step( FollowStateTests.TIME_DELTA )

        self.assertEqual(
            self._state.simulate_departure(),
            SimulationDelta(PhysicalState(CompositeHitbox(), (0.0, 0.0), 0.0)),
            "Simulating a departure from a follow state results in a non-empty physical delta."
        )

    def test_step_simulation( self ):
        self._state.simulate_arrival(Event(EventType.COLLISION, {"objects": (Entity("test"), self._follow), "volumes": (None, None)}))
        first_change = self._state.simulate_step( FollowStateTests.TIME_DELTA )
        second_change = self._state.simulate_step( FollowStateTests.TIME_DELTA )

        self.assertTrue( first_change == second_change,
            "Simulating a step in a follow state results in different changes over time." )
        self.assertEqual( first_change,
            SimulationDelta( PhysicalState(CompositeHitbox(0.0, 0.0), (0,0), 0.0) ),
            "The physical delta for each step is incorrect." )
