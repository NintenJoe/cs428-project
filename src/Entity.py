##  @file Entity.py
#   @author Josh Halstead, Joseph Ciurej
#   @date Spring 2014
#
#   Source File for the "Entity" Type
#
#   @TODO
#   - Create a subclass type of this type to add testing coverage for this type.
#   - Override the default behvior of the "setup_machine" function to load a
#     finite-state machine from a file (when the logic is available).

from abc import ABCMeta, abstractmethod
from PhysicalState import *

##  The representation of a dynamic object within the scope of the world.  Each
#   entity object is an independent and autonomous item within the game world with 
#   its own physical and mental state.
class Entity( object ):
    ### Class Setup ###

    ##  Identifies the class as an abstract base class.
    __metaclass__ = ABCMeta

    ### Constructors ###

    ##  Constructs an entity with the given initial physical state configuration
    #   and the given name identifier.
    #
    #   @param name The name identifier for the entity object instance.
    #   @param initial_state The initial physical state configuration for the 
    #    entity object instance.
    def __init__( self, name, initial_state=PhysicalState() ):
        self._event_queue = Queue()

        self._phys_state = initial_state
        self._ephm_state = self._setup_statemachine()

    ### Methods ###

    ##  Updates the entity based given a time delta that represents the amount of
    #   time that has passed since the previous update in the game world.
    #
    #   @param time_delta The amount of time that has passed since the entity was
    #    last updated.
    def update( self, time_delta ):
        phys_delta = PhysicalState()

        while not self._event_queue.empty():
            event = self._event_queue.get()
            phys_delta.add_delta( self._ephm_state.notify_of(event) )
        phys_delta.add_delta( self._ephm_state.automate_step(time_delta) )

        self._phys_state.add_delta( phys_delta )

    ##  Notifies an entity of an event relevant to that entity.  This notification
    #   may cause changes in the ephermeral state of the entity.
    #
    #   @param event The event relevant to the entity instance of which the entity
    #    will be notified.
    def notify_of( self, event ):
        self._event_queue.put( event )

    ### Helper Methods ###

    ##  Sets up the state machine for the entity instance, returning this machine
    #   from this function.
    #
    #   @return The state machine instance that will be used as the ephermeral
    #    state for the entity instance.
    @abstractmethod
    def _setup_machine( self ):
        pass

