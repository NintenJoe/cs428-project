##  @file State.py
#   @author Joseph Ciurej
#   @date Spring 2014
#
#   Source File for the "State" Type
#
#   @TODO
#   High Priority:
#   - Finalize the step simulation logic when time outs occur.
#       > Choice 1 (current): Quantize time on a per-frame basis.  This option entails
#         that if a state times out, then it will return an empty delta and
#         all time delta will be delegated to the next state.
#       > Choice 2: Delegate time based on the amount of time given to each
#         state.  This option entails that intermediate timeouts may be invisible,
#         but that they will always occur and eat up time proportional to their
#         timeout time.
#   Low Priority:
#   - Determine if this is more appropriate for this module file or if it 
#     should be contained within the "StateMachine" module instead.
#   - Determine how the inheritance hierarchy for the "State" type
#     should affect module containment.
#       > If "State" subclasses are to be contained in the same module
#         as "State," should there be a dedicated module?

from abc import ABCMeta, abstractmethod
from SimulationDelta import *
from Event import *

##  The representation of a single node within a state machine.  Each state
#   represents a distinct set of update behaviors, which encode how an object
#   "in" the state should change over time.
class State( object ):
    ### Class Setup ###

    ##  Identifies the class as an abstract base class.
    __metaclass__ = ABCMeta

    ### Constructors ###

    ##  Constructs a state instance with the given string identifier and a
    #   given time until a state "time out" occurs.
    #
    #   @param identifier A string identifier for that will represent the
    #    name of the instance state.
    #   @param timeout The amount of time until the instance state "times out."
    #    If no time is specified, there is no "time out" time for the state.
    def __init__( self, identifier, timeout=float("inf") ):
        self._name = identifier

        self._active_time = 0.0
        self._timeout_time = timeout

    ### Methods ###

    ##  Simulates a time step (of the given length) within the instance state,
    #   returning the resultant changes as a "SimulationDelta" instance.
    #
    #   @param time_delta The length of the time step to be simulated by the state.
    #   @return A "SimulationDelta" containing all the changes incurred by the step.
    def simulate_step( self, time_delta ):
        self._active_time += time_delta

        return self._calc_step_changes( time_delta ) if not self.has_timed_out() \
            else SimulationDelta()

    ##  Simulates an arrival at the instance state, returning the resultant
    #   changes as a "SimulationDelta" instance.
    #
    #   @param event The event that triggered the arrival
    #
    #   @return A "SimulationDelta" containing all the changes incurred by the
    #    arrival.
    def simulate_arrival( self, event=Event() ):
        self._active_time = 0.0

        return self._calc_arrival_changes(event)

    ##  Simulates a departure from the instance state, returning the resultant
    #   changes as a "SimulationDelta" instance.
    #
    #   @return A "SimulationDelta" containing all the changes incurred by the
    #    departure.
    def simulate_departure( self ):
        self._active_time = 0.0

        return self._calc_departure_changes()

    ##  @return True if the state has exceeded its maximum "time out" time and
    #    false otherwise.
    def has_timed_out( self ):
        return self.get_excess_time() > 0.0

    ##  @return The identifying name for the state object instance.
    def get_name( self ):
        return self._name

    ##  @return The total amount of time that the instance state has been active.
    def get_active_time( self ):
        return self._active_time

    ##  @return The maximum amount of time for which the state can be active
    #    (which will be infinite if the state has no time out time).
    def get_timeout_time( self ):
        return self._timeout_time

    ##  @return The amount of excess time that the instance state has been
    #    active (which will be 0 if no such excess time exists).
    def get_excess_time( self ):
        return max( self.get_active_time() - self.get_timeout_time(), 0.0 )

    ### Helper Methods ###

    ##  Calculates the changes for being in the instance state for the given
    #   period of time.
    #
    #   @param time_delta The length of the time step to be simulated by the state.
    #   @return The changes associated with the step as a "SimulationDelta".
    @abstractmethod
    def _calc_step_changes( self, time_delta ):
        pass

    ##  Simulates an arrival at the instance state, returning the changes
    #   associated with this arrival.
    #
    #   @param event The event that triggered the arrival
    #
    #   @return The changes associated with the arrival as a "SimulationDelta".
    @abstractmethod
    def _calc_arrival_changes( self, event ):
        pass

    ##  Simulates an arrival at the instance state, returning the changes
    #   associated with this departure.
    #
    #   @return The changes associated with the departure as a "SimulationDelta".
    @abstractmethod
    def _calc_departure_changes( self ):
        pass

