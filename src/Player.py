##  @file Player.py
#   @author Nick Jeffrey
#   @date Spring 2014
#
#   Source File for the "Player" Type
#
#   @TODO
#   - Use actual key input and not just a placeholder

from Entity import *
from IdleState import *
from MoveState import *
from StateMachine import *
from Graph import *
from Event import *

##  Represents the Player and the actions that the Player character can execute
#   For now, this includes only walking around
class Player( Entity ):

    ## Setup state machine
    #   Build state machine and set up initial state
    #   TODO: Use actual key value and not just placeholder
    #   @override
    def _setup_machine( self ):
        G=Graph()
        G.add_node(MoveState("up", (0,-1)))
        G.add_node(MoveState("down", (0,1)))
        G.add_node(MoveState("left", (-1,0)))
        G.add_node(MoveState("right", (1,0)))
        idle = IdleState("1")
        G.add_node(idle)
        edges = [("idle_1","move_up", Event(EventType.KEYDOWN, {"key" : "up"})),("idle_1","move_left", Event(EventType.KEYDOWN, {"key" : "left"})),("idle_1","move_right", Event(EventType.KEYDOWN, {"key" : "right"})),
        ("idle_1","move_down", Event(EventType.KEYDOWN, {"key" : "down"})),("move_up","idle_1", Event(EventType.KEYUP, {"key" : "up"})),("move_left","idle_1", Event(EventType.KEYUP, {"key" : "left"})),
        ("move_right","idle_1", Event(EventType.KEYUP, {"key" : "right"})),("move_down","idle_1", Event(EventType.KEYUP, {"key" : "down"}))]
        G.add_edges_from_source(edges)
        return StateMachine(G, idle)