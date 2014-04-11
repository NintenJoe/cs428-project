##  @file GameWorld.py
#   @author Josh Halstead, Joseph Ciurej
#   @date Spring 2014
#
#   Source File for the "GameWorld" Type
#
#   @TODO
#   High Priority:
#   - Write the implementation in this file!
#   - Remove the `Camera` instance from the `GameWorld` type and export it
#     to a different module.
#       > The level of abstraction of the `Camera` doesn't match with the
#         level of the `GameWorld`.  It's still a model component, but it
#         should exist one level above the `GameWorld` for the best abstraction.
#   - Add support for actual world loading instead of just loading a default
#     world.
#   - Implement functionality associated with interpretting events sent back
#     by `Entity` object instances on update.
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

        segment = self._world.levels[ "1" ].segments[ "1.2" ]
        segment_dims = segment.get_pixel_dims()

        self._tilemap = segment.get_tiles()
        # TODO: Update when integrated with the `Entity` updates.
        self._entities = []
        player_entity = None
        for ( (x, y), entity_class ) in segment.get_entities():
            entity_pos = ( TILE_DIMS[0] * x, TILE_DIMS[1] * y )
            entity_phys = PhysicalState( PG.Rect(entity_pos[0], entity_pos[1], 0, 0) )
            entity = Entity(entity_class, entity_phys)

            if entity_class == "player":
                player_entity = entity

            self._entities.append( entity )

        # NOTE: Must designate some entity within the entity list as the 'main'
        # entity.  This entity's hitbox will be set as the camera's focus.
        self._camera = Camera( target=player_entity.get_hitbox(),
            new_border=PG.Rect(0, 0, segment_dims[0], segment_dims[1]) )
        self._collision_detector = SpatialDictionary( segment_dims[0] / 4,
            segment_dims[0], segment_dims[1] )

        self._setup_collision_detector()

    ### Methods ###

    ##  Updates the state of the game world based on the given time delta,
    #   which represents the amount of time that has passed since the last update.
    #
    #   @param time_delta The amount of game time that has passed in the frame.
    def update( self, time_delta ):
        # TODO: Handle the events passed back by the `Entity` updates.
        for entity in self._entities:
            entity.update( time_delta )
        self._collision_detector.update()

        for entity_collision in self._collision_detector.get_all_collisions():
            self._resolve_entity_collision( list(entity_collision) )

        for entity in self._entities:
            self._resolve_tile_collisions( entity )

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
        self._cdrepr2entity_dict[ entity.get_hitbox() ] = entity
        self._collision_detector.add( entity.get_hitbox() )

    ##  Removes the given entity from the collision detection system.
    #
    #   @param entity The `Entity` object instance to be removed from the
    #    collision detection system for the game world.
    def _remove_from_collision_detector( self, entity ):
        del self._cdrepr2entity_dict[ entity.get_hitbox() ]
        self._collision_detector.remove( entity.get_hitbox() )

    ##  Given the collision system's representation of an entity, this function
    #   returns the actual `Entity` object associated with this representation.
    #
    #   @param cd_repr The representation of an entity given by the collision
    #    detector (i.e. a Rectangle).
    #   @return The `Entity` object instance assocaited with the representation.
    def _get_entity_from_collision_detector( self, cd_repr ):
        return self._cdrepr2entity_dict[ cd_repr ]

    ##  Resolves a given collision between `Entity` objects given their
    #   representations in the collision detector as a two-tuple.
    #
    #   @param collision The two-tuple (Rect, Rect) given by the collision system.
    def _resolve_entity_collision( self, collision ):
        ( entity1, entity2 ) = (
            self._get_entity_from_collision_detector( collision[0] ),
            self._get_entity_from_collision_detector( collision[1] ),
        )
        collision_event = Event(
            EventType.COLLISION,
            {
                "objects": ( entity1, entity2 ),
                "volumes": ( entity1.get_hitbox(), entity2.get_hitbox() )
            }
        )

        entity1.notify_of( collision_event )
        entity2.notify_of( collision_event )

        # TODO: Determine the player entity and move that entity out.
        self._resolve_collision( entity1.get_hitbox(), entity2.get_hitbox() )

    ##  Resolves the collisions between an `Entity` and all the world tiles
    #   with which it intersects.
    #
    #   @param entity The `Entity` object that will have its tile collisions resolved.
    def _resolve_tile_collisions( self, entity ):
        entity_hitbox = entity.get_hitbox()
        tile_hitbox = PG.Rect( 0, 0, Globals.TILE_DIMS[0], Globals.TILE_DIMS[1] )

        start_idx_x = int( entity_hitbox.left / Globals.TILE_DIMS[0] )
        start_idx_y = int( entity_hitbox.top / Globals.TILE_DIMS[1] )
        final_idx_x = int( entity_hitbox.right / Globals.TILE_DIMS[0] ) + 1
        final_idx_y = int( entity_hitbox.bottom / Globals.TILE_DIMS[1] ) + 1

        for idx_x in range( start_idx_x, final_idx_x ):
            for idx_y in range( start_idx_y, final_idx_y ):
                tile_is_tangible = self._tilemap[ idx_x ][ idx_y ][ 1 ]

                if tile_is_tangible:
                    tile_hitbox.topleft = (
                        idx_x * Globals.TILE_DIMS[0],
                        idx_y * Globals.TILE_DIMS[1]
                    )

                    self._resolve_collision( entity_hitbox, tile_hitbox )

    ##  Resolves a collision between two hitboxes, adjusting the them as
    #   necessary so that they're no longer intersecting.
    #
    #   @param hitbox1 The first hitbox involved in a collision to be resolved.
    #   @param hitbox2 The second hitbox involved in a collision to be resolved.
    def _resolve_collision( self, hitbox1, hitbox2 ):
        collision_rect = hitbox1.clip( hitbox2 )
        res_vector = [ 0, 0 ]

        if collision_rect.w < collision_rect.h:
            res_factor = -1 if hitbox1.x < collision_rect.x else 1
            res_vector[ 0 ] = res_factor * collision_rect.w
        else:
            res_factor = -1 if hitbox1.y < collision_rect.y else 1
            res_vector[ 1 ] = res_factor * collision_rect.h

        # TODO: Update this functionality once the `CompositeHitbox` structure
        # is integrated.
        hitbox1.move_ip( res_vector[0], res_vector[1] )

