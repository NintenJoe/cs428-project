##  @file PhysicalState.py
#   @author Joseph Ciurej
#   @date Spring 2014
#
#   Source File for the "PhysicalState" Type
#
#   @TODO
#   High Priority:
#   - Tuples are used for the velocity vector, which requires an uneccesary
#     duplicaton on updates.
#       > If the current method isn't fast enough, remove the tuple dependence
#         and replace it with a list or something similar.
#   - Note somewhere that physical deltas no longer support altering the
#     dimensions of the collision volume.
#       > This aspect was omitted from the current version because the
#         functionality wasn't previously used and implementing it with
#         `CompositeHitbox` instances is complex.
#   Low Priority:
#   - Rename the attributes associated with the `volume` to be more properly
#     associated with the `hitbox` metaphor.
#   - Refactor the constructor to more elegantly copy the contents of the given
#     `CompositeHitbox`.

import pygame as PG
from CompositeHitbox import *

##  A representation of the tangible state of an object within the game world.
#   This type describes all physical information associated with an object,
#   such as its current position, bounding volume, velocity, et cetera.
class PhysicalState( object ):
    ### Constructors ###

    ##  Initializes a physical state with the given collision volume, velocity,
    #   and mass values.
    #
    #   @param volume The collision volume for the state (as a `CompositeHitbox`).
    #   @param velocity The velocity for the state (as a 2-tuple).
    #   @param mass The floating-point value that will represent the state mass.
    def __init__( self, volume=CompositeHitbox(), velocity=(0, 0), mass=0.0 ):
        self._volume = CompositeHitbox(
            volume.get_position()[0],
            volume.get_position()[1],
            volume.get_relative_hitboxes()
        )
        self._velocity = velocity
        self._mass = mass

    ### Overloaded Operators ###

    ##  Returns true if all aspects of the physical state instances are
    #   equivalent (i.e. volume, velocity, mass).
    #
    #   @return True if the instance state is equivalent to the given state and
    #    false otherwise.
    def __eq__( self, other ):
        return self._mass == other._mass and \
            self._velocity == other._velocity and \
            self._volume == other._volume

    ### Methods ###

    ##  Adds the change in physical state represented by the given state object
    #   to the instance state.
    #
    #   @param state_delta The physical state representing the changes in state.
    def add_delta( self, state_delta ):
        self._volume.translate(
            state_delta._volume.get_position()[ 0 ],
            state_delta._volume.get_position()[ 1 ]
        )

        self._velocity = (
            self._velocity[ 0 ] + state_delta._velocity[ 0 ],
            self._velocity[ 1 ] + state_delta._velocity[ 1 ]
        )

        self._mass += state_delta._mass

    ##  Updates the physical state based on the given time delta.
    #
    #   @param time_delta The amount of time between updates to the physical state.
    def update( self, time_delta ):
        position_delta = map( lambda v_i: time_delta * v_i, self._velocity )

        self._volume.translate( position_delta[0], position_delta[1] )

    ##  @return The collision volume associated with the instance state (of type
    #    "HashableRect").
    def get_volume( self ):
        return self._volume

    ##  @return The velocity vector associated with the instance state (of type
    #    integer two-tuple).
    def get_velocity( self ):
        return self._velocity

    ##  @return The mass value associated with the instance state (of type float).
    def get_mass( self ):
        return self._mass

