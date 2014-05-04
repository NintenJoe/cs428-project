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

    # TODO: Re-implement this properly.
    def test_get_tilemap(self):
        pass

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

    def test_get_camera(self):
        #TODO
        pass

#    def test_segment_transition(self):
#        pass

#        entities = self._world.get_entities()
#        player = None

#        for entity in entities:
#            if entity.get_name() == "player":
#                player = entity
#        self.assertTrue(player, "Player not found.")

#        transitions = self._world._segment.transitions
#        print "orig_seg", self._world._segment
#        print "transitions", transitions
#        self.assertTrue(transitions, "Transitions not found.")

#        coords,new_seg = transitions.popitem()
#        print "coords",coords
#        print "new_seg",new_seg[0]
#        player_chitbox = player.get_physical_state().get_volume()

#        print "player before",str(player.get_physical_state().get_volume()._container_box)
#        coords = (Globals.TILE_DIMS[0] * coords[0], Globals.TILE_DIMS[1] * coords[1])
#        print "coords_x",coords[0]
#        print "coords_y",coords[1]
#        player_chitbox.place_at(coords[0], coords[1])

#        print "player after",str(player.get_physical_state().get_volume()._container_box)
#        self._world.update(0.1)
#        print "curr_seg",self._world._segment
#        self.assertTrue (new_seg[0] == self._world._segment,
#                "Game world didn't transition to new segment.")
