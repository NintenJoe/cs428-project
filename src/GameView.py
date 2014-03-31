##  @file GameView.py
#   @author Edwin Chan
#   @date Spring 2014
#
#   Source File for Viewing 
#
#   @TODO
#   High Priority:
#   - 
#   Low Priority:
#   - Init will take as input the screen size of our game

import os.path
import pygame as PG
from pygame.locals import *

from GameWorld import GameWorld
from Animation import Animation
from Event import Event
from Globals import *

##  This class is a container and viewing methods for camera,
#   world, and all entities. Its job is to load and construct the
#   GameWorld.
class GameView():
    ### Constructors ###

    ##  Constructs a Game View that will set up the game screen
    def __init__(self):
        self._screen = PG.display.set_mode( (640, 480) )

        PG.display.set_caption( GAME_NAME )
        PG.mouse.set_visible( True )

        self._loaded_tiles = {}
        self._loaded_entities = {}

    ### Methods ###

    ##  Draws the Game World within the camera's viewport.
    #
    #   @param game_world   Game World, which contains information about the world
    #                        and all the entities contained in it.
    def render( self, game_world ):
        self._screen.fill( (0, 0, 0) )

        viewport = game_world.get_camera().get_viewport()
        tilemap = game_world.get_tilemap()
        entity_list = game_world.get_entities()

        self.render_environment( viewport, tilemap )
        self.render_entities( viewport, entity_list )

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
        self._load_tiles_for_tilemap( tilemap )

        num_tiles_x = len( tilemap )
        num_tiles_y = len( tilemap[0] )

        start_idx_x = clamp( int(viewport.left / TILE_DIMS[0]), 0, num_tiles_x )
        start_idx_y = clamp( int(viewport.top / TILE_DIMS[1]), 0, num_tiles_y )
        final_idx_x = clamp( int(viewport.right / TILE_DIMS[0]) + 1, 0, num_tiles_x )
        final_idx_y = clamp( int(viewport.bottom / TILE_DIMS[1]) + 1, 0, num_tiles_y )

        for idx_x in range( start_idx_x, final_idx_x ):
            for idx_y in range( start_idx_y, final_idx_y ):
                tile_pos_x = idx_x * TILE_DIMS[0] - viewport.x
                tile_pos_y = idx_y * TILE_DIMS[1] - viewport.y

                tile_id = tilemap[ idx_x ][ idx_y ]

                self._screen.blit( self._loaded_tiles[tile_id], (tile_pos_x, tile_pos_y) )

    ##  Renders all the entities (player and monsters) onto the screen.
    #
    #   @param viewport     The camera's view, should be a pygame rect
    #   @param entity_list  List of all entities and their information
    def render_entities( self, viewport, entity_list ):
        self._load_entities( entity_list )

        for entity in entity_list:
            entity_pos_x = entity.get_hitbox().x - viewport.x
            entity_pos_y = entity.get_hitbox().y - viewport.y

            entity_key = self._get_entity_key( entity )
            entity_animation = self._loaded_entities[ entity_key ]
            game_time = float( entity.get_status().split()[2] )

            self._screen.blit( entity_animation.get_frame(game_time), (entity_pos_x, entity_pos_y) )

    ##  Creates a dictionary called loaded_tiles which maps a tile key to an image
    #
    #   @param tilemap      2D Array of strings that contain the all the
    #                        information about each tile.
    def _load_tiles_for_tilemap( self, tilemap ):
        for idx_x in range( len(tilemap) ):
            for idx_y in range( len(tilemap[0]) ):
                tile_id = tilemap[ idx_x ][ idx_y ]

                if tile_id not in self._loaded_tiles:
                      self._loaded_tiles[ tile_id ] = load_image( ASSET_PATH + "/graphics/tiles/" + tile_id + ".bmp")

    ##  Creates a dictionary called loaded_entities which maps an entity key to a
    #   its corresponding sprite sheet.
    #
    #   @param entity_list  List of all entities and their information
    def _load_entities( self, entity_list ):
        for entity in entity_list:
            entity_key = self._get_entity_key( entity )
            entity_path = self._get_entity_path( entity )

            # TODO: Remove this and replace it with a valid frame count loaded.
            frame_count = 1
            if entity_key == "player idle_1":
                frame_count = 6
            elif entity_key.find( "move" ) != -1:
                frame_count = 4
            elif entity_key.find( "monster" ) !=-1:
                frame_count = 7

            if entity_key not in self._loaded_entities:
                self._loaded_entities[ entity_key ] = Animation( entity_path, frame_count, 33, True )

    ##  Helper function that helps gather the entities' dictionary key
    #
    #   @param entity       The entity in which we need information from
    #
    #   @return             The key which is a combination of an entity's name and state
    def _get_entity_key( self, entity ):
        entity_info = entity.get_status().split()
        return entity_info[0] + " " + entity_info[1]

    ##  Helper function that helps gather the entities' filepath
    #
    #   @param entity       The entity in which we need information from
    #
    #   @return             The filepath for the entity's spritesheet
    def _get_entity_path( self, entity ):
        entity_info = entity.get_status().split()
        return ASSET_PATH + "/graphics/entities/" + entity_info[0] + "/" + entity_info[1] + ".png"

