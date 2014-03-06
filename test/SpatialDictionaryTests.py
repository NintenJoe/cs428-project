##  @file SpatialDictionaryTests.py
#   @author Joshua Halstead
#   @date Spring 2014
#
#   Test File for the "SpatialDictionary" collision strategy

import unittest

from src.Entity import *
from src.HashableRect import *
from src.SpatialDictionary import *
from src.CollisionDetector import *


class SpatialDictionaryTests(unittest.TestCase):
    ### Test Set Up/Tear Down ###

    def setUp(self):
        self.cell_size = 25
        self.width = 100
        self.height = 100

        self.entityA = Entity(HashableRect(4, 28, 15, 20))
        self.entityB = Entity(HashableRect(28, 10, 15, 20))
        self.entityC = Entity(HashableRect(65, 15, 20, 20))
        self.entityD = Entity(HashableRect(35, 35, 30, 45))
        self.entityE = Entity(HashableRect(60, 60, 10, 10))
        self.entityF = Entity(HashableRect(30, 76, 10, 10))
        self.entityG = Entity(HashableRect(80, 20, 15, 20))
        self.entityH = Entity(HashableRect(62, 68, 10, 10))
        self.entityI = Entity(HashableRect(75, 50, 20, 20))
        self.entityJ = Entity(HashableRect(80, 60, 10, 13))
        self.entityK = Entity(HashableRect(78, 55, 15, 15))
        self.some_entities = [self.entityA, self.entityB, self.entityC,
                              self.entityD, self.entityE, self.entityF,
                              self.entityG, self.entityH, self.entityI,
                              self.entityK]
        self.all_entities = self.some_entities + [self.entityJ]

        self.dict_ = SpatialDictionary(self.cell_size, self.width, self.height)
        pass

    def tearDown(self):
        self.dict_.clear()
        pass

    ### Testing Functions ###

    def test_add_one_object(self):
        self.dict_.add(self.entityJ)
        self.assertTrue(self.dict_.exists(self.entityJ),
                        "A single object was not added correctly.")

    def test_add_multiple_objects(self):
        self.dict_.add_multiple(self.some_entities)
        for entity in self.some_entities:
            self.assertTrue(self.dict_.exists(entity),
                            "Some objects were not added correctly.")

    def test_remove_one_object(self):
        self.dict_.add(self.entityJ)
        self.dict_.remove(self.entityJ)
        self.assertFalse(self.dict_.exists(self.entityJ),
                         "A single object was not removed correctly.")

        # Restore the deleted object
        self.dict_.add(self.entityJ)

    def test_remove_multiple_objects(self):
        self.dict_.add_multiple(self.some_entities)
        self.dict_.remove_multiple(self.some_entities)
        for entity in self.all_entities:
            self.assertFalse(self.dict_.exists(entity),
                             "Some objects were not removed.")

        # Restore the deleted objects
        self.dict_.add_multiple(self.some_entities)

    def test_clear_empty(self):
        self.dict_.remove_multiple(self.all_entities)
        self.dict_.clear()
        self.assertEqual(len(self.dict_), 0,
                         "Phantom entities exist after clearing empty list.")

        # Restore the deleted objects
        self.dict_.add_multiple(self.all_entities)

    def test_clear_nonempty(self):
        self.dict_.add_multiple(self.all_entities)
        self.dict_.clear()

        self.assertEqual(len(self.dict_), 0,
                         "Entities still exists after clearing nonempty list.")

    def test_exists_true(self):
        self.dict_.add(self.entityJ)
        assertTrue(self.dict_.exists(self.entityJ),
                   "Entity does not exist after adding it.")

    def test_exists_false(self):
        self.dict_.remove(self.entityJ)
        assertFalse(self.dict_.exists(self.entityJ),
                    "Entity still exists after removing it.")

        # Restore the deleted object
        self.dict_.add(self.entityJ)

    def test_size_empty(self):
        self.dict_.clear()
        self.assertEqual(self.dict_.size(), 0,
                         "Size mismatch with empty dictionary.")

    def test_size_nonempty(self):
        self.dict_.add_multiple(self.all_entities)
        self.assertEqual(self.dict_.size(), len(self.all_entities),
                         "Size mismatch with nonempty dictionary.")

    def test_get_all_collisions_none(self):
        self._test_get_all_collisions([], [])

    def test_get_all_collisions_one_inside_cell(self):
        entities = [self.entityI, self.entityJ]
        expected_collision = [frozenset([self.entityI, self.entityJ])]
        self._test_get_all_collisions(entities, expected_collision)

    def test_get_all_collisions_one_across_cells(self):
        entities = [self.entityC, self.entityG]
        expect_collision = [frozenset([self.entityC, self.entityG])]
        self._test_get_all_collisions(entities, expected_collision)

    def test_get_all_collisions_multiple_inside_cell(self):
        entities = [self.entityI, self.entityJ, self.entityK]
        expected_collisions = [frozenset([self.entityI, self.entityJ]),
                               frozenset([self.entityI, self.entityK]),
                               frozenset([self.entityJ, self.entityK])]
        self._test_get_all_collisions(entities, expected_collisions)

    def test_get_all_collisions_multiple_across_cells(self):
        entities = [self.entityB, self.entityC, self.entityD,
                    self.entityE, self.entityF, self.entityH]
        expected_collisions = [frozenset([self.entityD, self.entityF]),
                               frozenset([self.entityD, self.entityE]),
                               frozenset([self.entityD, self.entityH]),
                               frozenset([self.entityE, self.entityH])]
        self._test_get_all_collisions(entities, expected_collisions)

    def test_get_all_collisions_universal(self):
        expected_collisions = [frozenset([self.entityC, self.entityG]),
                               frozenset([self.entityD, self.entityF]),
                               frozenset([self.entityD, self.entityE]),
                               frozenset([self.entityD, self.entityH]),
                               frozenset([self.entityE, self.entityH]),
                               frozenset([self.entityI, self.entityJ]),
                               frozenset([self.entityI, self.entityK]),
                               frozenset([self.entityJ, self.entityK])]
        self._test_get_all_collisions(self.all_entities, expected_collisions)

    def test_get_all_objects_empty(self):
        self.dict_.remove_multiple(self.all_entities)
        entities = self.dict_.get_all_objects()
        self.assertEqual(entities, [],
                         "Unknown objects present.")

    def test_get_all_objects_nonempty(self):
        self.dict_.remove_multiple(self.all_entities)
        self.dict_.add(self.entityA)
        self.dict_.add(self.entityB)
        entities = self.dict_.get_all_objects()
        self.assertEqual(entities, [self.entityA, self.entityB],
                         "Unknown objects present.")

    # Private helper functions

    def _test_get_all_collisions(self, entities, expected_collisions):
        self.dict_.remove_multiple(self.all_entities)
        self.dict_.add_multiple(entities)

        collisions = self.dict_.get_all_collisions()
        self.assertTrue(set(collisions) == set(expected_collisions),
                        "Incorrect list of collisions detected.")

        # Restore the deleted objects
        self.dict_.add_multiple(self.all_entities)
