##  @file EntityTests.py
#   @author Joseph Ciurej
#   @date Spring 2014
#
#   Test File for the "Entity" Type
#
#   @TODO
#   High Priority:
#   - Update the 'TestStates' reference in this testing file once the location
#     of this file changes.
#   - Update the 'TestEntities' reference in this testing file once the location
#     of this file changes.
#   Low Priority:
#   - It may be worthwhile to add a test with state machine timeouts, but these
#     should be handled properly assuming that the 'StateMachine' class works.
#   - Update the 'status' testing function to either be more complete or to
#     change based on the needs of the 'Entity' class.

import unittest
import src
from TestEntities import *
from TestStates import *

from src.Entity import *
from src.StateMachine import *
from src.State import *
from src.Transition import *

from src.Event import *
from src.PhysicalState import *
from src.SimulationDelta import *
from src.CompositeHitbox import *

##  Container class for the test suite that tests the functionality of the
#   "Entity" type.
class EntityTests( unittest.TestCase ):
    ### Testing Constants ###

    ##  The name given to the test "Entity" created in the contained tests.
    ENTITY_NAME = "test"

    ##  The physical delta used to initialize the test "Entity" in the value
    #   constructor based tests.
    ENTITY_DELTA = PhysicalState( volume=CompositeHitbox(4, 3), velocity=(2, -1), mass=2.0, curr_health=-1 )

    ##  The time delta used for update testing on the test "Entity" objects.
    TIME_DELTA = 1.0

    ### Test Set Up/Tear Down ###

    def setUp( self ):
        self._entity = SimpleTestEntity(
            EntityTests.ENTITY_NAME,
            EntityTests.ENTITY_DELTA
        )

    def tearDown( self ):
        self._entity = None

        # TODO: This is a bit of a hack to reset all the state timers.  While
        # not a terrible solution, this could certainly be improved.
        [ state.simulate_arrival() for state in SimpleTestEntity.MACHINE_STATES ]

    ### Testing Functions ###

    def test_default_constructor_initialization( self ):
        default_entity = SimpleTestEntity( EntityTests.ENTITY_NAME )

        self.assertEqual(
            default_entity.get_name(),
            EntityTests.ENTITY_NAME,
            "Default entity constructor improperly initializes entity name."
        )
        self.assertEqual(
            set( default_entity.get_mental_state().get_states() ),
            set( SimpleTestEntity.MACHINE_STATES ),
            "Default entity constructor improperly initializes machine states."
        )
        self.assertEqual(
            set( default_entity.get_mental_state().get_transitions() ),
            set( SimpleTestEntity.MACHINE_TRANS ),
            "Default entity constructor improperly initializes machine transitions."
        )
        self.assertEqual(
            default_entity.get_physical_state(),
            SimpleTestEntity.INITIAL_PHYSICAL,
            "Default entity constructor improperly initializes physical state."
        )


    def test_value_constructor_initialization( self ):
        self.assertEqual(
            self._entity.get_name(),
            EntityTests.ENTITY_NAME,
            "Value entity constructor improperly initializes entity name."
        )
        self.assertEqual(
            set( self._entity.get_mental_state().get_states() ),
            set( SimpleTestEntity.MACHINE_STATES ),
            "Value entity constructor improperly initializes machine states."
        )
        self.assertEqual(
            set( self._entity.get_mental_state().get_transitions() ),
            set( SimpleTestEntity.MACHINE_TRANS ),
            "Value entity constructor improperly initializes machine transitions."
        )

        soln_physstate = PhysicalState()
        soln_physstate.add_delta( SimpleTestEntity.INITIAL_PHYSICAL )
        soln_physstate.add_delta( EntityTests.ENTITY_DELTA )

        self.assertEqual(
            self._entity.get_physical_state(),
            soln_physstate,
            "Value entity constructor improperly initializes physical state."
        )


    def test_value_constructor_independence( self ):
        test_physstate = PhysicalState()
        test_physstate.add_delta( SimpleTestEntity.INITIAL_PHYSICAL )

        value_entity = SimpleTestEntity( EntityTests.ENTITY_NAME, test_physstate )
        test_physstate.add_delta( SimpleTestEntity.INITIAL_PHYSICAL )

        self.assertNotEqual(
            value_entity.get_physical_state(),
            test_physstate,
            "Value entity constructor isn't independent of initial delta parameter."
        )

    def test_update_without_events( self ):
        pre_state = self._entity.get_mental_state().get_current_state()
        events = self._entity.update( EntityTests.TIME_DELTA )
        post_state = self._entity.get_mental_state().get_current_state()

        self.assertEqual(
            pre_state,
            post_state,
            "Updates without events improperly change entity mental state."
        )
        self.assertEqual(
            events,
            SimpleTestState.STEP_DELTA.get_events(),
            "Updates without events return improper event listings."
        )

        soln_physstate = PhysicalState()
        soln_physstate.add_delta( SimpleTestEntity.INITIAL_PHYSICAL )
        soln_physstate.add_delta( EntityTests.ENTITY_DELTA )
        soln_physstate.add_delta( SimpleTestState.STEP_DELTA.get_entity_delta() )
        soln_physstate.update( EntityTests.TIME_DELTA )

        self.assertEqual(
            self._entity.get_physical_state(),
            soln_physstate,
            "Updates without events improperly update the entity's physical state."
        )


    def test_update_with_events( self ):
        initial_state = self._entity.get_mental_state().get_current_state()
        self._entity.notify_of( Event() )
        post_notify_state = self._entity.get_mental_state().get_current_state()

        self.assertEqual(
            initial_state,
            post_notify_state,
            "Entity notify function prematurely updates the instance entity."
        )

        events = self._entity.update( EntityTests.TIME_DELTA )
        post_update_state = self._entity.get_mental_state().get_current_state()

        self.assertNotEqual(
            initial_state,
            post_update_state,
            "Entity notify function doesn't propogate mental state changes on update."
        )

        soln_events = SimpleTestState.ARRIVAL_DELTA.get_events() + \
            SimpleTestState.DEPARTURE_DELTA.get_events() + \
            SimpleTestState.STEP_DELTA.get_events()

        self.assertEqual(
            events,
            soln_events,
            "Updates with events return improper event listings."
        )

        soln_physstate = PhysicalState()
        soln_physstate.add_delta( SimpleTestEntity.INITIAL_PHYSICAL )
        soln_physstate.add_delta( EntityTests.ENTITY_DELTA )
        soln_physstate.add_delta( SimpleTestState.DEPARTURE_DELTA.get_entity_delta() )
        soln_physstate.add_delta( SimpleTestState.ARRIVAL_DELTA.get_entity_delta() )
        soln_physstate.add_delta( SimpleTestState.STEP_DELTA.get_entity_delta() )
        soln_physstate.update( EntityTests.TIME_DELTA )

        self.assertEqual(
            self._entity.get_physical_state(),
            soln_physstate,
            "Updates with events improperly update the entity's physical state."
        )


    def test_status( self ):
        soln_status = EntityTests.ENTITY_NAME + " " + \
            SimpleTestEntity.MACHINE_STATES[0].get_name() + " " + \
            str( 0.0 )

        self.assertEqual(
            self._entity.get_status(),
            soln_status,
            "Status function returns an improperly formatted string."
        )

