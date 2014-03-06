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

    ### Methods ###

    ##  Simulates a time step (of the given length) within the instance state,
    #   returning the aggregate change in physical state resulting from this step.
    #
    #   @param total_time The total amount of time that the state has been active.
    #   @param time_delta The length of the time step to be simulated by the state.
    #   @return A physical state object that represents the state delta caused
    #    by simulating the instance state behavior for the given period of time.
    @abstractmethod
    def simulate_step( self, total_time, time_delta ):
        return PhysicalState( )

    ##  Simulates an arrival at the instance state, returning the physical state
    #   changes that accompany such a change.
    #
    #   @return A physical state object that represents the state delta caused
    #    by arriving at the instance state.
    @abstractmethod
    def simulate_arrival( self ):
        return PhysicalState( )

    ##  Simulates a departure from the instance state, returning the physical state
    #   changes that accompany such a change.
    #
    #   @return A physical state object that represents the state delta caused
    #    by departing from the instance state.
    @abstractmethod
    def simulate_departure( self ):
        return PhysicalState( )

    ##  @return The identifying name for the state object instance.
    def get_name( self ):
        return self._name

    ### Class Setup ###

    ##  Identifies the class as an abstract base class.
    __metaclass__ = ABCMeta

