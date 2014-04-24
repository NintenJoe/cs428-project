##  @file FollowState.py
#   @author Eric Christianson, Joseph Ciurej
#   @date Spring 2014
#
#   Source File for the "FollowState" Type
#
#   @TODO
#   - This class

from State import *
from PhysicalState import *
from SimulationDelta import *
from CompositeHitbox import *

##  A type of state that represents an object that is currently moving
#(or at least, attempting to move) in a given direction
class FollowState( State ):
    ### Constructors ###

    ##  Constructs a state instance with the given string identifier.
    #
    #   @param identifier A string identifier for that will represent the
    #    name of the instance state.
    #   @param (vx,vy) the x and y components of the velocity of movement
    def __init__( self, identifier, v, timeout=float("inf") ):
        super( FollowState, self ).__init__( "follow_" + identifier, timeout )
        self._v = v

    ### Methods ###

    # Note: There are no public functions for this type!  For public method
    # reference, see the 'State' type.

    ### Helper Methods ###

    ##  Calculates the change in x and y position by multiplying the
    #   x and y velocities by the time delta, and returns a representation
    #   of the change in coordinates
    #
    #   @override
    def _calc_step_changes( self, time_delta ):
        deltax = self._vx * time_delta;
        deltay = self._vy * time_delta;
        phys_delta = PhysicalState(CompositeHitbox(deltax, deltay), (0, 0), 0.0 )

        return SimulationDelta( phys_delta )

    ##  Returns an empty set of physical changes.
    #
    #   @override
    def _calc_arrival_changes( self, event ):
        return SimulationDelta(PhysicalState(CompositeHitbox(), (self._vx, self._vy), 0.0))

    ##  Returns an empty set of physical changes.
    #
    #   @override
    def _calc_departure_changes( self ):
        return SimulationDelta(PhysicalState(CompositeHitbox(), (-self._vx, -self._vy), 0.0))