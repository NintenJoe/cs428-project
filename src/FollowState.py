##  @file FollowState.py
#   @author Nick Jeffrey
#   @date Spring 2014
#
#   Source File for the "FollowState" Type
#

from State import *
from PhysicalState import *
from SimulationDelta import *
from CompositeHitbox import *
import math

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
        self._follow = None
        self._pos = None

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
        if self._follow != None and self._pos != None:
            pos = self._pos.get_chitbox().get_position()
            follow = self._follow.get_chitbox().get_position()
            if pos[0] == follow[0] and pos[1] == follow[1]:
                return SimulationDelta()
            dist = self._v * time_delta
            xdif = 0
            if pos[0] >= follow[0]:
                xdif = pos[0] - follow[0]
            else:
                xdif = follow[0] - pos[0]
            ydif = 0
            if pos[1] >= follow[1]:
                ydif = pos[1] - follow[1]
            else:
                ydif = follow[1] - pos[1]
            xperc = xdif / (xdif + ydif)
            deltax = math.sqrt(dist**2 - (1+xperc)**2)
            deltay = math.sqrt(dist**2 - (2-xperc)**2)
            if pos[0] > follow[0]:
                deltax = -1 * deltax
            if pos[1] > follow[1]:
                deltay = -1 * deltay
            phys_delta = PhysicalState(CompositeHitbox(deltax, deltay), (0, 0), 0.0 )
            return SimulationDelta( phys_delta )
        return SimulationDelta()

    ##  Player should be one of the collissions,
    #   finds player and sets them to be followed
    #   Returns an empty set of physical changes.
    #
    #   @override
    def _calc_arrival_changes( self, event ):
        return SimulationDelta(PhysicalState(CompositeHitbox(), (0, 0), 0.0))

    ##  Returns an empty set of physical changes.
    #
    #   @override
    def _calc_departure_changes( self ):
        return SimulationDelta(PhysicalState(CompositeHitbox(), (0, 0), 0.0))