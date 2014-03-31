##  @file Entity.py
#   @author Josh Halstead, Joseph Ciurej
#   @date Spring 2014
#
#   Source File for the "Entity" Type
#
#   @TODO
#   High Priority:
#   - Override the default behvior of the "setup_machine" function to load a
#     finite-state machine from a file (when the logic is available).
#   - Add a means of changing hitbox information as an "Entity" object changes
#     between states.
#   - Determine how the hitbox information for an "Entity" object should
#     be loaded.
#       > Option 1 (current): Each "Entity" loads their own hitbox information
#         independent of all other entities.
#       > Option 2: Each "Entity" hitbox depends on the graphical assets used
#         to represent that entity (or equivalent hitbox information associated
#         with each asset).
#   - Assert that names correspond to actual supported entities, or implement
#     a default behavior for asset/hitbox loading.
#   Low Priority:
#   - Consider updating the interface of the 'Entity' object to allow for
#     returning newly produced events separate of the 'update' method.
#   - Consider converting the 'get_status' method to a 'str' or 'repr' method
#     for the sake of consistency.

from abc import ABCMeta, abstractmethod
from Queue import Queue

from PhysicalState import *
from SimulationDelta import *
import Queue

##  The representation of a dynamic object within the scope of the world.  Each
#   entity object is an independent and autonomous item within the game world with 
#   its own physical and mental state.
class Entity( object ):
    ### Class Setup ###

    ##  Identifies the class as an abstract base class.
    __metaclass__ = ABCMeta

    ### Constructors ###

    ##  Constructs an entity with the given initial physical state delta and the
    #   given name identifier.
    #
    #   @param name The name identifier for the "Entity" to be constructed.
    #   @param initial_delta The initial physical state delta for the new "Entity."
    def __init__( self, name, initial_delta=PhysicalState() ):
        self._name = name
        self._event_queue = Queue.Queue()

        self._phys_state = self._produce_physical()
        self._mntl_state = self._produce_machine()

        self._phys_state.add_delta( initial_delta )

    ### Methods ###

    ##  Updates the state of the entity based on the given game time that has
    #   passed since the last update, returning any events generated.
    #
    #   @param time_delta The amount of game time that has passed in the frame.
    #   @return A list of "Event" objects generated during the "Entity" update.
    def update( self, time_delta ):
        sim_delta = SimulationDelta()

        while not self._event_queue.empty():
            next_event = self._event_queue.get()
            sim_delta += self._mntl_state.simulate_transition( next_event )
        sim_delta += self._mntl_state.simulate_step( time_delta )

        self._phys_state.add_delta( sim_delta.get_entity_delta() )
        self._phys_state.update( time_delta )

        return sim_delta.get_events()

    ##  Notifies an entity of an event relevant to that entity, which may cause
    #   changes in the ephemeral state of the "Entity" on the next update.
    #
    #   @param event The event of which the instance "Entity" will be notified.
    def notify_of( self, event ):
        self._event_queue.put( event )

    ##  @return The status of the "Entity" instance as a string of the form
    #    "[entity-name] [state-name] [state-time]".
    def get_status( self ):
        entity_name = str( self._name )
        entity_state = self._mntl_state.get_current_state()

        entity_state_name = str( entity_state.get_name() )
        entity_state_time = str( entity_state.get_active_time() )

        return entity_name + " " + entity_state_name + " " + entity_state_time

    ##  @return The name identifier assigned to the "Entity" object instance.
    def get_name( self ):
        return self._name

    ##  @return The physical state of the "Entity" object instance (as a 
    #    "PhysicalState" object).
    def get_physical_state( self ):
        return self._phys_state

    ##  @return The mental state of the "Entity" object instance (as a 
    #   "StateMachine" object).
    def get_mental_state( self ):
        return self._mntl_state

    ##  @return The hitbox information associated with the instance "Entity"
    #    object (returned as a PyGame "Rect" object).
    def get_hitbox( self ):
        return self.get_physical_state().get_volume()

    ### Helper Methods ###

    ##  Produces the initial physical state for the entity instance, returning
    #   a reference to this created state.
    #
    #   @return The "PhysicalState" instance constructed for the entity instance.
    @abstractmethod
    def _produce_physical( self ):
        pass

    ##  Produces the state machine for the entity instance, returning a
    #   reference to this produced machine.
    #
    #   @return The "StateMachine" instance constructed for the entity instance.
    @abstractmethod
    def _produce_machine( self ):
        pass

