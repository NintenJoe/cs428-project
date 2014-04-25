##  @file AnimationTests.py
#   @author Joseph Ciurej
#   @date Spring 2014
#
#   Test File for the "Animation" Type
#
#   @TODO
#   High Priority:
#   - 
#   Low Priority:
#   - Add tests to ensure that the calculation functionality for the frame
#     widths and heights are working properly.
#   - Refactor the functionality associated with the `DISPLAY_PATCHERS` to
#     make the code less clunky.

import unittest
import mock
import pygame as PG
import src.Globals

from src.Animation import Animation

##  Container class for the test suite that tests the functionality of the
#   "Animation" type.
class AnimationTests( unittest.TestCase ):
    ### Testing Constants ###

    ##  The mock file name that will be assigned to the test animation object.
    ANIM_FILENAME = "test.png"

    ##  The mock total width that will be assigned to the test animation object.
    ANIM_TOTALWIDTH = 20

    ##  The mock total height that will be assigned to the test animation object.
    ANIM_TOTALHEIGHT = 10

    ##  The amount of time per frame that will be assigned to the test animation.
    ANIM_FRAMETIME = 5

    ##  The looping conitional that will be assigned to the test animation.
    ANIM_LOOPING = True


    ##  The rectangle representing the first frame for the test animation.
    ANIM_FIRSTFRAME = PG.Rect( 0, 0, ANIM_TOTALWIDTH / 2, ANIM_TOTALHEIGHT )

    ##  The rectangle representing the last frame for the test animation.
    ANIM_LASTFRAME = PG.Rect( ANIM_TOTALWIDTH / 2, 0, ANIM_TOTALWIDTH / 2, ANIM_TOTALHEIGHT )


    ##  A dictionary containing all the mock patchers for all library elements.
    LIB_PATCHERS = {
        "load_image": mock.patch( "src.Globals.load_image" ),
    }

    ### Test Set Up/Tear Down ###

    def setUp( self ):
        self._load_mock = AnimationTests.LIB_PATCHERS[ "load_image" ].start()
        # TODO: This is a bit of a hack that should be removed and replaced
        # with a `MagicMock` reset.
        self._load_mock.return_value = mock.MagicMock( **{
            "get_width.return_value": AnimationTests.ANIM_TOTALWIDTH,
            "get_height.return_value": AnimationTests.ANIM_TOTALHEIGHT
        } )

        self._default_anim = Animation( AnimationTests.ANIM_FILENAME )
        self._value_anim = Animation(
            AnimationTests.ANIM_FILENAME,
            AnimationTests.ANIM_FRAMETIME,
            AnimationTests.ANIM_LOOPING
        )

    def tearDown( self ):
        self._default_anim = None
        self._value_anim = None

        [ patcher.stop() for patcher in AnimationTests.LIB_PATCHERS.values() ]

    ### Testing Functions ###

    def test_default_initialization( self ):
        self.assertEqual(
            self._default_anim._frame_width,
            AnimationTests.ANIM_TOTALWIDTH,
            "Default constructor improperly initializes the frame width."
        )
        self.assertEqual(
            self._default_anim._frame_height,
            AnimationTests.ANIM_TOTALHEIGHT,
            "Default constructor improperly initializes the frame height."
        )
        self.assertEqual(
            self._default_anim._frame_count,
            1,
            "Default constructor improperly initializes the frame count."
        )

        self.assertEqual(
            self._default_anim._frame_time,
            33,
            "Default constructor improperly initializes the frame time."
        )
        self.assertEqual(
            self._default_anim._looping,
            False,
            "Default constructor improperly initializes the looping flag."
        )


    def test_value_initialization( self ):
        self.assertEqual(
            self._value_anim._frame_width,
            AnimationTests.ANIM_TOTALWIDTH,
            "Value constructor improperly initializes the frame width."
        )
        self.assertEqual(
            self._value_anim._frame_height,
            AnimationTests.ANIM_TOTALHEIGHT,
            "Value constructor improperly initializes the frame height."
        )
        self.assertEqual(
            self._value_anim._frame_count,
            1,
            "Value constructor improperly initializes the frame count."
        )

        self.assertEqual(
            self._value_anim._frame_time,
            AnimationTests.ANIM_FRAMETIME,
            "Value constructor improperly initializes the frame time."
        )
        self.assertEqual(
            self._value_anim._looping,
            AnimationTests.ANIM_LOOPING,
            "Value constructor improperly initializes the looping flag."
        )


    def test_get_frame( self ):
        self._value_anim._frame_width = AnimationTests.ANIM_TOTALWIDTH / 2
        self._value_anim._frame_count = 2

        self._value_anim.get_frame( 0 )
        sheet_ssurf_calls = self._value_anim.get_sheet().subsurface.call_args_list
        self.assertEqual(
            len( sheet_ssurf_calls ),
            1,
            "Retrieving a single frame causes too many croppings to be performed."
        )

        first_frame_bounds = sheet_ssurf_calls[ 0 ][ 0 ][ 0 ]
        self.assertEqual(
            first_frame_bounds,
            AnimationTests.ANIM_FIRSTFRAME,
            "Retrieving the first frame produces incorrect frame bounds."
        )

        self._value_anim.get_frame( AnimationTests.ANIM_FRAMETIME )
        last_frame_bounds = self._value_anim.get_sheet().subsurface.call_args_list[ 1 ][ 0 ][ 0 ]
        self.assertEqual(
            last_frame_bounds,
            AnimationTests.ANIM_LASTFRAME,
            "Retrieving the final frame produces incorrect frame bounds."
        )


    def test_get_frame_looping( self ):
        looping_anim = Animation(
            AnimationTests.ANIM_FILENAME,
            AnimationTests.ANIM_FRAMETIME,
            True
        )
        looping_anim._frame_width = AnimationTests.ANIM_TOTALWIDTH / 2
        looping_anim._frame_count = 2

        looping_anim.get_frame( 2 * AnimationTests.ANIM_FRAMETIME - 1 )
        last_frame_bounds = looping_anim.get_sheet().subsurface.call_args_list[ 0 ][ 0 ][ 0 ]
        self.assertEqual(
            last_frame_bounds,
            AnimationTests.ANIM_LASTFRAME,
            "Retrieiving the frame before the end improperly causes animation loop."
        )

        looping_anim.get_frame( 2 * AnimationTests.ANIM_FRAMETIME + 1 )
        loop_frame_bounds = looping_anim.get_sheet().subsurface.call_args_list[ 1 ][ 0 ][ 0 ]
        self.assertEqual(
            loop_frame_bounds,
            AnimationTests.ANIM_FIRSTFRAME,
            "Retrieving the frame after the end doesn't cause animation loop."
        )


    def test_get_frame_nonlooping( self ):
        nonlooping_anim = Animation(
            AnimationTests.ANIM_FILENAME,
            AnimationTests.ANIM_FRAMETIME,
            False
        )
        nonlooping_anim._frame_width = AnimationTests.ANIM_TOTALWIDTH / 2
        nonlooping_anim._frame_count = 2

        nonlooping_anim.get_frame( 2 * AnimationTests.ANIM_FRAMETIME - 1 )
        last_frame_bounds = nonlooping_anim.get_sheet().subsurface.call_args_list[ 0 ][ 0 ][ 0 ]
        self.assertEqual(
            last_frame_bounds,
            AnimationTests.ANIM_LASTFRAME,
            "Retrieiving the frame before the end improperly causes loops."
        )

        nonlooping_anim.get_frame( 2 * AnimationTests.ANIM_FRAMETIME + 1 )
        stay_frame_bounds = nonlooping_anim.get_sheet().subsurface.call_args_list[ 1 ][ 0 ][ 0 ]
        self.assertEqual(
            stay_frame_bounds,
            AnimationTests.ANIM_LASTFRAME,
            "Retrieving the frame after the end improperly causes animation loop."
        )

