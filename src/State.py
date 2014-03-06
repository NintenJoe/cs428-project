##  @file State.py
#   @author Joseph Ciurej
#   @date Spring 2014
#
#   Source File for the "State" Type
#
#   @TODO
#   - Determine if this is more appropriate for this module file or if it 
#     should be contained within the "StateMachine" module instead.
#   - Determine how the inheritance hierarchy for the "State" type
#     should affect module containment.
#       > If "State" subclasses are to be contained in the same module
#         as "State," should there be a dedicated module?
#   - Try to integrate the total time within the state into the state itself
#     to make some of the methods more elegant.
#   - Add support to allow simulating a step to return an event in addition to
#     returning the physical state.

from abc import ABCMeta, abstractmethod
# from PhysicalState import *

##  The representation of a single node within a state machine.  Each state
#   represents a distinct set of update behaviors, which encode how an object
#   "in" the state should change over time.
class State():
    ### Constructors ###

    ##  Constructs a state instance with the given string identifier.
    #
    #   @param identifier A string identifier for that will represent the
    #    name of the instance state.
    def __init__( self, identifier ):
        self._name = identifier
        self._active_time = 0.0

    ### Methods ###

    ##  Simulates a time step (of the given length) within the instance state,
    #   returning the aggregate change in physical state resulting from this step.
    #
    #   @param time_delta The length of the time step to be simulated by the state.
    #   @return A physical state object that represents the state delta caused
    #    by simulating the instance state behavior for the given period of time.
    def simulate_step( self, time_delta ):
        self._active_time += time_delta

        return self._calculate_step_changes( time_delta )

    ##  Simulates an arrival at the instance state, returning the physical state
    #   changes that accompany such a change.
    #
    #   @return A physical state object that represents the state delta caused
    #    by arriving at the instance state.
    def simulate_arrival( self ):
        self._active_time = 0.0

        return self._calc_arrivial_changes()

    ##  Simulates a departure from the instance state, returning the physical state
    #   changes that accompany such a change.
    #
    #   @return A physical state object that represents the state delta caused
    #    by departing from the instance state.
    def simulate_departure( self ):
        self._active_time = 0.0

        return self._calc_departure_changes()

    ##  @return The identifying name for the state object instance.
    def get_name( self ):
        return self._name

    ##  @return The total amount of time that the instance state has been active.
    def get_active_time( self ):
        return self._active_time

    ### Helper Methods ###

    ##  Calculates the changes for being in the instance state for the given
    #   period of time.
    #
    #   @param time_delta The length of the time step to be simulated by the state.
    #   @return A physical state object that represents the state delta caused
    #    by simulating the instance 
    @abstractmethod
    def _calc_step_changes( self, time_delta ):
        return PhysicalState()

    ##  Simulates an arrival at the instance state, returning the physical state
    #   changes that accompany such a change.
    #
    #   @return A physical state object that represents the state delta caused
    #    by arriving at the instance state.
    @abstractmethod
    def _calc_arrival_changes( self ):
        return PhysicalState()

    ##  Simulates an departure at the instance state, returning the physical state
    #   changes that accompany such a change.
    #
    #   @return A physical state object that represents the state delta caused
    #    by departure at the instance state.
    @abstractmethod
    def _calc_departure_changes( self ):
        return PhysicalState()

    ### Class Setup ###

    ##  Identifies the class as an abstract base class.
    __metaclass__ = ABCMeta

