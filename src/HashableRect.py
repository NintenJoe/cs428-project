##  @file HashableRect.py
#   @author Josh Halstead
#   @date Winter 2014
#
#   An extension of pygame.Rect that creates a hashable rectangle.

import pygame


class HashableRect(pygame.Rect):
    def __init__(self, x, y, w, h):
        pygame.Rect.__init__(self, x, y, w, h)

    def __hash__(self):
        return id(self)
