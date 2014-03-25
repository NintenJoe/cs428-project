from Entity import *
from IdleState import *
from MoveState import *
import networkx as nx

class Player( Entity ):

    ## Setup state machine
    #   Build state machine and set up initial state
    #TODO: finish this
    #@override
    _setup_machine( self ):
        G=nx.DiGraph()
        G.add_node(MoveState("up", (0,-1)))
        G.add_node(MoveState("down", (0,1)))
        G.add_node(MoveState("left", (-1,0)))
        G.add_node(MoveState("right", (1,0)))
        idle = IdleState("idle")
        G.add_node(idle)
        edges = [("idle","move_up", event=EventType.KEYDOWN),("idle","move_left", event=EventType.KEYDOWN),("idle","move_right", event=EventType.KEYDOWN),
        ("idle","move_down", event=EventType.KEYDOWN),("move_up","idle", event=EventType.KEYUP),("move_left","idle", event=EventType.KEYUP),
        ("move_right","idle", event=EventType.KEYUP),("move_down","idle", event=EventType.KEYUP)]
        G.add_edges_from_source(edges)
        return StateMachine(G, idle)

