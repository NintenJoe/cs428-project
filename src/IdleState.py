##  @file IdleState.py
#   @author Joseph Ciurej
#   @date Spring 2014
#
#   Source File for the "IdleState" Type
#
#   @TODO
#   - Determine whether or not this class should be in the 'State' module or
#     not.

from State import *
from PhysicalState import *

##  A type of state that represents a lack of movement or other ancillary state
#   changes.  Essentially, this is a state to represent object stillness.
class IdleState( State ):
    ### Constructors ###

    ##  Constructs a state instance with the given string identifier.
    #
    #   @param identifier A string identifier for that will represent the
    #    name of the instance state.
    def __init__( self, identifier ):
        super( IdleState, self ).__init__( "idle_" + identifier )

    ### Methods ###

    # Note: There are no public functions for this type!  For public method
    # reference, see the 'State' type.

    ### Helper Methods ###

    ##  Returns an empty set of physical changes.
    #
    #   @override
    def _calc_step_changes( self, time_delta ):
        return PhysicalState()

    ##  Returns an empty set of physical changes.
    #
    #   @override
    def _calc_arrival_changes( self ):
        return PhysicalState()

    ##  Returns an empty set of physical changes.
    #
    #   @override
    def _calc_departure_changes( self ):
        return PhysicalState()

