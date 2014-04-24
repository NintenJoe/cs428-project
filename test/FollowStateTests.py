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
        self._pos = Entity("monster")

    def tearDown( self ):
        self._state = None
        self._follow = None
        self._pos = None

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
            self._state.simulate_arrival(Event(EventType.COLLISION, {"objects": (self._pos, self._follow), "volumes": (None, None)})),
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

    def test_step_no_follow( self ):
        first_change = self._state.simulate_step( FollowStateTests.TIME_DELTA )
        second_change = self._state.simulate_step( FollowStateTests.TIME_DELTA )

        self.assertTrue( first_change == second_change,
            "Simulating a step in a follow state results in different changes over time." )
        self.assertEqual( first_change,
            SimulationDelta( PhysicalState(CompositeHitbox(0.0, 0.0), (0,0), 0.0) ),
            "The physical delta for each step is incorrect." )

    def test_step_same_position( self ):
        self._state.simulate_arrival(Event(EventType.COLLISION, {"objects": (self._pos, self._follow), "volumes": (None, None)}))
        first_change = self._state.simulate_step( FollowStateTests.TIME_DELTA )
        second_change = self._state.simulate_step( FollowStateTests.TIME_DELTA )

        self.assertTrue( first_change == second_change,
            "Simulating a step in a follow state results in different changes over time." )
        self.assertEqual( first_change,
            SimulationDelta( PhysicalState(CompositeHitbox(0.0, 0.0), (0,0), 0.0) ),
            "The physical delta for each step is incorrect." )

    def test_step_right( self ):
        self._state.simulate_arrival(Event(EventType.COLLISION, {"objects": (self._pos, self._follow), "volumes": (None, None)}))
        self._follow.get_chitbox().get_bounding_box().x += 2
        change = self._state.simulate_step( FollowStateTests.TIME_DELTA * 2 )

        self.assertEqual( change,
            SimulationDelta( PhysicalState(CompositeHitbox(2.0, 0.0), (0,0), 0.0) ),
            str(self._follow.get_chitbox().get_bounding_box().x) + " != " + str(self._pos.get_chitbox().get_bounding_box().x) )

    def test_step_down_left( self ):
        self._state.simulate_arrival(Event(EventType.COLLISION, {"objects": (self._pos, self._follow), "volumes": (None, None)}))
        self._follow.get_chitbox().get_bounding_box().x -= 8
        self._pos.get_chitbox().get_bounding_box().y -= 6
        first_change = self._state.simulate_step( FollowStateTests.TIME_DELTA * 5)

        self.assertEqual( first_change,
            SimulationDelta( PhysicalState(CompositeHitbox(-4.0, 3.0), (0,0), 0.0) ),
            str(first_change.get_entity_delta().get_volume().get_position()) + " != (-4, 3)" )