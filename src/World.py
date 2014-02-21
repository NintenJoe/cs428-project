##  @file World.py
#   @author Andrew Exo
#   @date 2/20/2014
#
#   Source File for the "World" Type
#
#   @TODO
#   - Implement load method

##  This class is a high level container for all of the levels in the game.
#   For now its only job is to load and construct the levels.
class World():
    ### Constructors ###

    ##  
    #   
    def __init__(self):
        # This holds all of the levels and has the following form:
        # { "Level Name" => Level }
        #
        # Level names will be the file name of the segment with an entry point
        # for that level.
        self.levels = {}
        self.load()

    ### Methods ###

    ##  This method loads all of the segment files and creates segment objects
    #   for them. Then Levels are created using the connectivity information
    #   in each segment.
    #
    #   Segment files are stored in ../assets/data/segdata as .gif files
    def load(self):
        pass

    ### Helper Functions ###

    ##  
    #   
    def _method( self,  ):
        pass
