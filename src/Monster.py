##  @file Monster.py
#   @author Nick Jeffrey
#   @date Spring 2014
#
#   Source File for the "Monster" Type
#
#   @TODO
#   - Use actual key input and not just a placeholder

from Entity import *
from IdleState import *
from MoveState import *
from StateMachine import *
from Graph import *
from Event import *

##  Represents a single Monster and the actions that the Monster can execute
#   For now, this includes only walking around
class Monster( Entity ):

    ## Setup state machine
    #   Build state machine and set up initial state
    #   TODO: Implement timeouts as an optional parameter to Notify
    #   @override
    def _setup_machine( self ):
        G=Graph()
        G.add_node(MoveState("up", (0,-1)))
        G.add_node(MoveState("down", (0,1)))
        G.add_node(MoveState("left", (-1,0)))
        G.add_node(MoveState("right", (1,0)))
        idle = IdleState("1")
        G.add_node(idle)
        G.add_node(IdleState("2"))
        G.add_node(IdleState("3"))
        G.add_node(IdleState("4"))
        timeout = 20
        self.timeout = timeout
        edges = [("idle_1","move_up", Event(EventType.NOTIFY, {"timeout" : timeout})),
        ("idle_2","move_left", Event(EventType.NOTIFY, {"timeout" : timeout})),
        ("idle_4","move_right", Event(EventType.NOTIFY, {"timeout" : timeout})),
        ("idle_3","move_down", Event(EventType.NOTIFY, {"timeout" : timeout})),
        ("move_up","idle_2", Event(EventType.NOTIFY, {"timeout" : timeout})),
        ("move_left","idle_3", Event(EventType.NOTIFY, {"timeout" : timeout})),
        ("move_right","idle_1", Event(EventType.NOTIFY, {"timeout" : timeout})),
        ("move_down","idle_4", Event(EventType.NOTIFY, {"timeout" : timeout}))]
        G.add_edges_from_source(edges)
        return StateMachine(G, idle)