##  @file EntityTests.py
#   @author Joseph Ciurej
#   @date Spring 2014
#
#   Test File for the "Entity" Type
#
#   @TODO
#   - Write the implementation in this file!

import unittest
import src

from src.Entity import *
from src.StateMachine import *
from src.State import *
from src.Transition import *

from src.Event import *
from src.PhysicalState import *
from src.SimulationDelta import *

##  Basic class that overrides the abstract "Entity" class with the most basic 
#   functionality to facilitate testing.
class TestEntity( State ):
    ##  @override
    def _produce_physical( self ):
        pass

    ##  @override
    def _produce_machine( self ):
        pass


##  Container class for the test suite that tests the functionality of the
#   "Entity" type.
class EntityTests( unittest.TestCase ):
    ### Test Set Up/Tear Down ###

    def setUp( self ):
        pass

    def tearDown( self ):
        pass

    ### Testing Functions ###

    def test_test( self ):
        self.assertEqual( True, True, "" )

