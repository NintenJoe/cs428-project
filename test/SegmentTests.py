import unittest
import src
import pygame as pg

from src.World import *
from src.Level import *
from src.Segment import *
from src.Globals import *


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

    def testSegmentConstructor(self):
        level1 = self.world.levels['1']
        seg1 = level1.segments['1.1']
        seg2 = level1.segments['1.2']
        seg3 = level1.segments['1.3']

        self.assertTrue(seg1.width == 30, ("Segment width not set correctly."))
        self.assertTrue(seg2.width == 48, ("Segment width not set correctly."))
        self.assertTrue(seg3.width == 20, ("Segment width not set correctly."))

        self.assertTrue(seg1.height == 30, ("Segment height not set correctly."))
        self.assertTrue(seg2.height == 48, ("Segment height not set correctly."))
        self.assertTrue(seg3.height == 20, ("Segment height not set correctly."))

    def testSegmentGetSize(self):
        level1 = self.world.levels['1']
        seg1 = level1.segments['1.2']
        self.assertTrue(seg1.get_size() == (48,48), ("Segment returns incorrect size."))

    def testSegmentGetEntities(self):
        level1 = self.world.levels['1']
        seg1 = level1.segments['1.2']

        entities = seg1.get_entities()

        self.assertTrue(entities[0] == ((6,6),'player'), ("Entity was not loaded correctly."))
        self.assertTrue(entities[1] == ((7,32),'monster'), ("Entity was not loaded correctly."))
        self.assertTrue(entities[2] == ((22,5),'monster'), ("Entity was not loaded correctly."))
        self.assertTrue(entities[3] == ((22,25),'monster'), ("Entity was not loaded correctly."))
        self.assertTrue(entities[4] == ((31,42),'monster'), ("Entity was not loaded correctly."))
        self.assertTrue(entities[5] == ((38,24),'monster'), ("Entity was not loaded correctly."))