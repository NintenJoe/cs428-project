##  @file CompositeHitboxTests.py
#   @author Joseph Ciurej
#   @date 09/04/2014
#
#   Test File for the "CompositeHitbox" Type
#
#   @TODO
#   - Write the implementation in this file!

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

    ### Testing Functions ###

    def test_default_constructor( self ):
        default_hitbox = Hitbox( HitboxTests.BOX_X, HitboxTests.BOX_Y,
            HitboxTests.BOX_W, HitboxTests.BOX_H )

        self.assertEqual( default_hitbox.x, HitboxTests.BOX_X,
            "Default hitbox constructor improperly initializes x-value." )
        self.assertEqual( default_hitbox.y, HitboxTests.BOX_Y,
            "Default hitbox constructor improperly initializes y-value." )
        self.assertEqual( default_hitbox.w, HitboxTests.BOX_W,
            "Default hitbox constructor improperly initializes width." )
        self.assertEqual( default_hitbox.h, HitboxTests.BOX_H,
            "Default hitbox constructor improperly initializes height." )

        self.assertEqual( default_hitbox.htype, HitboxType.DEFAULT,
            "Default hitbox constructor improperly initializes type." )


    def test_value_constructor( self ):
        hitbox = Hitbox( HitboxTests.BOX_X, HitboxTests.BOX_Y,
            HitboxTests.BOX_W, HitboxTests.BOX_H, HitboxTests.BOX_TYPE )

        self.assertEqual( hitbox.x, HitboxTests.BOX_X,
            "Value hitbox constructor improperly initializes x-value." )
        self.assertEqual( hitbox.y, HitboxTests.BOX_Y,
            "Value hitbox constructor improperly initializes y-value." )
        self.assertEqual( hitbox.w, HitboxTests.BOX_W,
            "Value hitbox constructor improperly initializes width." )
        self.assertEqual( hitbox.h, HitboxTests.BOX_H,
            "Value hitbox constructor improperly initializes height." )

        self.assertEqual( hitbox.htype, HitboxTests.BOX_TYPE,
            "Value hitbox constructor improperly initializes type." )


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

        self.assertEqual( default_cbox.get_hitbox(), PG.Rect(0, 0, 0, 0),
            "Default composite hitbox constructor improperly initializes "
            "the container hitbox." )
        self.assertEqual( default_cbox.get_hitboxes(), [],
            "Default composite hitbox constructor contains inner hitboxes "
            "when there should be none." )


    def test_value_constructor( self ):
        self.assertEqual(
            self._cbox.get_hitbox(),
            PG.Rect(
                CompositeHitboxTests.COMPOSITE_X,
                CompositeHitboxTests.COMPOSITE_Y,
                self._hbox1.x + self._hbox1.w,
                self._hbox2.y + self._hbox2.h,
            ),
            "Value composite hitbox constructor improperly initializes "
            "the container hitbox."
        )
        self.assertEqual(
            self._cbox.get_hitboxes(),
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
                )
            ],
            "Value compsite hitbox constuctor improperly initializes inner "
            "hitboxes."
        )


    def test_constructor_independence( self ):
        initial_hbox = copy.deepcopy( self._cbox.get_hitbox() )
        initial_hboxes = copy.deepcopy( self._cbox.get_hitboxes() )

        self._hbox1.x += 5
        self._hbox2.h -= 2

        self.assertEqual( self._cbox.get_hitbox(), initial_hbox,
            "Composite hitbox container volume is dependent on constructor inputs." )
        self.assertEqual( self._cbox.get_hitboxes(), initial_hboxes,
            "Composite hitbox inner hitboxes are depedent on constructor inputs." )


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


    def test_translation( self ):
        self._cbox.translate(
            CompositeHitboxTests.COMPOSITE_X,
            CompositeHitboxTests.COMPOSITE_Y
        )

        self.assertEqual(
            self._cbox.get_hitbox(),
            PG.Rect(
                2 * CompositeHitboxTests.COMPOSITE_X,
                2 * CompositeHitboxTests.COMPOSITE_Y,
                self._hbox1.x + self._hbox1.w,
                self._hbox2.y + self._hbox2.h,
            ),
            "Translation function doesn't properly offset the container "
            "hitbox."
        )
        self.assertEqual(
            self._cbox.get_hitboxes(),
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
            "Translation function doesn't properly offset all the hitboxes "
            "that comprise the composite."
        )


    def test_relative_hitboxes( self ):
        rel_boxes = self._cbox.get_relative_hitboxes()

        self.assertEqual( rel_boxes, [self._hbox1, self._hbox2],
            "Relative hitbox computation improperly offsets output hitboxes." )

        initial_hbox = copy.deepcopy( self._cbox.get_hitbox() )
        initial_hboxes = copy.deepcopy( self._cbox.get_hitboxes() )

        rel_boxes[0].x += 5
        rel_boxes[1].h -= 2

        self.assertEqual( self._cbox.get_hitbox(), initial_hbox,
            "Composite hitbox container volume is dependent on output relative volumes." )
        self.assertEqual( self._cbox.get_hitboxes(), initial_hboxes,
            "Composite hitbox inner hitboxes are depedent on output relative volumes." )

