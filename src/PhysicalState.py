##  @file PhysicalState.py
#   @author Joseph Ciurej
#   @date Spring 2014
#
#   Source File for the "PhysicalState" Type
#
#   @TODO
#   - Write the implementation in this file!

import pygame as PG

##  A representation of the tangible state of an object within the game world.
#   This type describes all physical information associated with an object,
#   such as its current position, bounding volume, velocity, et cetera.
class PhysicalState():
    ### Constructors ###

    ##  Initializes a physical state with the given collision volume, velocity,
    #   and mass values.
    #
    #   @param volume The collision volume that will be instantiated to the state
    #    (given as a Pygame Rect).
    #   @param velocity The velocity that will be initialized to the state (as a
    #    2-tuple).
    #   @param mass The floating-point value that will represent the state mass.
    def __init__( self, volume=PG.Rect(0, 0, 0, 0), velocity=(0, 0), mass=0.0 ):
        self._volume = volume
        self._velocity = velocity
        self._mass = mass

    ### Methods ###

    ##  Adds the change in physical state represented by the given state object
    #   to the instance state.
    #
    #   @param state_delta The physical state representing the changes in state.
    def add_delta( self, state_delta ):
        self._volume.x += state_delta._volume.x
        self._volume.y += state_delta._volume.y
        self._volume.w += state_delta._volume.w
        self._volume.h += state_delta._volume.h

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

        self._volume.centerx += position_delta[ 0 ]
        self._volume.centery += position_delta[ 1 ]

    ##  @return The collision volume associated with the instance state.
    def get_volume( self ):
        return self._volume

    ##  @return The velocity vector associated with the instance state.
    def get_velocity( self ):
        return self._velocity

    ##  @return The mass value associated with the instance state.
    def get_mass( self ):
        return self._mass
