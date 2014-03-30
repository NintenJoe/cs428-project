##  @file StateMachineTests.py
#   @author Joseph Ciurej
#   @date Spring 2014
#
#   Test File for the "StateMachine" Type
#
#   @TODO
#   High Priority:
#   - Update the 'TestStates' reference in this testing file once the location
#     of this file changes.
#   Low Priority:
#   - Refactor the set-up procedure to allow for conditional construction
#     of graphs based on the testing function.
#   - Update the tests further to test for even more complex behavior in the
#     state machine transition/update functions (i.e. different states with

import unittest
import src
from TestStates import *
from src.StateMachine import *
from src.Transition import *
from src.Event import *
from src.SimulationDelta import *

##  Container class for the test suite that tests the functionality of the
#   "StateMachine" type.
class StateMachineTests( unittest.TestCase ):
    ### Testing Constants ###

    ##  The step that will be used as the time delta when simulating steps on
    #   the test state machines.
    TIME_DELTA = 1.0

    ##  The state information that will be used in the simple test state machine.
    SIMPLE_STATES = [ SimpleTestState("0") ]
    ##  The transition information that will be used in the simple test state machine.
    SIMPLE_TRANS = []

    ##  The state information that will be used in the complex test state machine.
    COMPLEX_STATES = [
        SimpleTestState( "0", 2.0 * TIME_DELTA ),
        SimpleTestState( "1", 2.0 * TIME_DELTA ),
        SimpleTestState( "2", 0.0 * TIME_DELTA )
    ]
    ##  The transition information that will be used in the complex test state machine.
    COMPLEX_TRANS = [
        Transition( COMPLEX_STATES[0].get_name(), COMPLEX_STATES[1].get_name(),
            "^" + repr( Event(EventType.NOTIFY) ) + "$" ),
        Transition( COMPLEX_STATES[0].get_name(), COMPLEX_STATES[2].get_name(),
            "^" + repr( Event(EventType.TIMEOUT) ) + "$" ),
        Transition( COMPLEX_STATES[2].get_name(), COMPLEX_STATES[1].get_name() ),
        Transition( COMPLEX_STATES[1].get_name(), COMPLEX_STATES[0].get_name() )
    ]

    ### Test Set Up/Tear Down ###

    def setUp( self ):
        # Simple Machine: Single Node Graph
        #
        #               ----------
        #               |    0   |
        #               ----------
        #
        self._simple_machine = StateMachine(
            StateMachineTests.SIMPLE_STATES,
            StateMachineTests.SIMPLE_TRANS
        )

        # Complex Machine: Cyclic Graph w/ Three Nodes
        #
        #               ----------*
        #       +-------|    1   |<-----+
        #       V *     ----------      |
        #  ----------       ^ N     ----------
        #  |    0   |-------+------>|    2   |
        #  ----------              T----------
        #
        self._complex_machine = StateMachine(
            StateMachineTests.COMPLEX_STATES,
            StateMachineTests.COMPLEX_TRANS,
            StateMachineTests.COMPLEX_STATES[0].get_name()
        )

    def tearDown( self ):
        self._simple_machine = None
        self._complex_machine = None

        # TODO: This is a bit of a hack to reset all the state timers.  While
        # not a terrible solution, this could certainly be improved.
        states = StateMachineTests.SIMPLE_STATES + StateMachineTests.COMPLEX_STATES
        [ state.simulate_arrival() for state in states ]

    ### Testing Functions ###

    def test_default_constructor( self ):
        self.assertEqual(
            self._simple_machine.get_current_state(),
            StateMachineTests.SIMPLE_STATES[ 0 ],
            "Default FSM constructor improperly sets initial state."
        )

        simple_states = self._simple_machine.get_states()
        self.assertEqual(
            set( simple_states ),
            set( StateMachineTests.SIMPLE_STATES ),
            "Default FSM constructor contains incorrect states."
        )

        simple_transitions = self._simple_machine.get_transitions()
        self.assertEqual(
            set( simple_transitions ),
            set( StateMachineTests.SIMPLE_TRANS ),
            "Default FSM constructor contains incorrect transitions."
        )


    def test_value_constructor( self ):
        self.assertEqual(
            self._complex_machine.get_current_state(),
            StateMachineTests.COMPLEX_STATES[ 0 ],
            "Value FSM constructor improperly sets initial state."
        )

        complex_states = self._complex_machine.get_states()
        self.assertEqual(
            set( complex_states ),
            set( StateMachineTests.COMPLEX_STATES ),
            "Value FSM constructor contains incorrect states."
        )

        complex_transitions = self._complex_machine.get_transitions()
        self.assertEqual(
            set( complex_transitions ),
            set( StateMachineTests.COMPLEX_TRANS ),
            "Value FSM constructor contains incorrect transitions."
        )


    def test_singular_step( self ):
        sd = self._complex_machine.simulate_step( StateMachineTests.TIME_DELTA )

        self.assertEqual(
            self._complex_machine.get_current_state(),
            StateMachineTests.COMPLEX_STATES[ 0 ],
            "Singular step improperly causes a state transition in a FSM."
        )
        self.assertEqual(
            sd,
            SimpleTestState.STEP_DELTA,
            "Singular step in a FSM returns an inaccurate simulation delta."
        )


    def test_invalid_transition( self ):
        td1 = self._complex_machine.simulate_transition( Event(EventType.COLLISION) )
        self.assertEqual(
            self._complex_machine.get_current_state(),
            StateMachineTests.COMPLEX_STATES[ 0 ],
            "Invalid event improperly causes a transition in a FSM."
        )
        self.assertEqual(
            td1,
            SimulationDelta(),
            "Invalid event transitions improperly return a non-zero sim delta."
        )

        td2 = self._complex_machine.simulate_transition( Event(EventType.COLLISION) )
        self.assertEqual(
            self._complex_machine.get_current_state(),
            StateMachineTests.COMPLEX_STATES[ 0 ],
            "Subsequent invalid events improperly cause a transition in a FSM."
        )
        self.assertEqual(
            td2,
            SimulationDelta(),
            "Subsequent innvalid event transitions return a non-zero sim delta."
        )


    def test_valid_transition( self ):
        td1 = self._complex_machine.simulate_transition( Event(EventType.NOTIFY) )
        self.assertEqual(
            self._complex_machine.get_current_state(),
            StateMachineTests.COMPLEX_STATES[ 1 ],
            "Valid event improperly doesn't cause a transition in a FSM."
        )
        self.assertEqual(
            td1,
            SimpleTestState.ARRIVAL_DELTA + SimpleTestState.DEPARTURE_DELTA,
            "Valid event transitions return an incorrect sim delta."
        )

        td2 = self._complex_machine.simulate_transition( Event(EventType.COLLISION) )
        self.assertEqual(
            self._complex_machine.get_current_state(),
            StateMachineTests.COMPLEX_STATES[ 0 ],
            "Subsequent valid events improperly don't cause a transition in a FSM."
        )
        self.assertEqual(
            td2,
            SimpleTestState.ARRIVAL_DELTA + SimpleTestState.DEPARTURE_DELTA,
            "Subsequent valid event transitions return an incorrect sim delta."
        )


    def test_timeout_transition( self ):
        self._complex_machine.simulate_transition( Event(EventType.TIMEOUT) )
        self.assertEqual(
            self._complex_machine.get_current_state(),
            StateMachineTests.COMPLEX_STATES[ 2 ],
            "Manual timeout event submission doesn't properly cause FSM transitions."
        )

        self._complex_machine.simulate_transition( Event(EventType.NOTIFY) )
        self.assertEqual(
            self._complex_machine.get_current_state(),
            StateMachineTests.COMPLEX_STATES[ 1 ],
            "Manual timeout event submission causes subsequent transitions to fail."
        )

        self._complex_machine.simulate_step( StateMachineTests.TIME_DELTA )
        self._complex_machine.simulate_step( StateMachineTests.TIME_DELTA )
        self.assertEqual(
            self._complex_machine.get_current_state(),
            StateMachineTests.COMPLEX_STATES[ 1 ],
            "Automatic step timeout causes FSM transitions too early."
        )

        self._complex_machine.simulate_step( StateMachineTests.TIME_DELTA )
        self.assertEqual(
            self._complex_machine.get_current_state(),
            StateMachineTests.COMPLEX_STATES[ 0 ],
            "Automatic step timeout doesn't properly cause FSM transitions."
        )


    def test_multipart_step( self ):
        self._complex_machine.simulate_step( StateMachineTests.TIME_DELTA )
        self._complex_machine.simulate_step( StateMachineTests.TIME_DELTA )

        sd = self._complex_machine.simulate_step( StateMachineTests.TIME_DELTA )
        self.assertEqual(
            self._complex_machine.get_current_state(),
            StateMachineTests.COMPLEX_STATES[ 1 ],
            "Multipart transitions aren't properly caused by step simulation."
        )

        # Step consists of two arrival/departure combinations and a single step
        # delta at the final state.
        soln_delta = SimpleTestState.DEPARTURE_DELTA + \
            SimpleTestState.ARRIVAL_DELTA + \
            SimpleTestState.DEPARTURE_DELTA + \
            SimpleTestState.ARRIVAL_DELTA + \
            SimpleTestState.STEP_DELTA
        self.assertEqual(
            sd,
            soln_delta,
            "Multipart transitions through steps return an incorrect sim delta."
        )

