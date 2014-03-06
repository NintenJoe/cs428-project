##  @file Entity.py
#   @author Josh Halstead
#   @date Winter 2014
#
#   A makeshift game world object class for collision detection testing.

import pygame

class Entity:
    def __init__(self, bounding_volume):
        self.bounding_volume = bounding_volume
        self.rect = None

    def __repr__(self):
        return repr( self.bounding_volume )

    def __str__(self):
        return repr( self.bounding_volume )

    def set_bv(self, bounding_volume):
        self.bounding_volume = bounding_volume
