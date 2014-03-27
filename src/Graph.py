##  @file Graph.py
#   @author Nick Jeffrey
#   @date Spring 2014
#
#   Source File for the "Graph" Type
#
#   @TODO
#   - Add functions for checking edges and what nodes exists
#   - Write tests
#   - Replace networkx graphs in the entire codebase, especially StateMachine and StateMachineTests

from State import *

class Graph():

    def __init__(self):
        self.nodes = {}
        self.edges = {}

    def add_node(self, new_node):
        self.nodes[new_node.get_name()] = new_node
        self.edges[new_node.get_name()] = {}

    def add_edge(self, start_node, end_node, event):
        self.edges[start_node][event] = end_node

    def add_edges_from_source(self, edges):
        for (x,y,z) in edges:
            self.add_edge(x,y,z)