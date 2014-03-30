##  @file TestStates.py
#   @author Joseph Ciurej
#   @date Spring 2014
#
#   Container Module for Testing Types Derived from the "Entity" Type
#
#   @NOTE
#   The types implemented in this file exist solely for testing purposes.  The
#   functionality of these types serve only to be interesting in some way and
#   are in no way meaningful in terms of implementation code.
#
#   @TODO
#   - Move this file to a separate directory (perhaps a nested directory of
#     some kind within the 'test' project directory).
#   - Reduce code redundancy by implementing copy function for the
#     'SimulationDelta' type.

import pygame as PG
import src
from TestStates import *
from src.Entity import *
from src.StateMachine import *
from src.State import *
from src.PhysicalState import *
from src.Event import *
from src.SimulationDelta import *

##  Basic class that overrides the abstract "Entity" class with the most basic 
#   functionality to facilitate testing.
class SimpleTestEntity( Entity ):
    ##  The initial "PhysicalState" assigned to the entity.
    INITIAL_PHYSICAL = PhysicalState( volume=PG.Rect(1, 2, 3, 4), velocity=(5, 6),
        mass=7.0 )

    ## The set of "State" objects that comprise the entity's state machine.
    MACHINE_STATES = [
        SimpleTestState( "0", 3.0 ),
        SimpleTestState( "1", 2.0 ),
    ]

    ##  The set of "Transition" objects in the entity's state machine.
    MACHINE_TRANS = [
        Transition( MACHINE_STATES[0].get_name(), MACHINE_STATES[1].get_name() ),
        Transition( MACHINE_STATES[1].get_name(), MACHINE_STATES[0].get_name() ),
    ]

    ##  @override
    def _produce_physical( self ):
        return PhysicalState( volume=PG.Rect(1, 2, 3, 4), velocity=(5, 6), mass=7.0 )

    ##  @override
    def _produce_machine( self ):
        return StateMachine(
            SimpleTestEntity.MACHINE_STATES,
            SimpleTestEntity.MACHINE_TRANS
        )

