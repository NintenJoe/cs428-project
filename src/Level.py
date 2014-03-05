##  @file Level.py
#   @author Andrew Exo
#   @date 2/20/2014
#
#   Source File for the "Level" Type
#
#   @TODO
#   - 

import os.path
import string
import pygame as PG
from Globals import *

##  This class is a container for a connected Segment graph.
class Level():
    ### Constructors ###

    ##  Creates an empty Level
    #   
    #   @param id A unique identifier for the level
    def __init__(self, id):
        self.id = id
        # Segment with entry point
        self.root = None
        # has the form { id => Segment }
        self.segments = {}
        # has the form { Color => Surface }
        self.tiles = {}
        # has the form { id => Surface }
        self.images = {}

    ### Methods ###

    ##  Adds the segment to the level by adding it to the
    #   segment dictionary.
    def add_segment(self, segment):
        self.segments[segment.id] = segment
        # set root if segment has entry point
        if (segment.entry_point != None):
            self.root = segment

    ##  Creates transitions between segments
    def connect(self):
        for segment_i in self.segments.values():
            for segment_j in self.segments.values():
                for tti in segment_i.transition_tiles:
                    for ttj in segment_j.transition_tiles:
                        if (tti[1] == ttj[1]):
                            if (segment_i != segment_j or tti[0] != ttj[0]):
                                segment_i.add_transition(tti[0],segment_j,ttj[0])
                                segment_j.add_transition(ttj[0],segment_i,tti[0])

    def load_tiles(self):
        # read level tiles file
        tiles_filename = os.path.join('assets','data','segdata', self.id + '.tiles')
        tiles_file = open(tiles_filename, 'r')

        for line in tiles_file:
            divider = string.find(line,':')
            color_str = line[:divider]
            tile_file = line[divider+1:].rstrip() + '.bmp'
            tile = load_image(join_paths("tiles", tile_file))
            self.tiles[tuple(PG.Color(color_str))] = tile

        tiles_file.close()

    def generate_images(self):
        for segment in self.segments.values():
            image = segment.get_image(self.tiles)
            self.images[segment.id] = image

    def get_image(self, seg_id):
        return self.images[seg_id]