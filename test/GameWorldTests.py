##  @file GameWorldTests.py
#   @author Josh Halstead, Joseph Ciurej
#   @date Spring 2014
#
#   Test File for the "GameWorld" Type
#
#   @TODO
#   - Write the implementation in this file!

import pygame as pg
import unittest
import src
from src.GameWorld import *

##  Container class for the test suite that tests the functionality of the
#   "GameWorld" type.
class GameWorldTests( unittest.TestCase ):
    ### Test Set Up/Tear Down ###

    @classmethod
    def setUpClass(cls):
        pg.init()
        pg.display.set_mode((640,480))

    @classmethod
    def tearDownClass(self):
        pg.quit()

    def setUp( self ):
        self._world = GameWorld()

    def tearDown( self ):
        self._world = None

    ### Testing Functions ###

    def test_test( self ):
        tilemap = self._world.get_tilemap()

        string = ""
        for x in range( len(tilemap) ):
            for y in range( len(tilemap) ):
                string += tilemap[x][y] + " "
            string += "\n"
        print string

