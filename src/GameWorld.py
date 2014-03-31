##  @file GameWorld.py
#   @author Joseph Ciurej
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

from Monster import *
from Player import *
from Event import *
from CollisionDetector import *
from SpatialDictionary import *
from Camera import *
from World import *

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
        # NOTE: World needs to be able to load different configurations.
        # NOTE: World must provide an interface to get the current level.
        self._world = World()
        # NOTE: World must provide an interface to get the inhabiting entities
        # by default (at least the names of these entities).
        self._entities = [
            Monster( "monster", PhysicalState(PG.Rect(200, 200, 0, 0)) ),
            Player( "player", PhysicalState(PG.Rect(480, 480, 0, 0)) ),
        ]

        self._setup_tilemap()

        # NOTE: Must designate some entity within the entity list as the 'main'
        # entity.  This entity's hitbox will be set as the camera's focus.
        self._camera = Camera( target=self._entities[1].get_hitbox(), new_border=PG.Rect(0, 0, 960, 960) )
        # NOTE: World must provide an interface to get level width/height in pixels.
        self._collision_detector = SpatialDictionary( 240, 960, 960 )

        self._setup_collision_detector()

    ### Methods ###

    ##  Updates the state of the game world based on the given time delta,
    #   which represents the amount of time that has passed since the last update.
    #
    #   @param time_delta The amount of game time that has passed in the frame.
    def update( self, time_delta ):
        for entity in self._entities:
            # NOTE: The events passed back by the entities should be handled
            # here in the future.
            entity.update( time_delta )

        for entity_collision in self._collision_detector.get_all_collisions():
            self._resolve_entity_collision( entity_collision )

        # NOTE: There should be some easy way to get the tiles with which an
        # `Entity` in the game world collides.
        #tile_collisions = self._get_tile_collisions()
        #[ self._resolve_collision( collision ) for collision in tile_collisions ]

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

    ##  @return The camera providing the view into the world (of type `Camera`).
    def get_camera( self ):
        return self._camera

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

    ##  Removes the given entity from the collision detection system.
    #
    #   @param entity The `Entity` object instance to be removed from the
    #    collision detection system for the game world.
    def _remove_from_collision_detector( self, entity ):
        del self._cdrepr2entity_dict[ entity.get_hitbox() ]

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

        # TODO: Clean up this last segment of the function!
        collision_rect = entity1.get_hitbox().clip( entity2.get_hitbox() )
        moving_volume = entity1.get_hitbox() if entity1.get_name().find( "player" ) != -1 \
            else entity2.get_hitbox()

        move_x = 0
        move_y = 0
        if collision_rect.w < collision_rect.h:
            move_x = -collision_rect.w if moving_volume.x < collision_rect.x else collision_rect.w
        else:
            move_y = -collision_rect.h if moving_volume.y < collision_rect.y else collision_rect.h

        moving_volume.move_ip( move_x, move_y )

    ##  Resolves a collision between an `Entity` object and a `Tile` object
    #   TODO
    def _resolve_tile_collision( self, collision ):
        pass

    ##  TODO: Remove this function.
    def _setup_tilemap( self ):
        self._tilemap = []

        curr_segment = self._world.levels[ "1" ].segments[ "2" ]
        collision_map = curr_segment.get_collisionmap()

        for x in range( len(collision_map) ):
            tilemap_column = []
            for y in range( len(collision_map[0]) ):
                tilemap_column.append( "6" if collision_map[x][y] else "4" )
            self._tilemap.append( tilemap_column )

