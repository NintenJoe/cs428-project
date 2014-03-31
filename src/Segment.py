##  @file Segment.py
#   @author Joseph Ciurej
#   @date Fall 2012 (Updated Winter 2014)
#
#   Module file for the "Segment" Type
#
#   @TODO
#   High Priority:
#   - Clean up the comments within this file, especially the in-line comments.
#   - Reformat the comments so that they follow the new style guidelines (triple
#     punctuation on class areas, etc.).
#   - Enforce an 80-character limit on the code contained within this file.
#   Low Priority:
#   - Fix the problems associated with fixed to free camera transitioning.

import struct
import pygame as PG
from os.path import join as join_paths
from Globals import *

##  A representation of a portion of the game world, which is composed of a 
#   matrix of tiles.  A segment instance handles all the assets associated with
#   the background and provides collision information for the game world.
class Segment():

    # Constructors #

    ##  Constructs a segment based on a segment ID and an entry point coordinate.
    #   
    #   @param segment_id The identification number of the segment to be constructed.
    #   @param entry_point The coordinate within the current segment at which the 
    #       player should be placed (defaults to the origin coordinate) (given in
    #       terms of tile coordinates).
    def __init__(self, id, surface):
        # Identifier for the current segment.
        self.id = id

        # The point at which the segment was entered by the player.
        self.entry_point = None

        # The width of the tile matrix (in number of tiles).
        self.width = surface.get_width()
        # The height of the tile matrix (in number of tiles).
        self.height = surface.get_height()

        # The surface of the GIF file for the segment
        self.data_surface = surface

        # edges to other segments, of the form:
        # { (x,y) => (dest_segment, (dest_x,dest_y)) }
        self.transitions = {}

        # initial position of entities, of the form:
        # { (x,y) => Entity Type (string) }
        self.entities = {}

        # Find transition and entry point tiles
        self.transition_tiles = []
        special_tiles = self._find_special_tiles()
        for tile in special_tiles:
            if (tile[1] == (255,0,0)):
                self.entry_point = tile[0]
            elif (tile[1][0] == tile[1][1] == tile[1][2]): # color is grayscale
                self.transition_tiles.append(tile)
            elif (tile[1] == (0,0,255)):
                self.entities[tile[0]] = "monster"

    # Methods #

    ##  Retrieves the image information regarding the segment and returns it as
    #   a pygame surface.
    #   
    #   @note The dimensions of the individual tiles of the segment are determined
    #   by the uniform dimensions of the tile images associated with the game
    #   project that utilizes the code.  This may cause slowdowns for very high
    #   resolution textures.
    #   
    #   @return A pygame surface that contains all the image information loaded into
    #   the segment currently.
    def get_image(self, tiles):
        tile_tex = tiles.values()[0]
        tile_dims = tile_tex.get_rect()

        seg_image = PG.Surface(
            (tile_dims.width * self.width, tile_dims.height * self.height),
            tile_tex.get_flags(), tile_tex.get_bitsize(), tile_tex.get_masks()
        )

        for x in range( 0, self.width ):
            for y in range( 0, self.height ):
                color = tuple(self.data_surface.get_at((x,y)))
                seg_image.blit(tiles[color], (x * tile_dims.width, y * tile_dims.height))

        return seg_image

    ##  Retrieves the collision map associated with the segment, which includes
    #   all of the collision information for the segment (i.e. collision information
    #   with the background).
    #   
    #   @return A two-dimensional Boolean array in column-major order that contains
    #   collision information.  If a cell at 'collisionmap[x][y]' is true, then
    #   the segment cell is solid.
    def get_collisionmap(self):
        collisionmap = []

        for x in range( 0, self.width ):
            collision_column = []

            for y in range( 0, self.height ):
                collision_column.append( self._tile_tangible(x, y) )

            collisionmap.append( collision_column )

        return collisionmap

    ##  Adds a transition to another segment
    #
    #   @param src A tuple of the form (x,y) representing the location of the
    #              transition in this segment.
    #   @param dest_segment The segment that the transition goes to.
    #   @param dest A tuple of the form (x,y) representing the location of the
    #              transition in the destination segment.
    def add_transition(self, src, dest_segment, dest):
        self.transitions[src] = (dest_segment, dest)

    # Helper Functions #

    ##  Given the coordinates of a tile within the segment, this function indicates
    #   whether the tile at that location is tangible.
    #   
    #   @todo Currently only opaque black (0,0,0,255) is considered tangible. This needs 
    #         to change to a set of colors so walls can have different tiles. A possible
    #         solution is to make alpha=255 the tangibility determinant.
    #   
    #   @param x The x-coordinate of the tile that will be tested for tangibility.
    #   @param y The y-coordinate of the tile that will be tested for tangibility.
    #   @return True if the tile is tangible (should cause collisions) and false
    #       otherwise.
    def _tile_tangible(self, x, y):
        return self.data_surface.get_at((x,y)) == (0,0,0,255)

    ##  Finds certain types of tiles in the segments data surface.
    #
    #   @return A list of tuples of the form:
    #       ((x,y),pygame.Color)
    def _find_special_tiles(self):
        tiles = []
        for x in range(0, self.width):
            for y in range(0,self.height):
                color = self.data_surface.get_at((x,y))
                if (color != (0,0,0) and color != (255,255,255)):
                    tiles.append(((x,y),color))
        return tiles

    #   @return A list of the entities in this segment.
    def get_entities(self):
        return self.entities