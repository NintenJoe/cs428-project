##  @file CompositeHitboxTests.py
#   @author Joseph Ciurej
#   @date 09/04/2014
#
#   Test File for the "CompositeHitbox" Type
#
#   @TODO
#   High Priority:
#   - 
#   Low Priority:
#   - Add more tests for the `CompositeHitbox` test for `adopt_template`
#     function.
#   - Add tests to assert the anchor adjustment occurs properly.

import unittest
import collections
import copy
import pygame as PG

import src
from src.CompositeHitbox import *

##  Container class for the test suite that tests the functionality of the
#   "Hitbox" type.
class HitboxTests( unittest.TestCase ):
    ### Testing Constants ###

    ##  The x-coordinate to be assigned to the test `Hitbox` instance.
    BOX_X = 5

    ##  The y-coordinate to be assigned to the test `Hitbox` instance.
    BOX_Y = 10

    ##  The width to be assigned to the test `Hitbox` instance.
    BOX_W = 15

    ##  The height to be assigned to the test `Hitbox` instance.
    BOX_H = 20

    ##  The classification to be assigned to test `Hitbox` instance.
    BOX_TYPE = HitboxType.HURT

    ### Test Set Up/Tear Down ###

    def setUp( self ):
        self._default_hbox = Hitbox( HitboxTests.BOX_X, HitboxTests.BOX_Y,
            HitboxTests.BOX_W, HitboxTests.BOX_H )
        self._value_hbox = Hitbox( HitboxTests.BOX_X, HitboxTests.BOX_Y,
            HitboxTests.BOX_W, HitboxTests.BOX_H, HitboxTests.BOX_TYPE )

    def tearDown( self ):
        self._default_hbox = None
        self._value_hbox = None

    ### Testing Functions ###

    def test_default_constructor( self ):
        self.assertEqual( self._default_hbox.x, HitboxTests.BOX_X,
            "Default constructor improperly initializes x-value." )
        self.assertEqual( self._default_hbox.y, HitboxTests.BOX_Y,
            "Default constructor improperly initializes y-value." )
        self.assertEqual( self._default_hbox.w, HitboxTests.BOX_W,
            "Default constructor improperly initializes width." )
        self.assertEqual( self._default_hbox.h, HitboxTests.BOX_H,
            "Default constructor improperly initializes height." )

        self.assertEqual( self._default_hbox.htype, HitboxType.DEFAULT,
            "Default constructor improperly initializes type." )


    def test_value_constructor( self ):
        self.assertEqual( self._value_hbox.x, HitboxTests.BOX_X,
            "Value constructor improperly initializes x-value." )
        self.assertEqual( self._value_hbox.y, HitboxTests.BOX_Y,
            "Value constructor improperly initializes y-value." )
        self.assertEqual( self._value_hbox.w, HitboxTests.BOX_W,
            "Value constructor improperly initializes width." )
        self.assertEqual( self._value_hbox.h, HitboxTests.BOX_H,
            "Value constructor improperly initializes height." )

        self.assertEqual( self._value_hbox.htype, HitboxTests.BOX_TYPE,
            "Value constructor improperly initializes type." )


    def test_repr_operator( self ):
        self.assertEqual( repr(self._default_hbox), HitboxType.DEFAULT,
            "Default hitbox doesn't have the correct representation string." )

        self.assertEqual( repr(self._value_hbox), HitboxTests.BOX_TYPE,
            "Value hitbox doesn't have the correct representation string." )


    def test_hash_operator( self ):
        hitbox = Hitbox( 0, 0, 0, 0 )
        deepcopy_hitbox = Hitbox( 0, 0, 0, 0 )
        shallowcopy_hitbox = hitbox

        hashtable = collections.defaultdict(int)
        hashtable[ hitbox ] = 10

        self.assertEqual( hashtable[hitbox], 10,
            "Hitbox hash function doesn't guarantee determinism." )
        self.assertEqual( hashtable[shallowcopy_hitbox], 10,
            "Hitbox hash function doesn't support shallow copy equivalence." )
        self.assertNotEqual( hashtable[deepcopy_hitbox], 10,
            "Hitbox hash function doesn't improperly map by object equality "
            "and not object instance." )


    def test_copy_ip( self ):
        copy_hbox = Hitbox( 0, 0, 0, 0 )
        copy_hbox.copy_ip( self._value_hbox )
        self._value_hbox.x = 0
        self._value_hbox.y = -2

        self.assertEqual( copy_hbox.x, HitboxTests.BOX_X,
            "Copy in-place operation improperly initializes x-value." )
        self.assertEqual( copy_hbox.y, HitboxTests.BOX_Y,
            "Copy in-place operation improperly initializes y-value." )
        self.assertEqual( copy_hbox.w, HitboxTests.BOX_W,
            "Copy in-place operation improperly initializes width." )
        self.assertEqual( copy_hbox.h, HitboxTests.BOX_H,
            "Copy in-place operation improperly initializes height." )

        self.assertEqual( copy_hbox.htype, HitboxTests.BOX_TYPE,
            "Copy in-place operation improperly initializes type." )


##  Container class for the test suite that tests the functionality of the
#   "CompositeHitbox" type.
class CompositeHitboxTests( unittest.TestCase ):
    ### Testing Constants ###

    ##  The x-coordinate to be assigned to the test `CompositeHitbox` instance.
    COMPOSITE_X = 200

    ##  The y-coordinate to be assigned to the test `CompositeHitbox` instance.
    COMPOSITE_Y = 400

    ### Test Set Up/Tear Down ###

    def setUp( self ):
        self._hbox1 = Hitbox( 9, 1, 3, 6, HitboxType.VULNERABLE )
        self._hbox2 = Hitbox( 2, 4, 7, 10, HitboxType.HURT )

        self._cbox = CompositeHitbox(
            CompositeHitboxTests.COMPOSITE_X,
            CompositeHitboxTests.COMPOSITE_Y,
            [ self._hbox1, self._hbox2 ]
        )

    def tearDown( self ):
        self._hbox1 = None
        self._hbox2 = None

        self._cbox = None

    ### Testing Functions ###

    def test_default_constructor( self ):
        default_cbox = CompositeHitbox()

        self.assertEqual(
            default_cbox.get_bounding_box(),
            Hitbox( 0, 0, 0, 0 ),
            "Default constructor improperly initializes the composite's bounding box."
        )

        self.assertEqual(
            default_cbox.get_inner_boxes()[0:2],
            [ Hitbox(0, 0, 0, 0, HitboxType.INTANGIBLE) for i in range(2) ],
            "Default constructor improperly  initializes inner hitboxes."
        )


    def test_value_constructor( self ):
        self.assertEqual(
            self._cbox.get_bounding_box(),
            PG.Rect(
                CompositeHitboxTests.COMPOSITE_X,
                CompositeHitboxTests.COMPOSITE_Y,
                self._hbox1.x + self._hbox1.w,
                self._hbox2.y + self._hbox2.h,
            ),
            "Value constructor improperly initializes the composite's bounding box."
        )

        self.assertEqual(
            self._cbox.get_inner_boxes()[0:2],
            [
                Hitbox(
                    CompositeHitboxTests.COMPOSITE_X + self._hbox1.x,
                    CompositeHitboxTests.COMPOSITE_Y + self._hbox1.y,
                    self._hbox1.w,
                    self._hbox1.h
                ), Hitbox(
                    CompositeHitboxTests.COMPOSITE_X + self._hbox2.x,
                    CompositeHitboxTests.COMPOSITE_Y + self._hbox2.y,
                    self._hbox2.w,
                    self._hbox2.h
                ),
            ],
            "Value constuctor improperly initializes inner hitboxes."
        )


    def test_constructor_independence( self ):
        initial_hbox = copy.deepcopy( self._cbox.get_bounding_box() )
        initial_hboxes = copy.deepcopy( self._cbox.get_inner_boxes() )

        self._hbox1.x += 5
        self._hbox2.h -= 2

        self.assertEqual(
            self._cbox.get_bounding_box(),
            initial_hbox,
            "Composite bounding volume is dependent on constructor input values."
        )
        self.assertEqual(
            self._cbox.get_inner_boxes(),
            initial_hboxes,
            "Composite inner hitboxes are dependent on constructor input values."
        )


    def test_equality_operator( self ):
        cbox_default = CompositeHitbox()
        cbox_copy = CompositeHitbox(
            CompositeHitboxTests.COMPOSITE_X,
            CompositeHitboxTests.COMPOSITE_Y,
            [ self._hbox1, self._hbox2 ]
        )

        self.assertTrue( cbox_default == cbox_default,
            "Equality operator doesn't return true for self equality in simple case." )
        self.assertTrue( self._cbox == self._cbox,
            "Equality operator doesn't return true for self equality in complex case." )

        self.assertTrue( cbox_default == CompositeHitbox(),
            "Equality operator doesn't return true for two simple equivalent objects." )
        self.assertTrue( cbox_copy == self._cbox,
            "Equality operator doesn't return true for two complex equivalent objects." )

        self.assertFalse( cbox_default == cbox_copy,
            "Equality operator improperly returns true for two unequivalent objects." )


    def test_adopt_template( self ):
        default_cbox = CompositeHitbox()
        default_cbox.adopt_template( self._cbox )

        default_cbox.translate(
            CompositeHitboxTests.COMPOSITE_X,
            CompositeHitboxTests.COMPOSITE_Y
        )

        self.assertEqual(
            default_cbox,
            self._cbox,
            "Template adoption operation improperly changes inner box values."
        )


    def test_translation( self ):
        self._cbox.translate(
            CompositeHitboxTests.COMPOSITE_X,
            CompositeHitboxTests.COMPOSITE_Y
        )

        self.assertEqual(
            self._cbox.get_bounding_box(),
            Hitbox(
                2 * CompositeHitboxTests.COMPOSITE_X,
                2 * CompositeHitboxTests.COMPOSITE_Y,
                self._hbox1.x + self._hbox1.w,
                self._hbox2.y + self._hbox2.h,
            ),
            "Translation function doesn't properly offset the bounding hitbox."
        )
        self.assertEqual(
            self._cbox.get_inner_boxes()[0:2],
            [
                Hitbox(
                    2 * CompositeHitboxTests.COMPOSITE_X + self._hbox1.x,
                    2 * CompositeHitboxTests.COMPOSITE_Y + self._hbox1.y,
                    self._hbox1.w,
                    self._hbox1.h
                ), Hitbox(
                    2 * CompositeHitboxTests.COMPOSITE_X + self._hbox2.x,
                    2 * CompositeHitboxTests.COMPOSITE_Y + self._hbox2.y,
                    self._hbox2.w,
                    self._hbox2.h
                )
            ],
            "Translation function doesn't properly offset all the inner hitboxes."
        )


    def test_relative_hitboxes( self ):
        rel_boxes = self._cbox.get_inner_boxes_relative()[0:2]

        self.assertEqual(
            rel_boxes,
            [self._hbox1, self._hbox2],
            "Relative hitbox computation improperly offsets output hitboxes."
        )

        initial_hbox = copy.deepcopy( self._cbox.get_bounding_box() )
        initial_hboxes = copy.deepcopy( self._cbox.get_inner_boxes() )
        rel_boxes[0].x += 5
        rel_boxes[1].h -= 2

        self.assertEqual(
            self._cbox.get_bounding_box(),
            initial_hbox,
            "Composite bounding volume is dependent on output relative volumes."
        )
        self.assertEqual(
            self._cbox.get_inner_boxes(),
            initial_hboxes,
            "Composite inner hitboxes are depedent on output relative volumes."
        )

