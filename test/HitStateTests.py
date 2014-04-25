##  @file HitStateTests.py
#   @author Josh Halstead 
#   @date Spring 2014
#
#   Test File for the "HitState" Type

import unittest

import src
from src.HitState import *
from src.PhysicalState import *
from src.SimulationDelta import *
from src.CompositeHitbox import *

##  Container class for the test suite that tests the functionality of the
#   "HitState" type.
class HitStateTests(unittest.TestCase):
    ### Testing Constants ###

    ##  The name identifier for the test hit state used for testing.
    STATE_NAME = "test"

    ##  The time delta that will be used to test physical state updating.
    TIME_DELTA = 1.0

    ## The amount of damage a hit should inflict
    DAMAGE = 1

    ### Test Set Up/Tear Down ###

    def setUp(self):
        self._state = HitState(HitStateTests.STATE_NAME, HitStateTests.DAMAGE)

    def tearDown(self):
        self._state = None

    ### Testing Functions ###

    def test_constructor(self):
        self.assertEqual(self._state.get_name(), HitStateTests.STATE_NAME,
            "HitState constructor improperly initializes name of the state.")
        self.assertEqual(self._state.get_damage(), HitStateTests.DAMAGE,
            "HitState constuctor improperly initializes the damage of the state.")


    def test_step_simulation(self):
        first_change = self._state.simulate_step(HitStateTests.TIME_DELTA)
        second_change = self._state.simulate_step(HitStateTests.TIME_DELTA)

        self.assertTrue(first_change == second_change,
            "Simulating a step in a hit state results in different changes over time.")
        self.assertEqual(first_change,
            SimulationDelta(
                PhysicalState(
                    volume=CompositeHitbox(0.0, 0.0),
                    velocity=(0,0),
                    mass=0.0,
                    curr_health=0,
                    max_health=0)
            ),
            "The physical delta is incorrect.")


    def test_arrival_simulation(self):
        self.assertEqual(
            self._state.simulate_arrival(),
            SimulationDelta(
                PhysicalState(
                    volume=CompositeHitbox(),
                    velocity=(0.0, 0.0),
                    mass=0.0,
                    curr_health=-HitStateTests.DAMAGE,
                    max_health=0
                )
            ),
            "Simulating an arrival at a hit state results in an incorrect current health delta."
        )


    def test_departure_simulation(self):
        self.assertEqual(
            self._state.simulate_departure(),
            SimulationDelta(
                PhysicalState(
                    volume=CompositeHitbox(),
                    velocity=(0.0, 0.0),
                    mass=0.0,
                    curr_health=0,
                    max_health=0
                )
            ),
            "Simulating a departure from a hot state results in a non-empty physical delta."
        )

