##  @file HealthWidgetTests.py
#   @author Joseph Ciurej
#   @date Spring 2014
#
#   Test File for the "HealthWidget" Type
#
#   @TODO
#   High Priority:
#   - 
#   Low Priority:
#   - Refactor the functionality associated with the `DISPLAY_PATCHERS` to
#     make the code less clunky.
#   - Once the `HealthWidget` is expanded to include more public access
#     functions, refactor these tests appropriately.
#   - Update the tests to use less hard-coded values once the logic for the
#     `HealthWidget` solidifies.

import unittest
import mock
import pygame
import src.Globals

from src.HealthWidget import HealthWidget

##  Container class for the test suite that tests the functionality of the
#   "HealthWidget" type.
class HealthWidgetTests( unittest.TestCase ):
    ### Testing Constants ###

    ##  A dictionary containing all the mock patchers for all library elements.
    LIB_PATCHERS = {
        "surface": mock.patch( "pygame.Surface" ),
        "scale": mock.patch( "pygame.transform.scale" ),
        "load_image": mock.patch( "src.Globals.load_image" ),
    }

    ##  The rectangle value that will be initialized to the test widget's
    #   rendering space value.
    WIDGET_SPACE = pygame.Rect( 20, 20, 50, 20 )

    ### Test Set Up/Tear Down ###

    def setUp( self ):
        self._view_surface_mock = mock.Mock( spec=pygame.Surface )

        self._surface_mock = HealthWidgetTests.LIB_PATCHERS[ "surface" ].start()
        self._scale_mock = HealthWidgetTests.LIB_PATCHERS[ "scale" ].start()
        self._load_mock = HealthWidgetTests.LIB_PATCHERS[ "load_image" ].start()

        self._hwidget = HealthWidget( HealthWidgetTests.WIDGET_SPACE )

    def tearDown( self ):
        self._hwidget = None

        [ patcher.stop() for patcher in HealthWidgetTests.LIB_PATCHERS.values() ]

    ### Testing Functions ###

    def test_default_initialization( self ):
        default_hwidget = HealthWidget()
        default_render_space = pygame.Rect( 10, 10, 90, 30 )
        self.assertEqual(
             default_hwidget._render_space,
             default_render_space,
            "Default constructor doesn't properly initialize rendering space."
        )

        hwidget_surface_dims = self._surface_mock.call_args_list[ 1 ][ 0 ][ 0 ]
        self.assertEqual(
            hwidget_surface_dims,
            ( default_render_space.w, default_render_space.h ),
            "Default constructor doesn't properly initialize widget dimensions."
        )

        hwidget_icon_dims = self._scale_mock.call_args_list[ 1 ][ 0 ][ 1 ]
        self.assertEqual(
            hwidget_icon_dims,
            ( 16, 20 ),
            "Default constructor doesn't properly initialize health icon dimensions."
        )


    def test_value_initialization( self ):
        value_render_space = HealthWidgetTests.WIDGET_SPACE
        self.assertEqual(
            self._hwidget._render_space,
            value_render_space,
            "Value constructor doesn't properly initialize rendering space."
        )

        hwidget_surface_dims = self._surface_mock.call_args_list[ 0 ][ 0 ][ 0 ]
        self.assertEqual(
            hwidget_surface_dims,
            ( value_render_space.w, value_render_space.h ),
            "Default constructor doesn't properly initialize widget dimensions."
        )

        hwidget_icon_dims = self._scale_mock.call_args_list[ 0 ][ 0 ][ 1 ]
        self.assertEqual(
            hwidget_icon_dims,
            ( 6, 10 ),
            "Value constructor doesn't properly initialize health icon dimensions."
        )


    def test_constructor_independence( self ):
        value_render_space = pygame.Rect( 10, 20, 30, 40 )
        value_hwidget = HealthWidget( value_render_space )

        value_render_space.x = 5

        self.assertNotEqual(
            value_hwidget._render_space,
            value_render_space,
            "Value constructor doesn't deep copy parameter objects."
        )


    def test_empty_render( self ):
        self._hwidget.render_to( self._view_surface_mock, 0 )

        widget_blit_calls = self._hwidget._widget_surface.blit.call_args_list
        self.assertEqual(
            len( widget_blit_calls ),
            0,
            "Rendering an empty widget improperly renders > 0 health icons."
        )

        view_blit_calls = self._view_surface_mock.blit.call_args_list
        self.assertEqual(
            len( view_blit_calls ),
            1,
            "Rendering an empty widget causes the widget to not be drawn."
        )
        widget_blit_location = view_blit_calls[ 0 ][ 0 ][ 1 ]
        self.assertEqual(
            widget_blit_location,
            HealthWidgetTests.WIDGET_SPACE.topleft,
            "Rendering an empty widget causes the to be drawn in the wrong place."
        )


    def test_nonempty_render( self ):
        self._hwidget.render_to( self._view_surface_mock, 4 )

        widget_blit_calls = self._hwidget._widget_surface.blit.call_args_list
        self.assertEqual(
            len( widget_blit_calls ),
            4,
            "Rendering a non-empty widget renders an improper number of health icons."
        )

        view_blit_calls = self._view_surface_mock.blit.call_args_list
        self.assertEqual(
            len( view_blit_calls ),
            1,
            "Rendering an non-empty widget causes the widget to not be drawn."
        )
        widget_blit_location = view_blit_calls[ 0 ][ 0 ][ 1 ]
        self.assertEqual(
            widget_blit_location,
            HealthWidgetTests.WIDGET_SPACE.topleft,
            "Rendering an non-empty widget causes the to be drawn in the wrong place."
        )

