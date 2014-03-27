##  @file SimulationDeltaTests.py
#   @author Joseph Ciurej
#   @date Spring 2014
#
#   Test File for the "SimulationDelta" Type
#
#   @TODO
#   - Update the tests for this type as more fields are added to the 
#     "SimulationDelta" type.

import unittest
import src
import pygame as PG

from src.PhysicalState import *
from src.Event import *
from src.SimulationDelta import *

##  Container class for the test suite that tests the functionality of the
#   "SimulationDelta" type.
class SimulationDeltaTests( unittest.TestCase ):
    ### Testing Constants ###

    ##  The physical state delta that will be assigned to the test delta.
    PHYSICAL_DELTA = PhysicalState( PG.Rect(1, 2, 3, 4), (4, 5), 6.0 )

    ##  The listing of events that will be assigned to the test delta.
    EVENT_LIST = [ Event( EventType.NOTIFY, { "one": 1 } ),
        Event( EventType.NOTIFY, { "two": 2 } ) ]

    ### Test Set Up/Tear Down ###

    def setUp( self ):
        self._delta = SimulationDelta( SimulationDeltaTests.PHYSICAL_DELTA,
            SimulationDeltaTests.EVENT_LIST )

    def tearDown( self ):
        self._delta = None

    ### Testing Functions ###

    def test_default_constructor_initialization( self ):
        default_delta = SimulationDelta()

        self.assertEqual( default_delta.get_entity_delta(), PhysicalState(),
            "Incorrect entity physical state delta on default initialization." )
        self.assertEqual( default_delta.get_events(), [],
            "Incorrect new event listing on default initialization." )


    def test_value_constructor_initialization( self ):
        self.assertEqual( self._delta.get_entity_delta(),
            SimulationDeltaTests.PHYSICAL_DELTA,
            "Incorrect entity physical state delta on explicit initialization." )
        self.assertEqual( self._delta.get_events(),
            SimulationDeltaTests.EVENT_LIST,
            "Incorrect new event listing on explicit initialization." )


    def test_value_constructor_independence( self ):
        self._delta._entity_delta.add_delta( SimulationDeltaTests.PHYSICAL_DELTA )
        self._delta._events.append( SimulationDeltaTests.EVENT_LIST[0] )
        self.assertNotEqual( self._delta.get_entity_delta(),
            SimulationDeltaTests.PHYSICAL_DELTA,
            "Value constructor doesn't deep copy the parameter physical state." )
        self.assertNotEqual( self._delta.get_events(),
            SimulationDeltaTests.EVENT_LIST,
            "Value construcor doesn't deepy copy the parameter event listing." )


    def test_add_simple( self ):
        simple_delta = SimulationDelta()
        aggregate_delta = self._delta + simple_delta

        self.assertEqual( aggregate_delta.get_entity_delta(),
            SimulationDeltaTests.PHYSICAL_DELTA,
            "Adding a zero delta to a non-zero delta produces physical state changes." )
        self.assertEqual( aggregate_delta.get_events(),
            SimulationDeltaTests.EVENT_LIST,
            "Adding a zero delta to a non-zero delta produces event listing changes." )


    def test_add_complex( self ):
        aggregate_delta = self._delta + self._delta

        soln_entity_delta = PhysicalState()
        soln_entity_delta.add_delta( self._delta.get_entity_delta() )
        soln_entity_delta.add_delta( self._delta.get_entity_delta() )

        soln_event_list = []
        soln_event_list.extend( self._delta.get_events() )
        soln_event_list.extend( self._delta.get_events() )

        self.assertEqual( aggregate_delta.get_entity_delta(), soln_entity_delta,
            "Adding two non-zero deltas produces incorrect physical state changes." )
        self.assertEqual( aggregate_delta.get_events(), soln_event_list,
            "Adding two non-zero deltas produces incorrect event listing changes." )

