##  @file GameView.py
#   @author Edwin Chan, Joseph Ciurej
#   @date Spring 2014
#
#   Source File for the "GameView" Type
#
#   @TODO
#   High Priority:
#   - 
#   Low Priority:
#   - Make the references to the global functions shorter while maintaining
#     the no 'from [module] import [item]' syntax.
#   - Generalize the constructor function to allow for arbitrary screen
#     dimensions input.
#   - Implement an observer pattern where the `GameView` is the observer
#     and the `GameWorld` is the subject.
#   - Introduce a `Renderable` type from which the `Entity` and `Tile`
#     types derive that identifies the asset paths for these items
#     and loads the graphics for these items.
#   - Add custimization for widgets to allow any widget to be rendered on top
#     of the game view.
#   - Make the `HealthWidget` a generalized widget and render all widgets
#     at once in a similar fashion when more widgets are used.

import os.path
import pygame as PG
from pygame.locals import *

import Globals
from Globals import *
import HealthWidget
from GameWorld import GameWorld
from Animation import Animation
from Event import Event

##  This class is a container and viewing methods for camera,
#   world, and all entities. Its job is to load and construct the
#   GameWorld.
class GameView():
    ### Constructors ###

    ##  Constructs a Game View that will set up the game screen
    def __init__( self ):
        self._tile_graphics = {}
        self._entity_graphics = {}

        self._screen = PG.display.set_mode( Globals.SCREEN_DIMS )
        PG.display.set_caption( Globals.GAME_NAME )

        # NOTE: Module is initialized here so that it's constructed after the
        # video mode is instantiated.
        self._player_health_widget = HealthWidget.HealthWidget()
        # Title Screen, Pause Screen, and Game Over Screen
        self.TITLE_IMAGE = load_image( os.path.join('screens', 'title_screen.png') )
        self.IMAGE_RECT = self.TITLE_IMAGE.get_rect()
        self.GAMEOVER_IMAGE = load_image( os.path.join('screens', 'gameover_screen.png') )
        self.PAUSE_IMAGE = load_image( os.path.join('screens', 'pause_screen.png') )

    ### Methods ###

    ##  Draws the Game World within the camera's viewport.
    #
    #   @param game_world   Game World, which contains information about the world
    #                        and all the entities contained in it.
    def render( self, game_world ):
        self._screen.fill( (0, 0, 0) )

        viewport = game_world.get_viewport()
        tilemap = game_world.get_tilemap()
        entity_list = game_world.get_entities()

        self.render_environment( viewport, tilemap )
        self.render_entities( viewport, entity_list )

        player = game_world._player_entity
        health = 4 if player is None else player.get_curr_health()
        self._player_health_widget.render_to( self._screen, health )

        PG.display.flip()

    ##  Render the environment by reading in a tilemap and a camera.
    #
    #   The function works by reading in a set of tilemaps and then sets up a
    #   dictionary that will map the tile key to a tile image. Then it will
    #   only draw the tiles that are within the camera's viewport.
    #
    #   @param viewport     The camera's view, should be a pygame rect
    #   @param tilemap      2D Array of strings that contain the all the
    #                        information about each tile.
    def render_environment( self, viewport, tilemap ):
        self._load_tilemap_graphics( tilemap )

        num_tiles_x = len( tilemap )
        num_tiles_y = len( tilemap[0] )

        start_idx_x = Globals.clamp( int(viewport.left / Globals.TILE_DIMS[0]), 0, num_tiles_x )
        start_idx_y = Globals.clamp( int(viewport.top / Globals.TILE_DIMS[1]), 0, num_tiles_y )
        final_idx_x = Globals.clamp( int(viewport.right / Globals.TILE_DIMS[0]) + 1, 0, num_tiles_x )
        final_idx_y = Globals.clamp( int(viewport.bottom / Globals.TILE_DIMS[1]) + 1, 0, num_tiles_y )

        for idx_x in range( start_idx_x, final_idx_x ):
            for idx_y in range( start_idx_y, final_idx_y ):
                tile_pos_x = idx_x * Globals.TILE_DIMS[0] - viewport.x
                tile_pos_y = idx_y * Globals.TILE_DIMS[1] - viewport.y
                tile = tilemap[ idx_x ][ idx_y ][ 0 ]

                self._screen.blit(
                    self._get_tile_graphic(tile),
                    (tile_pos_x, tile_pos_y)
                )

    ##  Renders all the entities (player and monsters) onto the screen.
    #
    #   @param viewport     The camera's view, should be a pygame rect
    #   @param entity_list  List of all entities and their information
    def render_entities( self, viewport, entity_list ):
        self._load_entity_graphics( entity_list )

        for entity in entity_list:
            entity_pos_x = entity.get_bbox().x - viewport.x
            entity_pos_y = entity.get_bbox().y - viewport.y

            self._screen.blit(
                self._get_entity_graphic(entity),
                (entity_pos_x, entity_pos_y)
            )

    ### Helper Methods ###

    ##  @return The graphic (given as a `PyGame.Surface`) associated with the
    #    given `Entity` object.
    def _get_entity_graphic( self, entity ):
        entity_animation = self._entity_graphics[ self._calc_entity_key(entity) ]
        animation_time = float( entity.get_status().split()[2] )

        return entity_animation.get_frame( animation_time )

    ##  @return The graphic (given as a `PyGame.Surface`) associated with the
    #    given `Tile` object.
    def _get_tile_graphic( self, tile ):
        return self._tile_graphics[ self._calc_tile_key(tile) ]

    ##  @return True if the graphic asset associated with the given `Entity`
    #    is loaded in the instance view and false otherwise.
    def _is_entity_graphic_loaded( self, entity ):
        return self._calc_entity_key( entity ) in self._entity_graphics

    ##  @return True if the graphic asset associated with the given `Tile`
    #    is loaded in the instance view and false otherwise.
    def _is_tile_graphic_loaded( self, tile ):
        return self._calc_tile_key( tile ) in self._tile_graphics

    ##  Loads all the assets for the tiles contained within the given tile map
    #   into the `self._tile_graphics` dictionary.
    #
    #   @param tilemap A matrix of `Tile` instances to have their assets loaded.
    def _load_tilemap_graphics( self, tilemap ):
        for idx_x in range( len(tilemap) ):
            for idx_y in range( len(tilemap[0]) ):
                tile = tilemap[ idx_x ][ idx_y ][ 0 ]

                if not self._is_tile_graphic_loaded( tile ):
                    tile_key = self._calc_tile_key( tile )
                    tile_path = self._calc_tile_path( tile )

                    self._tile_graphics[ tile_key ] = Globals.load_image( tile_path )

    ##  Loads all the assets for the entities contained within the given entity
    #   list into the `self._tile_graphics` dictionary.
    #
    #   @param entity_list A list of `Entity` instances to have their assets loaded.
    def _load_entity_graphics( self, entity_list ):
        for entity in entity_list:
            if not self._is_entity_graphic_loaded( entity ):
                entity_key = self._calc_entity_key( entity )
                entity_path = self._calc_entity_path( entity )

                self._entity_graphics[ entity_key ] = Animation( entity_path, 33, True )

    ##  @return The asset key string for the given `Entity` object, which
    #    identifies the object's associated rendering assets in the view.
    def _calc_entity_key( self, entity ):
        entity_info = entity.get_status().split()
        return entity_info[0] + "/" + entity_info[1]

    ##  @return The asset key string for the given `Tile` object, which
    #    identifies the object's associated rendering assets in the view.
    def _calc_tile_key( self, tile ):
        # TODO: Change this to be `tile.get_id()` after the change.
        return tile

    ##  @return The path to the sprite sheet image file associated with
    #    the given `Entity` object.
    def _calc_entity_path( self, entity ):
        entity_filename = self._calc_entity_key( entity ) + ".png"
        return os.path.join( "entities", entity_filename )

    ##  @return The path to the sprite sheet image file associated with
    #    the given `Tile` object.
    def _calc_tile_path( self, tile ):
        tile_filename = self._calc_tile_key( tile ) + ".bmp"
        return os.path.join( "tiles", tile_filename )

