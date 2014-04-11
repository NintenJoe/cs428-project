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

import Queue
import json

from xml.dom import minidom

from PhysicalState import *
from SimulationDelta import *
from StateMachine import *
from Globals import load_image

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

        f = open('assets/data/entities/'+name+'.json', 'r')
        data = json.load(f)
        self._mntl_state = self._produce_machine(data)

        #Create a hitbox dict for every state
        states = self._mntl_state.get_states()
        self._hitboxes = self._load_hitboxes(states)

        self._phys_state = self._produce_physical(data)
        self._phys_state.add_delta( initial_delta )
        self._update_hitbox()

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
        self._update_hitbox()

        return sim_delta.get_events()

    ##  Notifies an entity of an event relevant to that entity, which may cause
    #   changes in the ephemeral state of the "Entity" on the next update.
    #
    #   @param event The event of which the instance "Entity" will be notified.
    def notify_of( self, event ):
        if self.get_name() == "boss":
            print repr(event)
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

    # TODO: Remove this function in later versions.
    def _update_hitbox( self ):
        state_name = self._mntl_state.get_current_state().get_name()

        if state_name in self._hitboxes.keys():
            chitbox = self.get_hitbox()
            new_chitbox = self._hitboxes[state_name]

            for idx in range( 0, len(new_chitbox.get_hitboxes()) ):
                curr_hitbox = chitbox.get_hitboxes()[idx]
                curr_new_hitbox = new_chitbox.get_hitboxes()[idx]

                curr_hitbox.x = chitbox.get_position()[0] + curr_new_hitbox.x
                curr_hitbox.y = chitbox.get_position()[1] + curr_new_hitbox.y
                curr_hitbox.w = curr_new_hitbox.w
                curr_hitbox.h = curr_new_hitbox.h
                curr_hitbox._type = curr_new_hitbox._type

            for idx in range( len(new_chitbox.get_hitboxes()), len(chitbox.get_hitboxes()) ):
                curr_hitbox = chitbox.get_hitboxes()[idx]
                curr_hitbox.x = chitbox.get_position()[0]
                curr_hitbox.y = chitbox.get_position()[1]
                curr_hitbox.w = 0
                curr_hitbox.h = 0
                curr_hitbox._type = HitboxType.DEFAULT

            chitbox.get_hitbox().w = max( [hb.x + hb.w for hb in chitbox.get_hitboxes()] ) - chitbox.get_hitbox().x
            chitbox.get_hitbox().h = max( [hb.y + hb.h for hb in chitbox.get_hitboxes()] ) - chitbox.get_hitbox().y

    ### Helper Methods ###

    ##  Produces the initial physical state for the entity instance, returning
    #   a reference to this created state.
    #
    #   @param data A dict containing all the initialization data for this type of Entity
    #   @return The "PhysicalState" instance constructed for the entity instance.
    def _produce_physical( self, data ):
        info = data['physical']

        rect = info[0]
        velocity = ( info[1][0], info[1][1] )
        mass = info[2]

        max_hitbox_count = max( [len(chb.get_hitboxes()) for chb in self._hitboxes.values()] )
        chitbox = CompositeHitbox( rect[0], rect[1],
            [Hitbox(0,0,0,0) for i in range(max_hitbox_count) ] )

        return PhysicalState(chitbox, velocity, mass)


    ##  Import class based on class path
    #   @see http://stackoverflow.com/a/8255024
    #
    #   @param cl The complete path to the class from the src folder
    #   @return The loaded class ready to be instantiated
    def _import_class(self, cl):
        d = cl.rfind(".")
        classname = cl[d+1:len(cl)]
        m = __import__(cl[0:d], globals(), locals(), [classname])
        return getattr(m, classname)


    ##  Produces the state machine for the entity instance, returning a
    #   reference to this produced machine.
    #
    #   @param data A dict containing all the initialization data for this type of Entity
    #   @return The "StateMachine" instance constructed for the entity instance.
    def _produce_machine( self, data ):
        states = []
        for ele in data['states']:
            state_class = self._import_class(ele[0])
            states.append(state_class(*ele[1:]))
        edges = []
        for ele in data['edges']:
            edges.append(Transition(*ele))
        if 'start' in data:
            return StateMachine(states, edges, data['start'])
        return StateMachine(states, edges)

    ##  Load in the hitboxes from a file and return them in a dict
    #   indexed by state.
    #
    #   @param states A list of all the states.
    #   @return A dict containing composite hitboxes indexed by state
    def _load_hitboxes(self, states):
        hitlist = {}

        # Get states and entity names
        for state in states:
            hitboxes = []

            state_name = state.get_name()
            f = open('assets/data/hitbox/' + self._name + '/' + state_name + '.svg', 'r')
            tree = minidom.parse(f)
            rects = tree.getElementsByTagName('rect')

            for rect in rects:
                x = int( rect.getAttribute('x') )
                y = int( rect.getAttribute('y') )
                w = int( rect.getAttribute('width') )
                h = int( rect.getAttribute('height') )
                h_class = str( rect.getAttribute('class') )

                hitboxes.append(Hitbox(x, y, w, h, h_class))

            hitlist[state_name] = CompositeHitbox(0, 0, hitboxes)

        return hitlist

