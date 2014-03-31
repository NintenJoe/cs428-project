##  @file GraphTests.py
#   @author Nick Jeffrey
#   @date Spring 2014
#
#   Test File for the "Graph" Type
#
#   @TODO
#   - Cover at least 90% of code in Graph

import unittest
import src
from src.Graph import *
from src.IdleState import *
from src.Event import *

class GraphTest( unittest.TestCase ):

    ### Test Set Up/Tear Down ###

    def setUp( self ):
        self.G = Graph()

    def tearDown( self ):
        self.G = None

    ### Testing Functions ###

    def test_default_constructor( self ):
        self.assertEqual(self.G.nodes, {})
        self.assertEqual(self.G.edges, {})

    def test_adding_node( self ):
        idle = IdleState("1")
        self.G.add_node(idle)
        self.assertEqual(idle, self.G.nodes[idle.get_name()])
        self.assertEqual(self.G.edges[idle.get_name()], {})

    def test_adding_edge( self ):
        idle1 = IdleState("1")
        idle2 = IdleState("2")
        self.G.add_node(idle1)
        self.G.add_node(idle2)
        self.G.add_edge(idle1.get_name(), idle2.get_name(), Event(EventType.NOTIFY))
        self.assertEqual(idle2.get_name(), self.G.edges[idle1.get_name()][repr(Event(EventType.NOTIFY))])

    def test_transition( self ):
        idle1 = IdleState("1")
        idle2 = IdleState("2")
        self.G.add_node(idle1)
        self.G.add_node(idle2)
        self.G.add_edge(idle1.get_name(), idle2.get_name(), Event(EventType.NOTIFY))
        self.assertEqual(idle2, self.G.transition(idle1, Event(EventType.NOTIFY)))
        self.assertEqual(idle2, self.G.transition(idle2, Event(EventType.NOTIFY)))