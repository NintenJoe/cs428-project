## @file EntityTests.py
#  @authore Josh Halstead
#  @date Winter 2014
#
#  Test file for the Entity class.

import unittest
import pygame

from src.HashableRect import *
from src.Entity import *


class EntityTests(unittest.TestCase):
    ### Initialization/Cleanup ###

    def setUp(self):
        self.e = Entity(HashableRect(1, 2, 3, 4))
        pass

    def tearDown(self):
        pass

    ### Testing Functions ###

    def test_init(self):
        self.assertEqual(self.e, Entity(HashableRect(1, 2, 3, 4)))

    def test_repr(self):
        self.assertEqual(repr(self.e), repr(Entity(HashableRect(1, 2, 3, 4))))

    def test_eq(self):
        self.assertEqual(self.e, Entity(HashableRect(1, 2, 3, 4)))

    def test_str(self):
        self.assertEqual(str(self.e), str(Entity(HashableRect(1, 2, 3, 4))))

    def test_set_bv(self):
        self.e.set_bv(HashableRect(4, 3, 2, 1))
        self.assertEqual(self.e.get_bv(), HashableRect(4, 3, 2, 1))
        self.e.set_bv(HashableRect(1, 2, 3, 4))

    def test_get_bv(self):
        self.assertEqual(self.e.get_bv(), HashableRect(1, 2, 3, 4))
