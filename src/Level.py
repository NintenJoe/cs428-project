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
        # has the form { id => Segment }
        self.segments = {}

    ### Methods ###

    ##  Adds the segment to the level by adding it to the segment dictionary.
    #
    #   @param segment The segment object to be added to the level
    def add_segment(self, segment):
        self.segments[segment.id] = segment

    ##  Creates transitions between segments in the level
    def connect(self):
        for segment_i in self.segments.values():
            for segment_j in self.segments.values():
                for tti in segment_i.transition_tiles:
                    for ttj in segment_j.transition_tiles:
                        if (tti[1] == ttj[1]):
                            if (segment_i != segment_j or tti[0] != ttj[0]):
                                segment_i.add_transition(tti[0],segment_j,ttj[0])
                                segment_j.add_transition(ttj[0],segment_i,tti[0])