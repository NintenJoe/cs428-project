##  @file HashableRectTests.py
#   @author Joshua Halstead
#   @date Spring 2014
#
#   Test File for the HashableRect class

import unittest
import pygame

from src.HashableRect import *


class HashableRectTests(unittest.TestCase):
    ### Initialization/Cleanup functions ###

    def setUp(self):
        pass

    def tearDown(self):
        pass

    ### Testing Functions ###

    def test_init(self):
        rect = HashableRect(1, 2, 3, 4)
        self.assertEqual(rect.x, 1, "Invalid x-value detected.")
        self.assertEqual(rect.y, 2, "Invalid y-value detected.")
        self.assertEqual(rect.w, 3, "Invalid width detected.")
        self.assertEqual(rect.h, 4, "Invalid height detected.")

    def test_hash_nochange(self):
        rect = HashableRect(1, 2, 3, 4)
        self.assertEqual(hash(rect), id(rect), "Mismatching hash detected.")

    def test_hash_change(self):
        rect = HashableRect(1, 2, 3, 4)
        old_rect_hash = hash(rect)
        rect.w = -41
        rect.h = -144
        self.assertEqual(hash(rect), old_rect_hash,
                    "Hash changed after modifying rect.")

    def test_hash_eq_rects_diff_hashes(self):
        rect1 = HashableRect(1, 2, 3, 4)
        rect2 = HashableRect(1, 2, 3, 4)
        self.assertNotEqual(hash(rect1), hash(rect2), "Unexpected hash collision.")

