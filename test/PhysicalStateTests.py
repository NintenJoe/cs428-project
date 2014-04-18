##  @file PhysicalStateTests.py
#   @author Joseph Ciurej
#   @date Spring 2014
#
#   Test File for the "PhysicalState" Type
#
#   @TODO
#   - Since the 'PhysicalState' is a fairly volatile module, this testing file
#     may need to be changed fairly often.
#   - Update these tests to more thoroughly test the change from `pygame.Rect`
#     to `CompositeHitbox` (particularly in updating all contained hitboxes).

import unittest

import src
from src.CompositeHitbox import *
from src.PhysicalState import *

##  Container class for the test suite that tests the functionality of the
#   "PhysicalState" type.
class PhysicalStateTests( unittest.TestCase ):
    ### Testing Constants ###

    ##  The volume that will be initialized to the test physical state.
    VOLUME = CompositeHitbox( 10, 20,
        [Hitbox(0, 0, 30, 40), Hitbox(0, 0, 10, 10)] )

    ##  The velocity vector that will be initialized to the test physical state.
    VELOCITY = (-5, 2)

    ##  The maass value that will be initialized to the test physical state.
    MASS = 0.4

    ##  The time delta that will be used to test physical state updating.
    TIME_DELTA = 1.0

    ## The maximum health that will be used to test physical state updating.
    MAX_HEALTH = 6

    ## The current health that will be used to test physical state updating.
    CURR_HEALTH = 6

    ### Test Set Up/Tear Down ###

    def setUp( self ):
        self._physstate = PhysicalState( PhysicalStateTests.VOLUME,
            PhysicalStateTests.VELOCITY, PhysicalStateTests.MASS,
            PhysicalStateTests.MAX_HEALTH, PhysicalStateTests.CURR_HEALTH )

    def tearDown( self ):
        self._physstate = None

    ### Testing Functions ###

    def test_default_constructor( self ):
        default_physstate = PhysicalState()

        self.assertEqual( default_physstate.get_volume(), CompositeHitbox(),
            "Default physical state contructor doesn't initialize identity volume." )
        self.assertEqual( default_physstate.get_velocity(), (0, 0),
            "Default physical state contructor doesn't initialize identity velocity." )
        self.assertEqual( default_physstate.get_mass(), 0.0,
            "Default physical state contructor doesn't initialize identity mass." )
        self.assertEqual( default_physstate.get_max_health(), 0,
            "Default physical state contructor doesn't initialize identity\
             maximum health." )
        self.assertEqual( default_physstate.get_curr_health(), 0,
            "Default physical state contructor doesn't initialize identity\
             current health." )


    def test_value_constructor( self ):
        self.assertEqual( self._physstate.get_volume(), PhysicalStateTests.VOLUME,
            "Value physical state contructor doesn't initialize with given volume." )
        self.assertEqual( self._physstate.get_velocity(), PhysicalStateTests.VELOCITY,
            "Value physical state contructor doesn't initialize with given velocity." )
        self.assertEqual( self._physstate.get_mass(), PhysicalStateTests.MASS,
            "Value physical state contructor doesn't initialize with given mass." )
        self.assertEqual( self._physstate.get_max_health(), PhysicalStateTests.MAX_HEALTH,
            "Value physical state contructor doesn't initialize with given maximum health." )
        self.assertEqual( self._physstate.get_curr_health(), PhysicalStateTests.CURR_HEALTH,
            "Value physical state contructor doesn't initialize with given current health." )


    def test_constructor_independence( self ):
        self._physstate._volume.translate( 10, 10 )
        self.assertNotEqual( self._physstate.get_volume(), PhysicalStateTests.VOLUME,
            "Value constructor for physical state doesn't deep copy parameter objects." )


    def test_constructor_independence2( self ):
        state1 = PhysicalState()
        state1.add_delta( self._physstate )
        state2 = PhysicalState()

        self.assertNotEqual(state1.get_volume(), state2.get_volume())
        self.assertNotEqual(state1.get_velocity(), state2.get_velocity())
        self.assertNotEqual(state1.get_mass(), state2.get_mass())
        self.assertNotEqual(state1.get_max_health(), state2.get_max_health())
        self.assertNotEqual(state1.get_curr_health(), state2.get_curr_health())


    def test_equality_operator( self ):
        physstate_default = PhysicalState()
        physstate_copy = PhysicalState(
            PhysicalStateTests.VOLUME,
            PhysicalStateTests.VELOCITY,
            PhysicalStateTests.MASS,
            PhysicalStateTests.MAX_HEALTH,
            PhysicalStateTests.CURR_HEALTH
        )

        self.assertTrue( physstate_default == physstate_default,
            "Equality operator doesn't return true for self equality in simple case." )
        self.assertTrue( self._physstate == self._physstate,
            "Equality operator doesn't return true for self equality in complex case." )

        self.assertTrue( physstate_default == PhysicalState(),
            "Equality operator doesn't return true for two simple equivalent objects." )
        self.assertTrue( physstate_copy == self._physstate,
            "Equality operator doesn't return true for two complex equivalent objects." )

        self.assertFalse( physstate_default == physstate_copy,
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
        self.assertEqual( self._physstate.get_max_health(), PhysicalStateTests.MAX_HEALTH,
            "Adding a zero delta to a state changes its maximum health value." )
        self.assertEqual( self._physstate.get_curr_health(), PhysicalStateTests.CURR_HEALTH,
            "Adding a zero delta to a state changes its current health value." )


    def test_add_complex_delta( self ):
        pos_x_delta = 1
        pos_y_delta = 2
        hitbox_delta = CompositeHitbox( pos_x_delta, pos_y_delta, [Hitbox(0, 0, 20, 20)] )

        vx_delta = -5.0
        vy_delta = -3.0

        mass_delta = 18.0
        max_health_delta = 3
        curr_health_delta = -4

        complex_delta = PhysicalState(
            hitbox_delta,
            (vx_delta, vy_delta),
            mass_delta,
            max_health_delta,
            curr_health_delta
        )
        self._physstate.add_delta( complex_delta )

        self.assertEqual(
            self._physstate.get_volume().get_position()[0],
            PhysicalStateTests.VOLUME.get_position()[0] + pos_x_delta,
            "Adding a non-zero delta to a state doesn't properly alter volume X."
        )
        self.assertEqual(
            self._physstate.get_volume().get_position()[1],
            PhysicalStateTests.VOLUME.get_position()[1] + pos_y_delta,
            "Adding a non-zero delta to a state doesn't properly alter volume Y."
        )
        self.assertEqual(
            self._physstate.get_volume().get_hitbox().w,
            PhysicalStateTests.VOLUME.get_hitbox().w,
            "Adding a non-zero delta to a state doesn't properly alter volume W."
        )
        self.assertEqual(
            self._physstate.get_volume().get_hitbox().h,
            PhysicalStateTests.VOLUME.get_hitbox().h,
            "Adding a non-zero delta to a state doesn't properly alter volume H."
        )

        self.assertEqual(
            self._physstate.get_velocity()[0],
            PhysicalStateTests.VELOCITY[0] + vx_delta,
            "Adding a non-zero delta to a state doesn't properly alter velocity X."
        )
        self.assertEqual(
            self._physstate.get_velocity()[1],
            PhysicalStateTests.VELOCITY[1] + vy_delta,
            "Adding a non-zero delta to a state doesn't properly alter velocity Y."
        )

        self.assertEqual(
            self._physstate.get_mass(),
            PhysicalStateTests.MASS + mass_delta,
            "Adding a non-zero delta to a state doesn't properly alter its mass."
        )

        self.assertEqual(
            self._physstate.get_max_health(),
            PhysicalStateTests.MAX_HEALTH + max_health_delta,
            "Adding a non-zero delta to a state doesn't properly alter its\
             maximum health."
        )

        self.assertEqual(
            self._physstate.get_curr_health(),
            PhysicalStateTests.CURR_HEALTH + curr_health_delta,
            "Adding a non-zero delta to a state doesn't properly alter its\
             current health."
        )

    def test_update( self ):
        self._physstate.update( PhysicalStateTests.TIME_DELTA )

        self.assertEqual(
            self._physstate.get_volume().get_hitbox().x,
            PhysicalStateTests.VOLUME.get_hitbox().x + \
                PhysicalStateTests.TIME_DELTA * PhysicalStateTests.VELOCITY[0],
            "Updating the physical state properly updates the x-value of position."
        )
        self.assertEqual(
            self._physstate.get_volume().get_hitbox().y,
            PhysicalStateTests.VOLUME.get_hitbox().y + \
                PhysicalStateTests.TIME_DELTA * PhysicalStateTests.VELOCITY[1],
            "Updating the physical state properly updates the y-value of position."
        )

        self.assertEqual(
            self._physstate.get_volume().get_hitbox().w,
            PhysicalStateTests.VOLUME.get_hitbox().w,
            "Updating the physical state improperly updates the volume."
        )
        self.assertEqual(
            self._physstate.get_volume().get_hitbox().h,
            PhysicalStateTests.VOLUME.get_hitbox().h,
            "Updating the physical state improperly updates the volume."
        )
        self.assertEqual(
            self._physstate.get_velocity(),
            PhysicalStateTests.VELOCITY,
            "Updating the physical state improperly updates the velocity."
        )
        self.assertEqual(
            self._physstate.get_mass(),
            PhysicalStateTests.MASS,
            "Updating the physical state improperly updates the mass."
        )
        self.assertEqual(
            self._physstate.get_max_health(),
            PhysicalStateTests.MAX_HEALTH,
            "Updating the physical state improperly updates the maximum health."
        )
        self.assertEqual(
            self._physstate.get_curr_health(),
            PhysicalStateTests.CURR_HEALTH,
            "Updating the physical state improperly updates the current health."
        )

