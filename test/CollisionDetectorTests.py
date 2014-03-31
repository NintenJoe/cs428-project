##  @file CollisionDetectorTests.py
#   @author Joshua Halstead
#   @date Spring 2014
#
#   Test File for the "CollisionDetector" base class

import unittest

from src.CollisionDetector import *

class BasicCollisionDetector(CollisionDetector):
    initialized = ""

    def __init__(self):
        CollisionDetector.__init__(self)
        self.initialized = "initialized"
        pass

    def add_multiple(self, objs):
        CollisionDetector.add_multiple(self, objs)
        pass

    def add(self, obj):
        CollisionDetector.add(self, obj)
        pass

    def remove_multiple(self, objs):
        CollisionDetector.remove_multiple(self, objs)
        pass

    def remove(self, obj):
        CollisionDetector.remove(self, obj)
        pass

    def get_all_collisions(self):
        CollisionDetector.get_all_collisions(self)
        return []

    def get_all_objects(self):
        CollisionDetector.get_all_objects(self)
        return []

    def exists(self, entity):
        CollisionDetector.exists(self, entity)
        return True

    def clear(self):
        CollisionDetector.clear(self)
        pass


class CollisionDetectorTests(unittest.TestCase):
    def setUp(self):
        self.bcd = BasicCollisionDetector()

    def test_init(self):
        self.assertTrue(
                self.bcd.initialized == "initialized",
                "Collision detector improperly initialized."
        )

    def test_add_multiple(self):
        self.bcd.add_multiple([])

        self.assertTrue(
            self.bcd.get_all_objects() == [],
            "Object(s) is missing from the collision detector."
        )

    def test_add(self):
        self.bcd.add([])

        self.assertTrue(
            self.bcd.get_all_objects() == [],
            "Object is missing from the collision detector."
        )

    def test_remove_multiple(self):
        self.bcd.remove_multiple([])

        self.assertTrue(
            self.bcd.get_all_objects() == [],
            "Object(s) still exists in the collision detector."
        )

    def test_remove(self):
        self.bcd.remove([])

        self.assertTrue(
            self.bcd.get_all_objects() == [],
            "Object still exists in the collision detector."
        )

    def test_get_all_collisions(self):
        self.assertTrue(
            self.bcd.get_all_collisions() == [],
            "Some collisions are not being detected."
        )

    def test_get_all_objects(self):
        self.assertTrue(
            self.bcd.get_all_objects() == [],
            "Some objects are not being detected."
        )

    def tests_exists(self):
        self.assertTrue(
            self.bcd.exists([]),
            "Known object not detected."
        )

    def tests_clear(self):
        self.bcd.clear()

        self.assertTrue(
            self.bcd.get_all_objects() == [],
            "Collision detector still contains objects."
        )
