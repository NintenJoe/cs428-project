##  @file StateMachine.py
#   @author Joseph Ciurej
#   @date Spring 2014
#
#   Source File for the "StateMachine" Type
#
#   @TODO
#   High Priority:
#   - Add more flexible machine creation through listings and dictionaries 
#     instead of explicit graphs.
#   - Allow for greater flexibility in specifying event transition qualifications.
#       > Should allow for finer granularity than simple event types (transition
#         based on event parameters as well, use regex).
#   Low Priority:
#   - Add functionality to this type to support reading in information from
#     graph data specification files.
#       > Details for graph data specification files are contained within the
#         NetworkX graph framework.
#   - Allow for greater flexibility in specifying state transition logic
#     (allow for special behavior based on transitions).
#       > This could probably be accomplished through intermediate states, which
#         may be more elegant overall.
#   - Add error handling in the constructor to ensure that the specified start
#     state is valid.

import networkx as NX
from Event import *

##  An implementation of the finite state machine pattern, which is used to 
#   facilitate state representation and transition specification for game
#   world objects.  A state machine resembles a graph in which nodes are
#   object states and edges are directed and activated by events occuring
#   within the game world.
class StateMachine():
    ### Constructors ###

    ##  Constructs a state machine with a state structure specified by the
    #   given state graph that starts in the given starting state.
    #
    #   @param state_graph A NetworkX directed graph in which nodes represent 
    #    machine states and an edge A -> B indicates that A transitions to B.
    #   @param start_state The identifier for the initial state for the instance
    #    state machine.
    def __init__( self, state_graph, start_state=state_graph.nodes()[0] ):
        self._machine = state_graph
        self._state = start_state

        self._idle_time = 0.0

    ### Methods ###

    ##  Automates a step of the state machine given the current time delta 
    #   between steps, returning a description of incurred state changes.
    #
    #   @param time_delta The amount of elapsed time in between machine steps.
    #   @return An user-dependent description of the state changes caused by
    #    automating a machine step.
    def automate_step( self, time_delta ):
        self._idle_time += time_delta

        return self._machine.node[ self._state ][ "step" ]( self._idle_time, time_delta )

    ##  Notifies the instance machine that the given event has ocurred, which
    #   will drive state changes within the machine based on the current state.
    #
    #   @param event The event related to the instance machine of which the
    #    machine will be notified.
    def notify_of( self, event ):
        outgoing_edges = self._machine.out_edges( self._state, data=True )

        # TODO: Update this transition to be dependent on more than event type.
        for ( src_state, dst_state, edge_data ) in outgoing_edges:
            if edge_data[ "event" ] == event.get_type():
                self._change_state( dst_state )

    ##  @returns The string identifier for the current state of the instance
    #   state machine.
    def get_current_state( self ):
        return self._state

    ### Helper Methods ###

    ##  Changes the current internal state to the given machine state, updating
    #   all internal parameters accordingly.
    #
    #   @param new_state The new state for the instance machine.
    def _change_state( self, new_state ):
        self._state = new_state
        self._idle_time = 0.0