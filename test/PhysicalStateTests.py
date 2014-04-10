##  @file PhysicalStateTests.py
#   @author Joseph Ciurej
#   @date Spring 2014
#
#   Test File for the "PhysicalState" Type
#
#   @TODO
#   - Since the 'PhysicalState' is a fairly volatile module, this testing file
#     may need to be changed fairly often.

import unittest
import src
import pygame as PG

from src.PhysicalState import *

##  Container class for the test suite that tests the functionality of the
#   "PhysicalState" type.
class PhysicalStateTests( unittest.TestCase ):
    ### Testing Constants ###

    ##  The volume that will be initialized to the test physical state.
    VOLUME = PG.Rect(10, 20, 30, 40)

    ##  The velocity vector that will be initialized to the test physical state.
    VELOCITY = (-5, 2)

    ##  The maass value that will be initialized to the test physical state.
    MASS = 0.4

    ##  The time delta that will be used to test physical state updating.
    TIME_DELTA = 1.0

    ### Test Set Up/Tear Down ###

    def setUp( self ):
        self._physstate = PhysicalState( PhysicalStateTests.VOLUME,
            PhysicalStateTests.VELOCITY, PhysicalStateTests.MASS )

    def tearDown( self ):
        self._physstate = None

    ### Testing Functions ###

    def test_default_constructor( self ):
        default_physstate = PhysicalState()

        self.assertEqual( default_physstate.get_volume(), PG.Rect(0, 0, 0, 0),
            "Default physical state contructor doesn't initialize identity volume." )
        self.assertEqual( default_physstate.get_velocity(), (0, 0),
            "Default physical state contructor doesn't initialize identity velocity." )
        self.assertEqual( default_physstate.get_mass(), 0.0,
            "Default physical state contructor doesn't initialize identity mass." )


    def test_value_constructor( self ):
        self.assertEqual( self._physstate.get_volume(), PhysicalStateTests.VOLUME,
            "Value physical state contructor doesn't initialize with given volume." )
        self.assertEqual( self._physstate.get_velocity(), PhysicalStateTests.VELOCITY,
            "Value physical state contructor doesn't initialize with given velocity." )
        self.assertEqual( self._physstate.get_mass(), PhysicalStateTests.MASS,
            "Value physical state contructor doesn't initialize with given mass." )


    def test_constructor_independence( self ):
        self._physstate._volume.x += 1
        self.assertNotEqual( self._physstate.get_volume(), PhysicalStateTests.VOLUME,
            "Value constructor for physical state doesn't deep copy parameter objects." )


    def test_constructor_independence2( self ):
        state1 = PhysicalState()
        state1.add_delta(PhysicalState(PG.Rect(2,3,-1,5), (1,0), 1))
        state2 = PhysicalState()
        self.assertNotEqual(state1.get_volume(), state2.get_volume())
        self.assertNotEqual(state1.get_velocity(), state2.get_velocity())
        self.assertNotEqual(state1.get_mass(), state2.get_mass())


    def test_equality_operator( self ):
        physstate1 = PhysicalState()
        physstate2 = PhysicalState()

        self.assertTrue( physstate1 == physstate1,
            "Equality operator doesn't return true for self equality in simple case." )
        self.assertTrue( self._physstate == self._physstate,
            "Equality operator doesn't return true for self equality in complex case." )
        self.assertTrue( physstate1 == physstate2,
            "Equality operator doesn't return true for two equivalent objects." )
        self.assertTrue( physstate1 != self._physstate,
            "Equality operator improperly returns true for two unequivalent objects." )


    def test_add_simple_delta( self ):
        simple_delta = PhysicalState()
        self._physstate.add_delta( simple_delta )

        self.assertEqual( self._physstate.get_volume(), PhysicalStateTests.VOLUME,
            "Adding a zero delta to a state changes its volume value." )
        self.assertEqual( self._physstate.get_velocity(), PhysicalStateTests.VELOCITY,
            "Adding a zero delta to a state changes its velocity value." )
        self.assertEqual( self._physstate.get_mass(), PhysicalStateTests.MASS,
            "Adding a zero delta to a state changes its mass value." )


    def test_add_complex_delta( self ):
        simple_delta = PhysicalState( PG.Rect(1, 2, 3, 4), (-5.0, -3.0), 18.0 )
        self._physstate.add_delta( simple_delta )

        self.assertEqual( self._physstate.get_volume().x, PhysicalStateTests.VOLUME.x + 1,
            "Adding a non-zero delta to a state doesn't properly alter volume X." )
        self.assertEqual( self._physstate.get_volume().y, PhysicalStateTests.VOLUME.y + 2,
            "Adding a non-zero delta to a state doesn't properly alter volume Y." )
        self.assertEqual( self._physstate.get_volume().w, PhysicalStateTests.VOLUME.w + 3,
            "Adding a non-zero delta to a state doesn't properly alter volume W." )
        self.assertEqual( self._physstate.get_volume().h, PhysicalStateTests.VOLUME.h + 4,
            "Adding a non-zero delta to a state doesn't properly alter volume H." )

        self.assertEqual( self._physstate.get_velocity()[0], PhysicalStateTests.VELOCITY[0] - 5.0,
            "Adding a non-zero delta to a state doesn't properly alter velocity X." )
        self.assertEqual( self._physstate.get_velocity()[1], PhysicalStateTests.VELOCITY[1] - 3.0,
            "Adding a non-zero delta to a state doesn't properly alter velocity Y." )

        self.assertEqual( self._physstate.get_mass(), PhysicalStateTests.MASS + 18.0,
            "Adding a non-zero delta to a state doesn't properly alter its mass." )


    def test_update( self ):
        self._physstate.update( PhysicalStateTests.TIME_DELTA )

        self.assertEqual( self._physstate.get_volume().x,
            PhysicalStateTests.VOLUME.x + PhysicalStateTests.TIME_DELTA * PhysicalStateTests.VELOCITY[0],
            "Updating the physical state properly updates the x-value of position." )
        self.assertEqual( self._physstate.get_volume().y,
            PhysicalStateTests.VOLUME.y + PhysicalStateTests.TIME_DELTA * PhysicalStateTests.VELOCITY[1],
            "Updating the physical state properly updates the y-value of position." )

        self.assertEqual( self._physstate.get_volume().w, PhysicalStateTests.VOLUME.w,
            "Updating the physical state improperly updates the volume." )
        self.assertEqual( self._physstate.get_volume().h, PhysicalStateTests.VOLUME.h,
            "Updating the physical state improperly updates the volume." )
        self.assertEqual( self._physstate.get_velocity(), PhysicalStateTests.VELOCITY,
            "Updating the physical state improperly updates the velocity." )
        self.assertEqual( self._physstate.get_mass(), PhysicalStateTests.MASS,
            "Updating the physical state improperly updates the mass." )

