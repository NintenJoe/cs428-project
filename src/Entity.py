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

import Globals
import Queue
import json
import os.path
from xml.dom import minidom

from PhysicalState import *
from SimulationDelta import *
from StateMachine import *

##  The representation of a dynamic object within the scope of the world.  Each
#   entity object is an independent and autonomous item within the game world with 
#   its own physical and mental state.
class Entity( object ):
    ### Constructors ###

    ##  Constructs an entity with the given initial physical state delta and the
    #   given name identifier.
    #
    #   @param name The name identifier for the "Entity" to be constructed.
    #   @param initial_delta The initial physical state delta for the new "Entity."
    def __init__( self, name, initial_delta=PhysicalState() ):
        self._name = name
        self._event_queue = Queue.Queue()

        self._mntl_state = self._produce_machine()
        self._phys_state = self._produce_physical()
        self._chitbox_templates = self._produce_chitboxes()

        self._phys_state.add_delta( initial_delta )
        self._update_chitbox()


    ### Methods ###

    ##  Updates the state of the entity based on the given game time that has
    #   passed since the last update, returning any events generated.
    #
    #   @param time_delta The amount of game time that has passed in the frame.
    #   @return A list of "Event" objects generated during the "Entity" update.
    def update( self, time_delta ):
        sim_delta = SimulationDelta()

        prev_state = self._mntl_state.get_current_state().get_name()
        while not self._event_queue.empty():
            next_event = self._event_queue.get()
            sim_delta += self._mntl_state.simulate_transition( next_event )
        sim_delta += self._mntl_state.simulate_step( time_delta )
        post_state = self._mntl_state.get_current_state().get_name()

        self._phys_state.add_delta( sim_delta.get_entity_delta() )
        self._phys_state.update( time_delta )
        if prev_state != post_state:
            self._update_chitbox()

        # Death may be inevitable
        if self._is_dead():
            sim_delta += self._notify_of_death()

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

    ##  @return The composite hitbox descibing the collision volume information
    #    for the "Entity" object instance.
    def get_chitbox( self ):
        return self.get_physical_state().get_volume()

    ##  @return The current health associated with the instance "Entity"
    #   (returne as an integer)
    def get_curr_health( self ):
        return self.get_physical_state().get_curr_health()

    ##  @return The hitbox describing the broadest collision volume for the
    #    "Entity" object instance.
    def get_bbox( self ):
        return self.get_chitbox().get_bounding_box()

    ### Helper Methods ###

    ##  Updates the composite hitbox for the instance based on the current state.
    def _update_chitbox( self ):
        state_name = self._mntl_state.get_current_state().get_name()

        if state_name in self._chitbox_templates.keys():
            entity_chitbox = self.get_chitbox()
            chitbox_template = self._chitbox_templates[ state_name ]

            entity_chitbox.adopt_template( chitbox_template )

    ##  Produces the state machine for the entity instance, returning a
    #   reference to this produced machine.
    #
    #   @return The `StateMachine` instance constructed for the entity instance.
    def _produce_machine( self ):
        data = json.load( self._open_entity_file() )

        states = []
        for ele in data[ "states" ]:
            state_class = Globals.load_class(ele[0])
            states.append(state_class(*ele[1:]))

        edges = []
        for ele in data[ "edges" ]:
            edges.append(Transition(*ele))

        return StateMachine( states, edges, data["start"] if "start" in data else None )

    ##  Produces the initial physical state for the entity instance, returning
    #   a reference to this created state.
    #
    #   @return The `PhysicalState` instance constructed for the entity instance.
    def _produce_physical( self ):
        data = json.load( self._open_entity_file() )
        info = data[ "physical" ]

        pos_x = info[0][0]
        pos_y = info[0][1]
        velocity = ( info[1][0], info[1][1] )
        mass = info[2]
        curr_health = info[3]
        max_health = info[4]

        return PhysicalState( CompositeHitbox(pos_x, pos_y), velocity, mass, curr_health, max_health )

    ##  Produces the composite hitbox templates for the entity instance (based 
    #   on its state machine), returning a list of these templates.
    #
    #   @return A list of `CompositeHitbox` instances constructed for the entity.
    def _produce_chitboxes( self ):
        hitlist = {}

        # Get states and entity names
        for state in self._mntl_state.get_states():
            hitboxes = []

            # TODO: Add functionality to specify an anchor for each chitbox.
            tree = minidom.parse( self._open_state_hbox_file(state) )

            rects = tree.getElementsByTagName('rect')
            for rect in rects:
                x = int( rect.getAttribute('x') )
                y = int( rect.getAttribute('y') )
                w = int( rect.getAttribute('width') )
                h = int( rect.getAttribute('height') )
                h_class = str( rect.getAttribute('class') )

                hitboxes.append( Hitbox(x, y, w, h, h_class) )

            ax = 0
            ay = 0
            circles = tree.getElementsByTagName('circle')
            for circle in circles:
                ax = int( circle.getAttribute('cx') )
                ay = int( circle.getAttribute('cy') )

            hitlist[ state.get_name() ] = CompositeHitbox( 0, 0, hitboxes, ax, ay )

        return hitlist

    ##  Builds a simulation delta with a death event inside to notify the
    #   GameWorld of the instance's death.
    #   TODO: I don't really like this function name.
    def _notify_of_death( self ):
        death_event = Event( EventType.DEAD, {} )
        return SimulationDelta( PhysicalState(), [death_event] )
    
    ## @return Whether the instance is dead.
    def _is_dead( self ):
        return self.get_physical_state().get_curr_health() < 1

    ##  @return An open file handle for the data file for the instance entity.
    def _open_entity_file( self ):
        efile = self._name + ".json"
        return open( os.path.join(Globals.DATA_PATH, "entities", efile), "r" )

    ##  @return An open file handle for the data file for the hitbox hile
    #    associated with the given state of the instance entity.
    def _open_state_hbox_file( self, state ):
        sfile = state.get_name() + ".svg"
        return open( os.path.join(Globals.DATA_PATH, "hitbox", self._name, sfile), "r" )

