##  @file GameWorld.py
#   @author Josh Halstead, Joseph Ciurej
#   @date Spring 2014
#
#   Source File for the "GameWorld" Type
#
#   @TODO
#   High Priority:
#   - Remove the `Camera` instance from the `GameWorld` type and export it
#     to a different module.
#       > The level of abstraction of the `Camera` doesn't match with the
#         level of the `GameWorld`.  It's still a model component, but it
#         should exist one level above the `GameWorld` for the best abstraction.
#   - Add support for actual world loading instead of just loading a default
#     world.
#   - Remove all 'NOTE' items within this file by fixing up the `GameWorld`
#     type.
#   Low Priority:
#   -

import pygame as PG
from Globals import TILE_DIMS

from Event import *
from CollisionDetector import *
from SpatialDictionary import *
from Camera import *
from World import *
from Entity import *

from PhysicalState import *

##  The representation of a world inhabited by various entities, which exist
#   within the realm of a world with particular rules and behaviors.  The
#   world evolves and changes in real time with successive updates.
class GameWorld():
    ### Constructors ###

    ##  Constructs a game world instance with the initial world specified by
    #   the input name parameter.
    #
    #   @param world_name The identifier for the initial world to be loaded.
    def __init__( self, world_name="" ):
        self._world = World()
        self._player_entity = None
        segment = self._world.levels[ "3" ].segments[ "3.1" ]
        self._load_new_segment(segment)

    ### Methods ###

    ##  Updates the state of the game world based on the given time delta,
    #   which represents the amount of time that has passed since the last update.
    #
    #   @param time_delta The amount of game time that has passed in the frame.
    def update( self, time_delta ):
        entity_gen_events = []
        for entity in self._entities:
            entity_gen_events = entity.update(time_delta)
            for event in entity_gen_events:
                if event.get_type() == EventType.DEAD:
                    self._remove_entity(entity)

        self._collision_detector.update()

        for entity_collision in self._collision_detector.get_all_collisions():
            self._resolve_entity_collision( list(entity_collision) )

        for entity in self._entities:
            transition = self._resolve_tile_collisions( entity )
            if (transition != None):
                self._load_new_segment(transition[0], transition[1])
                break

        self._camera.update( time_delta )

    ##  Notifies the game world of the given event, which is propogated to
    #   all proper entities on the next update.
    #
    #   @param event The event of which the game world will be notified.
    #   @param entities An optional listing of entities to be notified of the
    #    event.  If this list is empty, the event will be broadcasted.
    def notify_of( self, event, entities=[] ):
        entities_to_notify = self._entities if len(entities) == 0 else entities

        for entity in entities_to_notify:
            entity.notify_of( event )

    ##  @return A listing of all the entity objects contained within the world
    #    (of type `Entity` list).
    def get_entities( self ):
        return self._entities

    ##  @return A 2D matrix of strings where each string represents the
    #    identifier of the corresponding tile in the game world.
    def get_tilemap( self ):
        return self._tilemap

    ##  @return The rectangular view representing the player viewpoint of the
    #    game world (of type `pygame.Rect`).
    def get_viewport( self ):
        return self._camera.get_viewport()

    ### Helper Functions ###

    ##  Establishes the proper infrastructure to get the collision detection
    #   system for the world instance up and running.
    def _setup_collision_detector( self ):
        self._cdrepr2entity_dict = {}
        [ self._add_to_collision_detector( entity ) for entity in self._entities ]

    ##  Adds the given entity to the collision detection system.
    #
    #   @param entity The `Entity` object instance to be added to the collision
    #    detection system for the game world.
    def _add_to_collision_detector( self, entity ):
        for hitbox in entity.get_chitbox().get_inner_boxes():
            self._cdrepr2entity_dict[ hitbox ] = entity
            self._collision_detector.add( hitbox )

    ##  Removes the given entity from the collision detection system.
    #
    #   @param entity The `Entity` object instance to be removed from the
    #    collision detection system for the game world.
    def _remove_from_collision_detector( self, entity ):
        for hitbox in entity.get_chitbox().get_inner_boxes():
            del self._cdrepr2entity_dict[ hitbox ]
            self._collision_detector.remove( hitbox )

    ##  Given the collision system's representation of an entity, this function
    #   returns the actual `Entity` object associated with this representation.
    #
    #   @param cd_repr The representation of an entity given by the collision
    #    detector (i.e. a Rectangle).
    #   @return The `Entity` object instance assocaited with the representation.
    def _get_entity_from_collision_detector( self, cd_repr ):
        return self._cdrepr2entity_dict[ cd_repr ]

    ##  Given a collision between `Entity` objects given their representations
    #   in the collision detector as a two-tuple, this function returns an
    #   `Event` instance describing this collision event.
    #
    #   @param collision The two-tuple (Rect, Rect) given by the collision system.
    #   @return An `Event` representating the contents of the given collision.
    def _generate_collision_event( self, collision ):
        ( entity1, entity2 ) = (
            self._get_entity_from_collision_detector( collision[0] ),
            self._get_entity_from_collision_detector( collision[1] ),
        )
        event_args = {
            "objects": ( entity1, entity2 ),
            "volumes": ( collision[0], collision[1] )
        }

        if collision[0].htype == HitboxType.VULNERABLE and collision[1].htype == HitboxType.HURT:
            event_args.update( { "attacker": entity2, "victim": entity1 } )
        elif collision[1].htype == HitboxType.VULNERABLE and collision[0].htype == HitboxType.HURT:
            event_args.update( { "attacker": entity1, "victim": entity2 } )

        return Event( EventType.COLLISION, event_args )

    ##  Resolves a given collision between `Entity` objects given their
    #   representations in the collision detector as a two-tuple.
    #
    #   @param collision The two-tuple (Rect, Rect) given by the collision system.
    def _resolve_entity_collision( self, collision ):
        ( entity1, entity2 ) = (
            self._get_entity_from_collision_detector( collision[0] ),
            self._get_entity_from_collision_detector( collision[1] ),
        )

        collision_event = self._generate_collision_event( collision )

        if entity1 != entity2:
            entity1.notify_of( collision_event )
            entity2.notify_of( collision_event )

            self._resolve_collision( entity1.get_chitbox(), entity2.get_chitbox() )

    ##  Resolves the collisions between an `Entity` and all the world tiles
    #   with which it intersects.
    #
    #   @param entity The `Entity` object that will have its tile collisions resolved.
    #
    #   @return A tuple of the form (segment, starting_position) if the player is colliding
    #           with a transition tile, else None
    def _resolve_tile_collisions( self, entity ):
        entity_hitbox = entity.get_bbox()
        seg_dims = self._segment.get_dims()

        # Get bounds for tiles surrounding the entity
        start_idx_x = int( entity_hitbox.left / Globals.TILE_DIMS[0] )
        start_idx_y = int( entity_hitbox.top / Globals.TILE_DIMS[1] )
        final_idx_x = int( entity_hitbox.right / Globals.TILE_DIMS[0] ) + 1
        final_idx_y = int( entity_hitbox.bottom / Globals.TILE_DIMS[1] ) + 1

        # Get hitboxes for tiles that the entity is on top of
        tile_hitbox_list = []
        for idx_x in range( max(0, start_idx_x), min(final_idx_x, seg_dims[0]) ):
            for idx_y in range( max(0, start_idx_y), min(final_idx_y, seg_dims[1]) ):
                tile_hitbox = self._get_hitbox_from_tile(idx_x,idx_y)
                tile_hitbox_list.append( tile_hitbox )

                # Check for transitions to other segments
                if (entity == self._player_entity):
                    transition = self._segment.get_tile_transition(idx_x,idx_y)
                    if (transition != None):
                        new_segment = transition[0]
                        new_pos = (transition[1][0] + 2, transition[1][1] + 1)
                        # return the transition information so the new segment can be loaded
                        return (new_segment, new_pos)

        # Create composite hitbox of tangible tiles
        tile_collection_chitbox = self._get_composite_hitbox_from_hitboxes(tile_hitbox_list)

        # Resolve collision with the composite hitbox
        self._resolve_collision( entity.get_chitbox(), tile_collection_chitbox )

        # No transitions were found so we return None
        return None

    ##  Resolves a collision between two hitboxes, adjusting the them as
    #   necessary so that they're no longer intersecting.
    #
    #   @param chitbox_movable The composite to be resolved and moved in collision.
    #   @param chitbox_fixed The composite to be resolved in the collision.
    def _resolve_collision( self, chitbox_movable, chitbox_fixed ):
        hitbox_movable = chitbox_movable.get_bounding_box()
        hitbox_fixed = chitbox_fixed.get_bounding_box()

        collision_rect = hitbox_movable.clip( hitbox_fixed )
        res_vector = [ 0, 0 ]

        if collision_rect.w < collision_rect.h:
            res_factor = -1 if hitbox_movable.x < collision_rect.x else 1
            res_vector[ 0 ] = res_factor * ( collision_rect.w + 1 if collision_rect.w else 0 )
        else:
            res_factor = -1 if hitbox_movable.y < collision_rect.y else 1
            res_vector[ 1 ] = res_factor * ( collision_rect.h + 1 if collision_rect.h else 0 )

        chitbox_movable.translate( res_vector[0], res_vector[1] )

    ##  Removes an entity from the Game World.
    #
    #   @param entity The entity that needs to be removed
    def _remove_entity( self, entity ):
        # Remove from Collision Detector
        self._remove_from_collision_detector(entity)

        # Remove from Game World entity list
        if entity in self._entities:
            self._entities.remove(entity)

    def _load_new_segment(self, segment, player_pos=None):
        self._segment = segment
        segment_dims = segment.get_pixel_dims()
        self._tilemap = segment.get_tiles()
        self._entities = []

        # Create entities
        for ( (idx_x, idx_y), entity_class ) in segment.get_entities():
            entity_pos = ( TILE_DIMS[0] * idx_x, TILE_DIMS[1] * idx_y )

            if player_pos != None and entity_class == "player":
                self._player_entity.get_chitbox().place_at(TILE_DIMS[0] * player_pos[0], TILE_DIMS[1] * player_pos[1])
                self._entities.append(self._player_entity)
            else:
                entity = Entity( entity_class )
                entity.get_chitbox().place_at( entity_pos[0], entity_pos[1] )
                self._entities.append( entity )

                if entity_class == "player":
                    self._player_entity = entity

        # Initialize camera and collision detector
        self._camera = Camera( target=self._player_entity.get_bbox(),
            new_border=PG.Rect(0, 0, segment_dims[0], segment_dims[1]) )
        self._collision_detector = SpatialDictionary( segment_dims[0] / 16,
            segment_dims[0], segment_dims[1] )

        self._setup_collision_detector()

    ## Creates a hitbox for a tile specified by x and y coordinates.
    #
    #   @param x The x coordinate for the tile.
    #   @param y The y coordinate for the tile.
    #
    #   @return A hitbox that covers the tile.
    def _get_hitbox_from_tile(self, x, y):
        tile_is_tangible = self._tilemap[ x ][ y ][ 1 ]
        return Hitbox(
            x * Globals.TILE_DIMS[0],
            y * Globals.TILE_DIMS[1],
            Globals.TILE_DIMS[0],
            Globals.TILE_DIMS[1],
            HitboxType.DEFAULT if tile_is_tangible else HitboxType.INTANGIBLE
        )

    ## Creates a composite hitbox out of a list of individual hitboxes.
    #
    #   @param hitbox_list A list containing Hitboxes
    #
    #   @return A CompositeHitbox
    def _get_composite_hitbox_from_hitboxes(self, hitbox_list):
        x_list = [h.x for h in hitbox_list if h.htype != HitboxType.INTANGIBLE]
        y_list = [h.y for h in hitbox_list if h.htype != HitboxType.INTANGIBLE]

        if (len(x_list) == 0):
            return CompositeHitbox(0,0)
        else:
            min_x = min(x_list)
            min_y = min(y_list)
            for hitbox in hitbox_list:
                hitbox.x -= min_x
                hitbox.y -= min_y
            return CompositeHitbox( min_x, min_y, hitbox_list )
