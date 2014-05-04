##  @file GameWorldTests.py
#   @author Josh Halstead, Joseph Ciurej
#   @date Spring 2014
#
#   Test File for the "GameWorld" Type
#
#   @TODO
#   - Write the implementation in this file!
#   - Make all these ugly things less ugly and more robust

import pygame as pg
import unittest
import src

from src.GameWorld import *
from src.Event import *
from src.Globals import *

##  Container class for the test suite that tests the functionality of the
#   "GameWorld" type.
class GameWorldTests(unittest.TestCase):
    ### Test Set Up/Tear Down ###

    def setUp(self):
        self._world = GameWorld()

    def tearDown(self):
        self._world = None

    ### Testing Functions ###

    def test_init(self):
        try:
            self._world
        except NameError:
            self.assertTrue(False, "Game world didn't define a world.")

        try:
            self._world._collision_detector
        except NameError:
            self.assertTrue(
                False,
                "Game world didn't define a collision detector."
            )

        try:
            self._world._camera
        except NameError:
            self.assertTrue(False, "Game world didn't define a camera.")

        try:
            self._world._entities
        except NameError:
            self.assertTrue(False, "Game world didn't define entities.")

    def test_update_no_events(self):
        pre_entities = self._world.get_entities()
        self._world.update(1)
        post_entities = self._world.get_entities()

        self.assertTrue(pre_entities == post_entities)
        pass

    def test_notify_of(self):
        player = self._world._player_entity
        pre_player_status = player.get_status()
        event = Event(EventType.KEYDOWN, {"key": MOVE_UP})
        self._world.notify_of(event, [player])

        player.update(0.0001)
        post_player_status = player.get_status()

        # TODO: Resolve this here.
        self.assertTrue(
            "move_up" in post_player_status,
            "Player didn't change states."
        )

    def test_get_entities(self):
        entities = self._world.get_entities()
        self.assertTrue(len(entities) > 0, "Game world didn't define entities.")
        pass

    def test_get_viewport(self):
        curr_view = self._world.get_viewport()
        soln_view = self._world._camera.get_viewport()

        self.assertTrue(curr_view == soln_view,
                "Game world does not define the correct viewport.")

        self._world.update(0.1)
        self.assertTrue(curr_view == soln_view,
                "Game world does not update the viewport correctly.")

    def test_entity_death(self):
        entities = self._world.get_entities()
        entity = entities[0]
        phys_state = entity.get_physical_state()

        phys_state._curr_health = 0
        self._world.update(0.1)

        self.assertTrue(entity not in entities,
                "Game world did not delete entity.")

