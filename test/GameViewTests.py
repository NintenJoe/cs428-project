##  @file GameViewTests.py
#   @author Joseph Ciurej
#   @date Spring 2014
#
#   Test File for the "GameView" Type
#
#   @TODO
#   High Priority:
#   - Refine the tests to assert that only the `Entity` objects that are within
#     the scope of the game viewport are rendered once this functionality is
#     implemented.
#   Low Priority:
#   - Refactor the functionality associated with the `DISPLAY_PATCHERS` to
#     make the code less clunky.
#   - Update the `GameViewTests.WORLD_TILES` matrix to contain `Tile` instances
#     instead of strings.

import unittest
import mock
import src.Globals
import src.HealthWidget

from src.GameView import GameView
from src.GameWorld import GameWorld
from src.Camera import Camera
from src.HashableRect import HashableRect

##  Container class for the test suite that tests the functionality of the
#   "GameView" type.
class GameViewTests( unittest.TestCase ):
    ### Testing Constants ###

    ##  A dictionary containing all the mock patchers for all PyGame display
    #   functions.
    DISPLAY_PATCHERS = {
        "set_mode": mock.patch( "pygame.display.set_mode" ),
        "set_caption": mock.patch( "pygame.display.set_caption" ),
        "flip": mock.patch( "pygame.display.flip" ),
        "load_image": mock.patch( "src.Globals.load_image" ),
        "hwidget": mock.patch( "src.HealthWidget.HealthWidget" )
    }

    ##  A matrix containing the `Tile` objects given by the mock `GameWorld`.
    WORLD_TILES = [
        [ "0", "1" ],
        [ "2", "3" ],
        [ "4", "5" ],
    ]

    ##  A list containing the test `Entity` objects given by the mock `GameWorld`.
    WORLD_ENTITIES = []

    ##  A list containing the test viewport `Rect` given by the mock `GameWorld`.
    WORLD_VIEWPORT = HashableRect( 10, 30, 20, 40 )

    ### Test Set Up/Tear Down ###

    def setUp( self ):
        self._world_mock = mock.Mock( spec=GameWorld )
        self._world_mock.get_entities.return_value = GameViewTests.WORLD_ENTITIES
        self._world_mock.get_tilemap.return_value = GameViewTests.WORLD_TILES
        self._world_mock.get_viewport.return_value = GameViewTests.WORLD_VIEWPORT

        self._setmode_mock = GameViewTests.DISPLAY_PATCHERS[ "set_mode" ].start()
        self._setcapt_mock = GameViewTests.DISPLAY_PATCHERS[ "set_caption" ].start()
        self._flip_mock = GameViewTests.DISPLAY_PATCHERS[ "flip" ].start()
        self._load_image_mock = GameViewTests.DISPLAY_PATCHERS[ "load_image" ].start()
        self._hwidget_mock = GameViewTests.DISPLAY_PATCHERS[ "hwidget" ].start()

        self._display_mock = self._setmode_mock.return_value

        self._view = GameView()

    def tearDown( self ):
        self._world_mock = None
        self._view = None

        [ patcher.stop() for patcher in GameViewTests.DISPLAY_PATCHERS.values() ]

    ### Testing Functions ###

    def test_initialization( self ):
        self.assertTrue( self._setmode_mock.called,
            "Game view doesn't properly initialize PyGame display drivers." )
        self.assertTrue( self._setcapt_mock.called,
            "Game view doesn't properly initialize PyGame display caption." )


    def test_render_initialization( self ):
        self._view.render( self._world_mock )

        self.assertTrue( self._display_mock.fill.called,
            "Game view doesn't properly clear view before rendering." )
        self.assertTrue( self._flip_mock.called,
            "Game view doesn't properly flip the graphics buffer after rendering." )


    def test_render_loading( self ):
        for entity in GameViewTests.WORLD_ENTITIES:
            self.assertFalse( self._view._is_entity_graphic_loaded(entity),
                "Game view improperly loads entity assets before they're needed." )
        for tile in [ t for s in GameViewTests.WORLD_TILES for t in s ]:
            self.assertFalse( self._view._is_tile_graphic_loaded(tile),
                "Game view improperly loads tile assets before they're needed." )

        self._view.render( self._world_mock )

        for entity in GameViewTests.WORLD_ENTITIES:
            self.assertTrue( self._view._is_entity_graphic_loaded(entity),
                "Game view doesn't load entity assets when they're rendered." )
        for tile in [ t for s in GameViewTests.WORLD_TILES for t in s ]:
            self.assertTrue( self._view._is_tile_graphic_loaded(tile),
                "Game view doesn't load tile assets when they're rendered." )


    def test_render_onetile_environment( self ):
        self._world_mock.get_viewport.return_value = HashableRect( 0, 0,
             src.Globals.TILE_DIMS[0] - 1, src.Globals.TILE_DIMS[1] - 1 )
        self._view.render( self._world_mock )

        blit_calls = self._display_mock.blit.call_args_list
        self.assertEqual( len(blit_calls), 1,
            "Game view renders too many environment tiles in simple cases." )

        blit_call = blit_calls[0]
        self.assertEqual( blit_call[0][0], self._view._get_tile_graphic("0"),
            "Game view renders incorrect tiles in simple cases." )
        self.assertEqual( blit_call[0][1], (0, 0),
            "Game view renders improperly offsets tile graphics in simple cases." )


    def test_render_multitile_environment( self ):
        viewport_offset = (
            int(src.Globals.TILE_DIMS[0] / 2),
            int(src.Globals.TILE_DIMS[1] / 2)
        )
        viewport_dims = (
            src.Globals.TILE_DIMS[0],
            src.Globals.TILE_DIMS[1]
        )
        self._world_mock.get_viewport.return_value = HashableRect(
             viewport_offset[0], viewport_offset[1],
             viewport_dims[0], viewport_dims[1]
        )
        self._view.render( self._world_mock )

        blit_calls = self._display_mock.blit.call_args_list
        self.assertEqual( len(blit_calls), 4,
            "Game view renders too few environment tiles in complex cases." )

        self.assertEqual(
            set( [blit_call[0][0] for blit_call in blit_calls] ),
            set( [self._view._get_tile_graphic(str(i)) for i in range(4)] ),
            "Game view renders incorrect tiles in complex cases."
        )
        self.assertEqual(
            blit_calls[0][0][1],
            (0 - viewport_offset[0], 0 - viewport_offset[1]),
            "Game view renders improperly offsets tile graphics in complex cases."
        )


    def test_render_entities( self ):
        pass

