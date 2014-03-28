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
#   - Add functionality to read in state machine information from files.
#       > Does networkx allow for this behavior?
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

from Event import *
from PhysicalState import *

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
    def __init__( self, state_graph, start_state=None ):
        self._machine = state_graph
        self._state = start_state if start_state != None else state_graph.first_added

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

        return self._state.simulate_step(time_delta)

    ##  Notifies the instance machine that the given event has ocurred, which
    #   will drive state changes within the machine based on the current state.
    #
    #   @param event The event related to the instance machine of which the
    #    machine will be notified.
    def notify_of( self, event ):
        new_state = self._machine.transition(self._state, event)
        if new_state != self._state:
            change = self._state.simulate_departure()
            change.add_delta(new_state.simulate_arrival())
            self._change_state( new_state )
            return change
        return PhysicalState()

    ##  @return The string identifier for the current state of the instance
    #   state machine.
    def get_current_state( self ):
        return self._state

    ##  @return The amount of time that the instance machine has been idle on its
    #   current state.
    def get_idle_time( self ):
        return self._idle_time

    ### Helper Methods ###

    ##  Changes the current internal state to the given machine state, updating
    #   all internal parameters accordingly.
    #
    #   @param new_state The new state for the instance machine.
    def _change_state( self, new_state ):
        self._state = new_state
        self._idle_time = 0.0
