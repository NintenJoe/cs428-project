##  @file SpatialDictionaryTests.py
#   @author Joshua Halstead
#   @date Spring 2014
#
#   Test File for the "SpatialDictionary" collision strategy

import unittest

from src.HashableRect import *
from src.SpatialDictionary import *


class SpatialDictionaryTests(unittest.TestCase):
    ### Test Set Up/Tear Down ###

    def setUp(self):
        self.cell_size = 25
        self.width = 100
        self.height = 100

        self.entityA = HashableRect(4, 28, 15, 20)
        self.entityB = HashableRect(28, 10, 15, 20)
        self.entityC = HashableRect(65, 15, 20, 20)
        self.entityD = HashableRect(35, 35, 30, 45)
        self.entityE = HashableRect(60, 60, 10, 10)
        self.entityF = HashableRect(30, 76, 10, 10)
        self.entityG = HashableRect(80, 20, 15, 20)
        self.entityH = HashableRect(62, 68, 10, 10)
        self.entityI = HashableRect(75, 50, 20, 20)
        self.entityJ = HashableRect(80, 60, 10, 13)
        self.entityK = HashableRect(78, 55, 15, 15)
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

    def test_repr_empty(self):
        temp_dict = SpatialDictionary(self.cell_size, self.width, self.height)
        self.assertTrue(
            repr(temp_dict) == "{}",
            "Invalid object representation."
        )

    def test_repr_nonempty(self):
        temp_dict = SpatialDictionary(self.cell_size, self.width, self.height)
        temp_dict.add(self.entityA)

        self.assertTrue(
            repr(temp_dict) == "{4:Set([<rect(4, 28, 15, 20)>])}",
            "Invalid object representation."
        )

    def test_str_empty(self):
        temp_dict = SpatialDictionary(self.cell_size, self.width, self.height)
        self.assertTrue(
            str(temp_dict) == "{}",
            "Invalid stribg representation."
        )

    def test_str_nonempty(self):
        temp_dict = SpatialDictionary(self.cell_size, self.width, self.height)
        temp_dict.add(self.entityA)

        self.assertTrue(
            str(temp_dict) == "{4:Set([<rect(4, 28, 15, 20)>])}",
            "Invalid stribg representation."
        )

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
        self.assertEqual(self.dict_.size(), 0,
                         "Phantom entities exist after clearing empty list.")

        # Restore the deleted objects
        self.dict_.add_multiple(self.all_entities)

    def test_clear_nonempty(self):
        self.dict_.add_multiple(self.all_entities)
        self.dict_.clear()

        self.assertEqual(self.dict_.size(), 0,
                         "Entities still exists after clearing nonempty list.")

    def test_exists_true(self):
        self.dict_.add(self.entityJ)
        self.assertTrue(self.dict_.exists(self.entityJ),
                        "Entity does not exist after adding it.")

    def test_exists_false(self):
        self.dict_.remove(self.entityJ)
        self.assertFalse(self.dict_.exists(self.entityJ),
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
        expected_collision = [frozenset([self.entityC, self.entityG])]
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

    def test_get_all_collisions_entity_not_in_orig_cell(self):
        entities = [self.entityE, self.entityH]
        self.dict_.remove_multiple(self.all_entities)
        self.dict_.add_multiple(entities)

        # Move the entities to a new cell. (Ugly)
        e_x = e_y = 5
        e_x, self.entityE.x = self.entityE.x, e_x
        e_y, self.entityE.y = self.entityE.y, e_y

        h_x = h_y = 1
        h_x, self.entityH.x = self.entityH.x, h_x
        h_y, self.entityH.y = self.entityH.y, h_y

        # We cannot use the _test_get_all_collisions helper function because
        # it effectively manually updates the spatial dictionary
        expected_collisions = [frozenset([self.entityE, self.entityH])]
        stale_collisions = self.dict_.get_all_collisions()
        self.assertTrue(set(stale_collisions) != set(expected_collisions),
                        "Expected the list of collisions to no match.")

        self.dict_.update()
        actual_collisions = self.dict_.get_all_collisions()
        self.assertTrue(set(actual_collisions) == set(expected_collisions),
                        "Incorrect set of collisions detected.")

        self.entityE.x = e_x
        self.entityE.y = e_y
        self.entityH.x = h_x
        self.entityH.y = h_y

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
