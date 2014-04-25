##  @file TestStates.py
#   @author Joseph Ciurej
#   @date Spring 2014
#
#   Container Module for Testing Types Derived from the "State" Type
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

import src
from src.State import *
from src.PhysicalState import *
from src.Event import *
from src.SimulationDelta import *

##  Basic class that overrides the abstract "State" class with the most basic 
#   functionality to facilitate testing.
class SimpleTestState( State ):
    ##  The "SimulationDelta" instance returned on a state step operation.
    STEP_DELTA = SimulationDelta( PhysicalState(mass=1.0), [ Event() ] )

    ##  The "SimulationDelta" instance returned on a state arrival operation.
    ARRIVAL_DELTA = SimulationDelta( PhysicalState(mass=2.0), [ Event() ] )

    ##  The "SimulationDelta" instance returned on a state departure operation.
    DEPARTURE_DELTA = SimulationDelta( PhysicalState(mass=3.0) )

    ##  @override
    def _calc_step_changes( self, time_delta ):
        return SimulationDelta( PhysicalState(mass=1.0), [ Event() ] )

    ##  @override
    def _calc_arrival_changes( self, event ):
        return SimulationDelta( PhysicalState(mass=2.0), [ Event() ] )

    ##  @override
    def _calc_departure_changes( self, event ):
        return SimulationDelta( PhysicalState(mass=3.0) )

