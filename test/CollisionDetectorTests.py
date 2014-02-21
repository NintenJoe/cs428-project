import unittest
import src
import pygame as p

from src.SpatialDictionary import *
from src.CollisionDetector import *
from src.Entity import *


# TODO: Constructor test
# TODO: Get all collisions test 
class CollisionDetectorTests(unittest.TestCase):

    def setUp(self):
        self.cell_size = 25
        self.width = 100
        self.height = 100

        self.entityA = Entity(p.Rect(4, 28, 15, 20))
        self.entityB = Entity(p.Rect(28, 10, 15, 20))
        self.entityC = Entity(p.Rect(65, 15, 20, 20))
        self.entityD = Entity(p.Rect(35, 35, 30, 45))
        self.entityE = Entity(p.Rect(60, 60, 10, 10))
        self.entityF = Entity(p.Rect(30, 76, 10, 10))
        self.entityG = Entity(p.Rect(80, 20, 15, 20))
        self.entityH = Entity(p.Rect(62, 68, 10, 10))
        self.entityI = Entity(p.Rect(75, 50, 20, 20))
        self.entityJ = Entity(p.Rect(80, 60, 10, 13))
        self.entities = [self.entityA, self.entityB, self.entityC,
                         self.entityD, self.entityE, self.entityF,
                         self.entityG]

        self.cd = CollisionDetector(self.entities, self.cell_size, self.width,
                                    self.height)
        pass

    def tearDown(self):
        pass

    def test_add_objs(self):
        entities2 = [self.entityH, self.entityI]
        self.cd.add_objs(entities2)
        #self.entities += entities2

        for entity in entities2:
            self.assertTrue(self.cd.exists(entity), ("One or more objects"
                            " were not added correctly."))


    def test_add_obj(self):
        self.cd.add_obj(self.entityJ)

        self.assertTrue(self.cd.exists(self.entityJ), ("A single object was"
                        " not added correctly."))

    def test_remove_objs(self):
        entities2 = [self.entityH, self.entityI]
        self.cd.remove_objs(entities2)

        for entity in self.entities:
            self.assertFalse(self.cd.exists(entity), ("One or more objects"
                            " were not removed correctly."))

    def test_remove_obj(self):
        self.cd.remove_obj(self.entityJ)
        self.assertFalse(self.cd.exists(self.entityJ), ("A singled object was not"
                         " removed correctly."))

    # TODO
    # {{B,D}, {D,F}, {D,E}, {D,H}, {E,H}, {C,G}, {I,J}}
    def test_get_all_collisions(self):
        pass
