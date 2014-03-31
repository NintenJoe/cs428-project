##  @file World.py
#   @author Andrew Exo
#   @date 2/20/2014
#
#   Source File for the "World" Type
#
#   @TODO
#   - Implement load method

import os.path
import glob
import string
import pygame as PG
from Level import Level
from Segment import Segment

##  This class is a high level container for all of the levels in the game.
#   For now its only job is to load and construct the levels.
class World():
    ### Constructors ###

    ##  
    #   
    def __init__(self):
        # This holds all of the levels and has the following form:
        # { "Level #"" => Level }
        self.levels = {}
        self.load()

    ### Methods ###

    ##  This method loads all of the segment files and creates segment objects
    #   for them. Then Levels are created using the connectivity information
    #   in each segment.
    #
    #   Segment files are stored in ../assets/data/segdata as .gif files
    def load(self):
        # get list of segment files
        seg_file_pattern = os.path.join('assets','data','segdata','*.gif')
        seg_files = glob.glob(seg_file_pattern)

        # load segments into pygame surfaces
        # creates Segments
        # groups segments into levels
        lvl_groups = {}
        for seg_file in seg_files:
            seg_id = string.split(os.path.basename(seg_file),'.')[1]
            surface = PG.image.load(seg_file)
            segment = Segment(seg_id,surface)

            filename = os.path.basename(seg_file)
            lvl_id = filename[:string.find(filename,'.')]
            if (lvl_id not in lvl_groups):
                lvl_groups[lvl_id] = [segment]
            else:
                lvl_groups[lvl_id].append(segment)

        # create Levels
        for lvl_id in lvl_groups.keys():
            segments = lvl_groups[lvl_id]
            level = Level(lvl_id)
            for segment in segments:
                level.add_segment(segment)
            level.connect()
            level.load_tiles()
            level.generate_images()
            self.levels[lvl_id] = level

