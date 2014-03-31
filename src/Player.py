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
from Transition import *

##  Represents the Player and the actions that the Player character can execute
#   For now, this includes only walking around
class Player( Entity ):

    ## Setup state machine
    #   Build state machine and set up initial state
    #   TODO: Use actual key value and not just placeholder
    #   @override
    def _produce_machine( self ):
        states = [IdleState("1"), MoveState("up", (0,-1)), MoveState("down", (0,1)), MoveState("left", (-1,0)), MoveState("right", (1,0))]
        edges = [Transition("idle_1","move_up", "keydown,key:up"),
        Transition("idle_1","move_left", "keydown,key:left"),
        Transition("idle_1","move_right", "keydown,key:right"),
        Transition("idle_1","move_down", "keydown,key:down"),
        Transition("move_up","idle_1", "keyup,key:up"),
        Transition("move_left","idle_1", "keyup,key:left"),
        Transition("move_right","idle_1", "keyup,key:right"),
        Transition("move_down","idle_1", "keyup,key:down")]
        return StateMachine(states, edges, "idle_1")

    def _produce_physical( self ):
        return PhysicalState(PG.Rect(0, 0, 20, 20), (0,0), 1.0)