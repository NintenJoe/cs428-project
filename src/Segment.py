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

import string
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
    def __init__(self, id):
        # Identifier for the current segment.
        self.id = id

        # The width of the tile matrix (in number of tiles).
        self.width = 0
        # The height of the tile matrix (in number of tiles).
        self.height = 0

        # 2d array of Tiles
        self.tiles = []

        # edges to other segments, of the form:
        # { (x,y) => (dest_segment, (dest_x,dest_y)) }
        self.transitions = {}

        # initial position of entities, of the form:
        # ( (x,y), entity_id )
        self.entities = []

        self._setup_tiles()
        self._setup_entities()

        # Find transition and entry point tiles
        self.transition_tiles = []
        special_tiles = self._find_special_tiles()
        for tile in special_tiles:
            if (tile[1][0] == tile[1][1] == tile[1][2]): # color is grayscale
                self.transition_tiles.append(tile)

    # Methods #

    ##  Adds a transition to another segment
    #
    #   @param src A tuple of the form (x,y) representing the location of the
    #              transition in this segment.
    #   @param dest_segment The segment that the transition goes to.
    #   @param dest A tuple of the form (x,y) representing the location of the
    #              transition in the destination segment.
    def add_transition(self, src, dest_segment, dest):
        self.transitions[src] = (dest_segment, dest)

    ##  Returns the tile information
    #
    #   @return A 2d array of tiles.
    #           Tiles have form (tile_id, bool tangible)
    def get_tiles(self):
        return self.tiles

    ##  Returns the entity information
    #
    #   @return A list of the entities in this segment.
    #           List is of form ( (x,y), entity_id )
    def get_entities(self):
        return self.entities

    ##  Returns the segment size
    #
    #   @return A tuple of the level size. It is not multiplied by the tile size.
    def get_dims(self):
        return (self.width, self.height)

    ##  @return A tuple of the form (pw, ph) which contains the pixel dimensions
    #           of the segment.
    def get_pixel_dims(self):
        return (TILE_DIMS[0]*self.width, TILE_DIMS[1]*self.height)

    # Helper Functions #

    ##  Finds certain types of tiles in the segments data surface.
    #
    #   @return A list of tuples of the form:
    #       ((x,y),pygame.Color)
    def _find_special_tiles(self):
        tiles = []
        return tiles

    ##  Initializes the tile array
    #
    def _setup_tiles(self):
        surface_filename = os.path.join('assets','data','segdata', self.id + '.gif')
        surface = PG.image.load(surface_filename)

        self.width = surface.get_width()
        self.height = surface.get_height()

        tiles = self._load_tiles_file()

        for x in range(0, self.width):
            self.tiles.append([])
            for y in range(0, self.height):
                color = surface.get_at((x,y))
                self.tiles[x].append(tiles[tuple(color)])

    ##  Initializes the entity list
    #
    def _setup_entities(self):
        entities_filename = os.path.join('assets','data','segdata', self.id + 'e.gif')
        entity_surface = PG.image.load(entities_filename)

        entities = self._load_entities_file()

        for x in range(0, self.width):
            for y in range(0, self.height):
                color = entity_surface.get_at((x,y))
                if (tuple(color) in entities):
                    self.entities.append(((x,y), entities[tuple(color)]))

    ##  Loads the mapping from color to (tile_id, tangible)
    #
    #   @return A dict of the form { color_tuple -> (tile_id,tangible) }
    def _load_tiles_file(self):
        tiles = {}

        tiles_filename = os.path.join('assets','data','segdata','tiles')
        tiles_file = open(tiles_filename, 'r')

        for line in tiles_file:
            # find dividers
            d1 = string.find(line,':')
            d2 = string.find(line[d1+1:],':')

            color_str = line[:d1]
            tile_id = line[d1+1:d1+d2+1]
            tangible = (line[d1+d2+2:].rstrip()) == 't'

            color = PG.Color(color_str)
            tiles[tuple(color)] = (tile_id,tangible)

        tiles_file.close()

        return tiles

    ## Loads the mapping from color to entity_id
    #
    #   @return A dict of the form { color_tuple -> entity_id }
    def _load_entities_file(self):
        entities = {}

        entities_filename = os.path.join('assets','data','segdata','entities')
        entities_file = open(entities_filename, 'r')

        for line in entities_file:
            # find dividers
            divider = string.find(line,':')

            color_str = line[:divider]
            entity_id = line[divider+1:].rstrip()

            color = PG.Color(color_str)
            entities[tuple(color)] = entity_id

        entities_file.close()

        return entities
