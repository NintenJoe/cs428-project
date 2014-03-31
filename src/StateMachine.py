##  @file StateMachine.py
#   @author Joseph Ciurej
#   @date Spring 2014
#
#   Source File for the "StateMachine" Type
#
#   @TODO
#   High Priority:
#   - Add functionality to this type to support reading in information from
#     graph data specification files.
#       > Details for graph data specification files are contained within the
#         NetworkX graph framework.
#   Low Priority:
#   - Make the state machine independent of the state list and transition
#     list passed in on initialization by making deep copies.
#   - Add error handling in the constructor to ensure that the initial state
#     machine information is correct.
#   - Determine whether to use the in-house graph implementation or the
#     'networkx' implementation.
#       > Implementation used is fairly arbitrary since it's completely masked
#         by the interface of the type.

import networkx as NX
from State import *
from Transition import *
from Event import *
from SimulationDelta import *

##  An implementation of the finite state machine pattern, which is used to 
#   facilitate state representation and transition specification for game
#   world objects.  A state machine resembles a graph in which nodes are
#   object states and edges are directed and activated by events occuring
#   within the game world.
class StateMachine():
    ### Constructors ###

    ##  Constructs a state machine containing the states in the given state
    #   listing, connected via the given transitions, and with the given start
    #   state.
    #
    #   @param state_list A listing of the "State" objects that will make up
    #    the vertices in the state machine instance.
    #   @param transition_list A listing of the "Transition" objects that will
    #    make up the directed edges in the state machine instance.
    #   @param start_id The name identifier of the starting state for the
    #    state machine instance (defaults to the first item in the state list).
    def __init__( self, state_list, transition_list, start_id=None ):
        self._machine = NX.DiGraph()
        self._curr_state_id = start_id if start_id else state_list[0].get_name()

        [ self._add_state( state ) for state in state_list ]
        [ self._add_transition( transition ) for transition in transition_list ]

        assert self._is_machine_valid(), "Instantiation of an invalid FSM!"

    ### Methods ###

    ##  Simulates a step of the state machine given the time delta between
    #   steps, returning a "SimulationDelta" object describing the changes.
    #
    #   @param time_delta The amount of elapsed time in between machine steps.
    #   @return A "SimulationDelta" instance that describes step changes.
    def simulate_step( self, time_delta ):
        step_delta = SimulationDelta()

        step_delta += self.get_current_state().simulate_step( time_delta )
        while self.get_current_state().has_timed_out():
            step_delta += self.simulate_transition( Event(EventType.TIMEOUT) )
            step_delta += self.get_current_state().simulate_step( time_delta )

        return step_delta

    ##  Simulates a transition in the state machine on the given event,
    #   returning a "SimulationDelta" object describing all the changes incited.
    #
    #   @param event The event on which the transition will be simulated.
    #   @return A "SimulationDelta" instance that describes all transition changes.
    def simulate_transition( self, event ):
        for transition in self._get_outgoing_transitions( self._curr_state_id ):
            if transition.invoked_by( event ):
                src_state = self._get_state( transition.get_source() )
                dst_state = self._get_state( transition.get_destination() )

                self._curr_state_id = dst_state.get_name()
                return src_state.simulate_departure() + dst_state.simulate_arrival()

        return SimulationDelta()
    ##  @return The string identifier for the current state of the instance
    #    state machine.
    def get_current_state( self ):
        return self._get_state( self._curr_state_id )

    ##  @return A list containing all the "State" objects contained in the 
    #    instance state machine.
    def get_states( self ):
        node_list = self._machine.nodes( data=True )
        return [ nd[ "obj" ] for ( node_id, nd ) in node_list ]

    ##  @return A list containing all the "Transition" objects contained in the 
    #    instance state machine.
    def get_transitions( self ):
        edge_list = self._machine.edges( data=True )
        return [ ed[ "obj" ] for ( src_id, dst_id, ed ) in edge_list ]

    ### Helper Methods ###

    ##  Adds the given state to the graph structure underlying the state machine.
    #
    #   @param state A "State" object that will be added to the underlying graph.
    def _add_state( self, state ):
        self._machine.add_node( state.get_name(), obj=state )

    ##  Adds the given transition to the graph structure underlying the state
    #   machine.
    #
    #   @param transition A "Transition" object that will be added to the
    #    underlying graph.
    def _add_transition( self, transition ):
        self._machine.add_edge( transition.get_source(), transition.get_destination(),
            obj=transition )

    ##  Given the string identifier for a state, this function returns the "State"
    #   object associated with that identifier.
    #
    #   @param state_id The string identifier of the state to be retrieved.
    #   @return The "State" object associated with the given identifier (or "None"
    #    if no such "State" exists in the machine).
    def _get_state( self, state_id ):
        return self._machine.node[ state_id ][ "obj" ] \
            if self._has_state( state_id ) else None

    ##  Given the string identifier for a state, this function returns the
    #   "Transition" objects originating from that state as a list.
    #
    #   @param state_id The string identifier of the state in question.
    #   @return A list containing all "Transition" objects originating from
    #    the "State" represented by the given identifier.
    def _get_outgoing_transitions( self, state_id ):
        outgoing_edges = self._machine.out_edges( state_id, data=True ) \
            if self._has_state( state_id ) else []

        return [ ed[ "obj" ] for ( src_id, dst_id, ed ) in outgoing_edges ]

    ##  Returns true if the "State" corresponding with the given identifier
    #   exists within the underlying graph structure and false otherwise.
    #
    #   @param state_id The string identifier to be checked.
    #   @return True if there's a "State" object corresponding to the given
    #    identifier and false otherwise.
    def _has_state( self, state_id ):
        return self._machine.has_node( state_id )

    ##  Determines whether or not the underlying machine for the state machine
    #   is valid or not, returning a Boolean based on this result.
    #
    #   @return True if the underlying machine is valid (i.e. valid states, 
    #    valid transitions, weakly connected) and false otherwise.
    def _is_machine_valid( self ):
        return True

