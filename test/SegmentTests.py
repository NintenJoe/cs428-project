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


    def testLevelLoadTiles(self):
        level1 = self.world.levels['1']
        tile1 = load_image("tiles/1.bmp")
        tile2 = load_image("tiles/2.bmp")
        tile3 = load_image("tiles/3.bmp")
        self.assertTrue( self.imagesEqual(tile3, level1.tiles[(0,0,0,255)]), ("Tile did not load correctly."))
        self.assertTrue( self.imagesEqual(tile1, level1.tiles[(255,255,255,255)]), ("Tile did not load correctly."))
        self.assertTrue( self.imagesEqual(tile1, level1.tiles[(255,0,0,255)]), ("Tile did not load correctly."))
        self.assertTrue( self.imagesEqual(tile2, level1.tiles[(100,100,100,255)]), ("Tile did not load correctly."))
        self.assertTrue( self.imagesEqual(tile2, level1.tiles[(200,200,200,255)]), ("Tile did not load correctly."))

    def testLevelGetImages(self):
        level1 = self.world.levels['1']
        segment1_image = load_image("test/1.bmp")
        segment2_image = load_image("test/2.bmp")
        segment3_image = load_image("test/3.bmp")
        self.assertTrue( self.imagesEqual(segment1_image, level1.images['1']), ("Segment 1.1 image is not correct."))
        self.assertTrue( self.imagesEqual(segment2_image, level1.images['2']), ("Segment 1.2 image is not correct."))
        self.assertTrue( self.imagesEqual(segment3_image, level1.images['3']), ("Segment 1.3 image is not correct."))

    def testSegmentConstructor(self):
        pass

    def testSegmentGetCollisionMap(self):
        pass

    def testSegmentTileTangible(self):
        pass

    # checks for equality by comparing every pixel
    def imagesEqual(self, surface1, surface2):
        if (surface1.get_rect() != surface2.get_rect()):
            return False
        for i in range(surface1.get_width()):
            for j in range(surface1.get_height()):
                if (surface1.get_at((i,j)) != surface2.get_at((i,j))):
                    return False
        return True