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
    def _produce_machine( self ):
        timeout = 100
        self.timeout = timeout
        states = [
            IdleState("1", timeout),
            IdleState("2", timeout),
            IdleState("3", timeout),
            IdleState("4", timeout),
            MoveState("up", (0,-1), timeout),
            MoveState("down", (0,1), timeout),
            MoveState("left", (-1,0), timeout),
            MoveState("right", (1,0), timeout)
        ]
        edges = [
            Transition("idle_1","move_up", ".*timeout.*"),
            Transition("idle_2","move_left", ".*timeout.*"),
            Transition("idle_4","move_right", ".*timeout.*"),
            Transition("idle_3","move_down", ".*timeout.*"),
            Transition("move_up","idle_2", ".*timeout.*"),
            Transition("move_left","idle_3", ".*timeout.*"),
            Transition("move_right","idle_1", ".*timeout.*"),
            Transition("move_down","idle_4", ".*timeout.*"),
            Transition("move_up","idle_2", ".*collision.*"),
            Transition("move_left","idle_3", ".*collision.*"),
            Transition("move_right","idle_1", ".*collision.*"),
            Transition("move_down","idle_4", ".*collision.*")
        ]
        return StateMachine(states, edges, "idle_1")

    def _produce_physical( self ):
        return PhysicalState(PG.Rect(0, 0, 20, 40), (0,0), 1.0)
