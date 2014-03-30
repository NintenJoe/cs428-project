##  @file HashableRect.py
#   @author Josh Halstead
#   @date Winter 2014
#
#   Source File for the "HashableRect" Type
#
#   @TODO
#   High Priority:
#   - Implement an equality operator to make testing for aggregate types
#     a bit more elegant.
#   Low Priority:
#   - 

import pygame

class HashableRect( pygame.Rect ):
    def __init__(self, x, y, w, h):
        pygame.Rect.__init__(self, x, y, w, h)

    def __hash__(self):
        return id(self)

