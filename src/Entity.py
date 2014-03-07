##  @file Entity.py
#   @author Josh Halstead
#   @date Winter 2014
#
#   A makeshift game world object class for collision detection testing.

import pygame

from src.HashableRect import *


class Entity:
    def __init__(self, bounding_volume):
        self.bounding_volume = bounding_volume
        self.rect = None

    def __repr__(self):
        return repr(self.bounding_volume)

    def __str__(self):
        return repr(self.bounding_volume)

    def __eq__(self, other):
        return (self.bounding_volume.x == other.bounding_volume.x and
                self.bounding_volume.y == other.bounding_volume.y and
                self.bounding_volume.w == other.bounding_volume.w and
                self.bounding_volume.h == other.bounding_volume.h)

    def set_bv(self, bounding_volume):
        self.bounding_volume = bounding_volume

    def get_bv(self):
        return self.bounding_volume
