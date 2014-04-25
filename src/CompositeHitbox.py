##  @file CompositeHitbox.py
#   @author Joseph Ciurej
#   @date Spring 2014
#
#   Source File for the "CompositeHitbox" Type
#
#   @TODO
#   High Priority:
#   - Determine whether relationships between `Hitbox` and `CompositeHitbox`
#     instances should be maintained by these classes or computed manually
#     elsewhere (e.g. `GameWorld`).
#   - Add support in the equality operator to ensure that the types of the
#     hitboxes are considered when checking equality.
#   Low Priority:
#   - Determine if there's a means better than typing to facilitate arbitrary
#     behavioral mapping to hitboxes.
#   - Update the `HitboxType` types to better represent the array of behavior
#     possible for hitboxes on collision.
#   - Add support for intangible hitboxes by either identifying individual
#     hitboxes as intangible or by allowing for type mixins.
#   - Determine whether `id()` or `Identifiable` should be used to make all
#     `Hitbox` instances unique.
#   - Improve deep copy support to the `CompositeHitbox` type when it intakes a
#     listing of composite boxes.
#   - Remove assumption from `CompositeHitbox` constructor that all `Hitbox`
#     instances have positive x and y position values (valid for now since
#     composite hitboxes will be read in from file).
#   - Make the implementation of the equality operator in the `CompositeHitbox`
#     type more elegant.
#   - Add testing for the `Hitbox` type's `__repr__` function.
#   - Refactor the anchor functionality of the `CompositeHitbox` type.

import itertools
import pygame as PG

##  An enumeration that contains the broad classifications for hitboxes.  These
#   classifications help to define behavior on collision.
class HitboxType():
    ### General Classifications ###

    ##  Indicates that the described hitbox doesn't have any special behavior
    #   associated with it.
    DEFAULT = "default"

    ##  Indicates that the described hitbox is susceptible to attack.
    #   TODO: Update or remove this hitbox classification.
    VULNERABLE = "vulnerable"

    ##  Indicates that the described hitbox surrounds an attacking object.
    #   TODO: Update or remove this hitbox classification.
    HURT = "hurt"

    ##  Indicates that the described hitbox surrounds an intangible object.
    INTANGIBLE = "intangible"


##  The representation of a rectangular, axis-aligned collision volume within 
#   the game world.
class Hitbox( PG.Rect ):
    ### Constructors ###

    ##  Constructs a hitbox at the given position with the given dimensions.
    #   Optionally, the type of the hitbox (of type `HitboxType`) can be defined.
    #
    #   @param x The x-coordinate of the hitbox relative to its parent system.
    #   @param x The y-coordinate of the hitbox relative to its parent system.
    #   @param w The width of the hitbox (in number of pixels).
    #   @param h The height of the hitbox (in number of pixels).
    #   @param htype The classification to be attributed to the created hitbox.
    def __init__( self, x, y, w, h, htype=HitboxType.DEFAULT ):
        PG.Rect.__init__( self, x, y, w, h )
        self._type = htype

    ### Overloaded Operators ###

    ##  @return The hitbox type of the instance hitbox.
    def __repr__( self ):
        return str(self.htype)

    ##  @return The unique hashing integer identifier for the hitbox instance.
    def __hash__( self ):
        return id( self )

    ### Methods ###

    ##  Copies the contents of the given `Hitbox` into the instance `Hitbox`.
    #
    #   @param hitbox The `Hitbox` instance to have its values copied.
    def copy_ip( self, hitbox ):
        self.x = hitbox.x
        self.y = hitbox.y
        self.w = hitbox.w
        self.h = hitbox.h
        self._type = hitbox._type

    ##  @return The classification attributed to the hitbox (of type `HitboxType`).
    @property
    def htype( self ):
        return self._type

    ##  @return The identifier attributed to the hitbox (as an integer value).
    @property
    def hid( self ):
        return id( self )


##  The representation of a collision volume composed of multiple sub-volumes
#   within the game world.  Essentially, this type represents a collection
#   of `Hitbox` instances with a common origin point.
class CompositeHitbox( object ):
    ### Constructors ###

    ##  Constructs a composite hitbox composed of the given hitboxes located
    #   at the given position.
    #
    #   @param pos_x The horizontal game world position for the composite hitbox.
    #   @param pos_y The vertical game world position for the composite hitbox.
    #   @param hitbox_list A list of `Hitbox` objects that will compose the
    #    composite (positioned relative to the composite's origin).
    def __init__( self, pos_x=0, pos_y=0, hitbox_list=[], anchor_x=0, anchor_y=0 ):
        self._container_box = Hitbox( pos_x, pos_y, 0, 0 )
        self._anchor_pos = ( anchor_x, anchor_y )
        self._inner_boxes = [ Hitbox(0, 0, 0, 0) for i in range(6) ]

        self._adjust_boxes_to( hitbox_list )

    ### Overloaded Operators ###

    ##  @return True if the two composite hitboxes are equivalent (same sets
    #    of contained hitboxes, same positions) and false otherwise.
    def __eq__( self, other ):
        return self._container_box == other._container_box and \
            self._anchor_pos == other._anchor_pos and \
            len(self._inner_boxes) == len(other._inner_boxes) and \
            all(self._inner_boxes.count(i) == other._inner_boxes.count(i) for i in self._inner_boxes)

    ### Methods ###

    ##  Transforms the instance composite to adopt the composite template given,
    #   adjusting the instance box structure (but not position) to match template.
    #
    #   @param chitbox_template The template to be adopted by the instance.
    def adopt_template( self, chitbox_template ):
        self._adjust_boxes_to( chitbox_template.get_inner_boxes_relative() )

        other_anchor_pos = chitbox_template.get_anchor()
        anchor_shift = (
            self._anchor_pos[ 0 ] - other_anchor_pos[ 0 ],
            self._anchor_pos[ 1 ] - other_anchor_pos[ 1 ],
        )
        self.translate( anchor_shift[0], anchor_shift[1] )
        self._anchor_pos = other_anchor_pos

    ##  Translates the composite hitbox by the given amount along the two
    #   cardinal axes.
    #
    #   @param delta_x The translation amount along the horizontal axis.
    #   @param delta_y The translation amount along the vertical axis.
    def translate( self, delta_x, delta_y ):
        self._container_box.x += delta_x
        self._container_box.y += delta_y

        for inner_box in self._inner_boxes:
            inner_box.x += delta_x
            inner_box.y += delta_y

    ##  Places the instance composite hitbox at the given location in the world.
    #
    #   @param pos_x The new location for the composite along the horizontal axis.
    #   @param pos_y The new location for the composite along the vertical axis.
    def place_at( self, pos_x, pos_y ):
        cbox_pos = self.get_position()

        self.translate( -cbox_pos[0], -cbox_pos[1] )
        self.translate( pos_x, pos_y )

    ##  @return The position of the composite as a tuple of the form (x, y).
    def get_position( self ):
        return ( self._container_box.x, self._container_box.y )

    ##  @return The position of the anchor as a tuple of the form (x, y).
    def get_anchor( self ):
        return self._anchor_pos

    ##  @return A `Hitbox` container for all the hitboxes that compose the composite.
    def get_bounding_box( self ):
        return self._container_box

    ##  @return A listing of all the `Hitbox` objects that compose the composite.
    def get_inner_boxes( self ):
        return self._inner_boxes

    ##  @return A listing of all `Hitbox` objects that represents the inner hitboxes
    #    of the composite relative to the composite origin.
    def get_inner_boxes_relative( self ):
        cbox_pos = self.get_position()

        return [
            Hitbox(hb.x - cbox_pos[0], hb.y - cbox_pos[1], hb.w, hb.h, hb.htype) \
            for hb in self._inner_boxes
        ]

    ### Helper Methods ###

    ##  Adjusts the hitboxes contained in the composite to match the given list
    #   of hitboxes.
    #
    #   @param hitbox_list A listing of `Hitbox` instances to be mirrored by
    #    the instance's hitbox list.
    def _adjust_boxes_to( self, hitbox_list ):
        chitbox_pos = self.get_position()

        # Reset Inner Hitboxes #
        for inner_hitbox in self._inner_boxes:
            inner_hitbox.copy_ip( Hitbox(0, 0, 0, 0, HitboxType.INTANGIBLE) )
            inner_hitbox.move_ip( chitbox_pos[0], chitbox_pos[1] )

        # Update Inner Hitboxes to Mirror Given List #
        for hitbox_idx in range( 0, len(hitbox_list) ):
            inner_hitbox = self._inner_boxes[ hitbox_idx ]
            new_hitbox = hitbox_list[ hitbox_idx ]

            inner_hitbox.copy_ip( new_hitbox )
            inner_hitbox.move_ip( chitbox_pos[0], chitbox_pos[1] )

        # Update Containing Hitbox #
        self._container_box.copy_ip( Hitbox(chitbox_pos[0], chitbox_pos[1], 0, 0) )
        self._container_box.unionall_ip(
            [ b for b in self._inner_boxes if b.htype != HitboxType.INTANGIBLE ]
        )

