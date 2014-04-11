##  @file ShiftState.py
#   @author Nick Jeffrey
#   @date Spring 2014
#
#   Source File for the "ShiftState" Type
#

from State import *
from SimulationDelta import *
from CompositeHitbox import *

##  A type of state that represents a change in position at enter and exit of the state, but no other movement.
class ShiftState( State ):
    ### Constructors ###

    ##  Constructs an shift state instance with the given string identifier and a
    #   given time until a state "time out" occurs.
    #
    #   @param identifier A string identifier for that will represent the
    #    name of the instance state.
    #   @param xchange The amount of change in the x coordinate
    #   @param ychange The amount of change in the y coordinate
    #   @param timeout The amount of time until the instance state "times out."
    #    If no time is specified, there is no "time out" time for the state.
    def __init__( self, identifier, xchange, ychange, timeout=float("inf") ):
        super( ShiftState, self ).__init__( "idle_" + identifier, timeout )
        self._xchange = xchange
        self._ychange = ychange

    ### Methods ###

    # Note: There are no public functions for this type!  For public method
    # reference, see the 'State' type.

    ### Helper Methods ###

    ##  Returns a zero "SimulationDelta" as no changes occur while stepping in 
    #   an idle state.
    #
    #   @override
    def _calc_step_changes( self, time_delta ):
        return SimulationDelta()

    ##  Returns a zero "SimulationDelta" as no changes occur when arriving at
    #   an idle state.
    #
    #   @override
    def _calc_arrival_changes( self ):
        return SimulationDelta(PhysicalState(CompositeHitbox(self._xchange, self._ychange), (0, 0), 0.0))

    ##  Returns a zero "SimulationDelta" as no changes occur when departing from
    #   an idle state.
    #
    #   @override
    def _calc_departure_changes( self ):
        return SimulationDelta(PhysicalState(CompositeHitbox(-1 * self._xchange, -1 * self._ychange), (0, 0), 0.0))

