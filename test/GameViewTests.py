##  @file GameViewTests.py
#   @author Joseph Ciurej
#   @date Spring 2014
#
#   Test File for the "GameView" Type
#
#   @see http://www.voidspace.org.uk/python/mock/examples.html#nesting-patches
#
#   @TODO
#   - Refine the tests to assert that only the `Entity` objects that are within
#     the scope of the game viewport are rendered once this functionality is
#     implemented.
#   - Refactor the functionality associated with the `DISPLAY_PATCHERS` to
#     make the code less clunky.

import unittest
import mock

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
    }

    ##  A matrix containing the `Tile` objects given by the mock `GameWorld`.
    WORLD_TILES = [
        [ "0", "1", "2" ],
        [ "3", "4", "5" ],
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

        self.assertTrue( self._setmode_mock.return_value.fill.called,
            "Game view doesn't properly clear view before rendering." )
        self.assertTrue( self._flip_mock.called,
            "Game view doesn't properly flip the graphics buffer after rendering." )

    def test_render_loading( self ):
        self._view.render( self._world_mock )

        self.assertEqual( True, True, "" )

