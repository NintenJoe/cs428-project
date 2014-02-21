##  @file Level.py
#   @author Andrew Exo
#   @date 2/20/2014
#
#   Source File for the "Level" Type
#
#   @TODO
#   - 

##  This class is a container for a connected Segment graph.
class Level():
    ### Constructors ###

    ##  Creates an empty Level
    #   
    def __init__(self):
        # Segment with entry point
        self.root = None
        # has the form { id => Segment }
        self.segments = {}

    ### Methods ###

    ##  Adds the segment to the level by adding it to the
    #   segment dictionary.
    def add_segment(self, segment):
        self.segments[segment.id] = segment
        # set root if segment has entry point
        if (segment.entry_point != None):
            self.root = segment