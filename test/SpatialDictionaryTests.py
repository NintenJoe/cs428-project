import unittest
import src
import pygame as p

from src.SpatialDictionary import *
from src.Entity import *


##	Test case containment class for all of the test cases used in testing the
#	library functions of the 'gamelib' library.
class SpatialDictionaryTests(unittest.TestCase):
    ### Test Set Up/Tear Down ###

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
        self.entities = [self.entityB, self.entityC, self.entityD,
                         self.entityE, self.entityF, self.entityG]

        self.sp_dict = SpatialDictionary(self.cell_size, self.width,
                                         self.height)
        pass

    def tearDown(self):
        self.sp_dict.clear()
        pass

    ### Testing Functions ###

    def test_add_single_object(self):
        self.sp_dict.add_obj(self.entityA)
        self.assertTrue(self.sp_dict.exists(self.entityA), ("A single object was"
                        " not added correctly."))

    def test_add_multiple_objects(self):
        self.sp_dict.add_objs(self.entities)
        for entity in self.entities:
            self.assertTrue(self.sp_dict.exists(entity), ("One or more objects"
                           " were not added correctly."))

    def test_remove_single_object(self):
        self.sp_dict.remove_obj(self.entityA)
        self.assertFalse(self.sp_dict.exists(self.entityA), ("A single object was"
                                                        " not removed correctly."))
        self.sp_dict.add_obj(self.entityA)

    def test_remove_multiple_objects(self):
        self.sp_dict.remove_objs(self.entities)
        for entity in self.entities:
            self.assertFalse(self.sp_dict.exists(entity), ("One or more"
                           " objects were not removed correctly."))
        self.sp_dict.add_objs(self.entities)

    def test_get_nearby_objs_none(self):
        nearby_objs = self.sp_dict.get_nearby_objs(self.entityA)
        self.assertEqual(len(nearby_objs), 0, ("incorrect number of nearby"
                        " objects repoted."))

#    def test_get_nearby_objs_one(self):
#        nearby_objs = self.sp_dict.get_nearby_objs(self.entityF)
#        self.assertEqual(len(nearby_objs), 1, ("Incorrect number of nearby"
#                        " objects reported."))

#    def test_get_nearby_objs_multi(self):
#        nearby_objs = self.sp_dict.get_nearby_objs(self.entityD)
#        self.assertEqual(len(nearby_objs), 3, ("Incorrect number of nearby"
#                        " objects reported."))
