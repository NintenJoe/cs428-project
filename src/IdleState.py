##  @file IdleState.py
#   @author Joseph Ciurej
#   @date Spring 2014
#
#   Source File for the "IdleState" Type
#
#   @TODO
#   - Determine whether or not this class should be in the 'State' module or
#     not.

from State import *
from SimulationDelta import *

##  A type of state that represents a lack of movement or other ancillary state
#   changes.  Essentially, this is a state to represent object stillness.
class IdleState( State ):
    ### Constructors ###

    ##  Constructs an idle state instance with the given string identifier and a
    #   given time until a state "time out" occurs.
    #
    #   @param identifier A string identifier for that will represent the
    #    name of the instance state.
    #   @param timeout The amount of time until the instance state "times out."
    #    If no time is specified, there is no "time out" time for the state.
    def __init__( self, identifier, timeout=float("inf") ):
        super( IdleState, self ).__init__( "idle_" + identifier, timeout )

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
        return SimulationDelta()

    ##  Returns a zero "SimulationDelta" as no changes occur when departing from
    #   an idle state.
    #
    #   @override
    def _calc_departure_changes( self ):
        return SimulationDelta()

