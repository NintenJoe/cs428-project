import unittest
import src
import pygame as pg

from src.World import *
from src.Level import *
from src.Segment import *


class SegmentTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pg.init()
        pg.display.set_mode((640,480))

    @classmethod
    def tearDownClass(self):
        pg.quit()

    def setUp(self):
        self.world = World()

    def tearDown(self):
        pass

    def testWorldLoad(self):
        self.assertTrue('1' in self.world.levels, ("Level 1 did not load properly."))

    def testLevelConnect(self):
        level1 = self.world.levels['1']
        segments = level1.segments.values()
        for segment in segments:
            for trans in segment.transitions.items():
                trans_back = trans[1][0].transitions[trans[1][1]]
                self.assertTrue(segment == trans_back[0] and trans[0] == trans_back[1], ("Transition is not bidirectional."))
                self.assertTrue(segment != trans[1][0] or trans[0] != trans[1][1], ("Transition is a loop."))


    def testLevelLoadTiles(self):
        pass

    def testLevelGetImages(self):
        pass

    def testSegmentConstructor(self):
        pass

    def testSegmentGetCollisionMap(self):
        pass

    def testSegmentTileTangible(self):
        pass