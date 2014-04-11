##  @file Identifiable.py
#   @author Joseph Ciurej
#   @date Spring 2014
#
#   Source File for the "Identifiable" Type
#
#   @TODO
#   High Priority:
#   - 
#   Low Priority:
#   - Adjust the class to distribute unique identifiers based on a per-subclass
#     basis instead of a global basis.
#   - Determine whether or not assigning unique identifiers to all game world
#     objects will be feasible, and build infrastructure to reuse old identifiers
#     if necessary.

import abc

##  An interface class 
class Identifiable( object ):
    __metaclass__ = abc.ABCMeta

    ### Static Fields ###

    ##  An incremental unique ID generation function that generates object IDs.
    GENERATE_UID = itertools.count().next

    ### Constructors ###

    ##  Constructs an identifiable object and assigns this new object a unique
    #   identifier.
    def __init__( self ):
        self._id = Identifiable.GENERATE_UID()

    ### Methods ###

    ##  @return The unique integer identifier for the identifiable object.
    def get_id( self ):
        return self._id

