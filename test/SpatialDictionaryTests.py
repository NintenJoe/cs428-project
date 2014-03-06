<<<<<<< Updated upstream
=======
##  @file SpatialDictionaryTests.py
#   @author Joshua Halstead
#   @date Spring 2014
#
#   Test File for the "SpatialDictionary" Type
#
# TODO: Add __repr__ test

>>>>>>> Stashed changes
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
        self.entityH = Entity(p.Rect(62, 68, 10, 10))
        self.entityI = Entity(p.Rect(75, 50, 20, 20))
        self.entityJ = Entity(p.Rect(80, 60, 10, 13))
        self.some_entities = [self.entityA, self.entityB, self.entityC,
                              self.entityD, self.entityE, self.entityF,
                              self.entityG, self.entityH, self.entityI]
        self.all_entities = self.some_entities + [self.entityJ]
        self.sp_dict = SpatialDictionary(self.cell_size, self.width,
                                         self.height)
        pass

    def tearDown(self):
        self.sp_dict.clear()
        pass

    ### Testing Functions ###

<<<<<<< Updated upstream
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
=======
    def test_add_one_object(self):
        self.sp_dict.add_obj(self.entityJ)
        self.assertTrue(self.sp_dict.exists(self.entityJ),
                        "A single object was not added correctly.")

    def test_add_multiple_objects(self):
        self.sp_dict.add_objs(self.all_entities)
        for entity in self.all_entities:
            self.assertTrue(self.sp_dict.exists(entity),
                            "One or more objects were not added correctly.")

    def test_remove_one_object(self):
        self.sp_dict.remove_obj(self.entityJ)
        self.assertFalse(self.sp_dict.exists(self.entityJ),
                         "A single object was not removed correctly.")

        # Restore dictionary
        self.sp_dict.add_obj(self.entityJ)

    def test_remove_multiple_objects(self):
        self.sp_dict.remove_objs(self.all_entities)
        for entity in self.all_entities:
            self.assertFalse(self.sp_dict.exists(entity),
                             "One or more objects were not removed correctly.")

        # Restore dictionary
        self.sp_dict.add_objs(self.all_entities)
>>>>>>> Stashed changes

    # Nearby objects to A => {}
    def test_get_nearby_objs_none(self):
<<<<<<< Updated upstream
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
=======
        self.sp_dict.add_objs(self.all_entities)
        correct_nearby_objs = []

        self._test_get_nearby_objs(self.entityA, set([]))

    # Nearby objects to F => D
    def test_get_nearby_objs_one(self):
        self.sp_dict.add_objs(self.all_entities)
        correct_nearby_objs = [self.entityD]

        self._test_get_nearby_objs(self.entityF, correct_nearby_objs)

    # Nearby objects to D => B, C, E, F, and H
    def test_get_nearby_objs_multi(self):
        self.sp_dict.add_objs(self.all_entities)
        correct_nearby_objs = [self.entityB, self.entityC, self.entityE,
                               self.entityF, self.entityH]

        self._test_get_nearby_objs(self.entityD, correct_nearby_objs)

    def _test_get_nearby_objs(self, obj, correct_nearby_objs):
        nearby_objs = self.sp_dict.get_nearby_objs(obj)
        self.assertEqual(len(nearby_objs), len(correct_nearby_objs),
                         "Incorrect number of nearby objects reported.")
        self.assertTrue(set(nearby_objs) == set(correct_nearby_objs),
                        "Reported nearby objects list is incomplete.")
>>>>>>> Stashed changes
