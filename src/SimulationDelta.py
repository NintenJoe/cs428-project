##  @file SimulationDelta.py
#   @author Joseph Ciurej
#   @date Spring 2014
#
#   Source File for the "SimulationDelta" Type
#
#   @TODO
#   - Find a better name for the collection of data associated with the
#     "SimulationDelta" type.
#   - Include more fields in the "SimulationDelta" type as needed.
#   - Consider integrating this class into the "State" module.
#       > Integration may increase cohesion of the types (this type is never
#         needed without the "State" type), but will make the files a bit harder
#         to read (with multiple classes in a single file).
#   - Fix the shallow copy issue within the "add" function if necessary (should
#     be fine since the "Event" elements are immutable).
#   - Make the equality operator agnostic of event ordering if event ordering
#     doesn't end up mattering.

import copy

from PhysicalState import *
from Event import *

##  The representation of the changes that accompany a simulation step for a
#   given state.  Essentially, each instance of this type represents a set of
#   changes corresponding to simulating a step or set of steps.
class SimulationDelta( object ):
    ### Constructors ###

    ##  Constructs a state simulation delta with the given initial changes.
    #
    #   @param edelta A "PhysicalState" instance representing a change in
    #    physical state to be applied to the "Entity" instance associated with
    #    the state for the simulation delta.
    #   @param events A listing of all the events (as "Event" instances) produced 
    #    during the simulation step.
    def __init__( self, edelta=PhysicalState(), events=[] ):
        self._entity_delta = PhysicalState()
        self._entity_delta.add_delta( edelta )

        self._events = copy.deepcopy( events )

    ### Overloaded Operators ###

    ##  Returns true if all aspects of the delta operands are equivalent (i.e.
    #   physical state changes, event listing, etc.).
    #
    #   @return True if the operand deltas are equivalent in changes and
    #    false otherwise.
    def __eq__( self, other ):
        return self._entity_delta == other._entity_delta and \
            self._events == other._events

    ##  Aggregates two "SimulationDelta" instances by combining all changes
    #   represented in the two operand deltas, returning the resultant aggregation.
    #
    #   @param other The "SimulationDelta" instance to be added to the instance
    #    "SimulationDelta."
    #   @return The aggregate "SimulationDelta," which represents the amalgamation
    #    of changes for the operand deltas.
    def __add__( self, other ):
        aggregate = SimulationDelta()

        aggregate._entity_delta.add_delta( self._entity_delta )
        aggregate._entity_delta.add_delta( other._entity_delta )
        aggregate._events.extend( self._events )
        aggregate._events.extend( other._events )

        return aggregate

    def __str__( self ):
        return "{PhysicalState: " + str(self._entity_delta) + ", events: " + str(self._events) + "}"
    ### Methods ###

    ##  @return The aggregate changes to the physical state of the "Entity"
    #    instance associated with the instance "SimulationDelta."
    def get_entity_delta( self ):
        return self._entity_delta

    ##  @return A listing of all the events produced during the simulation steps
    #    represented by the instance "SimulationDelta."
    def get_events( self ):
        return self._events

