##  @file SpatialDictionary.py
#   @author Josh Halstead
#   @date Winter 2014
#
#   A spatial hashing collision detection strategy.
#
#   Given the dimensions of some part of the world, we overlay a grid of
#   virtual cells onto it. The dimensions of the square cells are uniform and
#   user-specified. Each cell may or may not contain game world entities, and
#   some game world entities may overlap multiple cells. From the cells, we
#   form a linear hashtable where each cell is identified by an integer index.
#   Game world entities will hash to said index if they exist (at all) inside
#   of the cell. For a given entity A, we can find its nearby neighbors by
#   hashing entity A and retrieving the other entities in that index. Then we
#   check if any of those objects collide with entity A. We do this for all
#   entities in the hash table to compute all collisions in the world.
#
#   Assumption: Width is a multiple of cell_size.

from CollisionDetector import *
from HashableRect import *

class SpatialDictionary( CollisionDetector ):

    ### Construtors ###

    ## Constructs a spatial hashing dictionary with a given cell size and
    #  width/height for detecting collisions amongst a set of bonding volumes.
    #
    #  @param cell_size An integer specifying the square dimensions of a cell
    #   in the game world. The cell size should be a factor of the width.
    #  @param width An integer specifying the total width of the area for which
    #   we're detecting collisions.
    #  @param height An integer specifying the total height of the area for
    #   which we're detecting collisions.
    def __init__(self, cell_size=1, width=1, height=1):
        # Initialize the super class
        CollisionDetector.__init__(self)

        # Configure the virtual grid
        self.cell_size = cell_size
        self.width = width
        self.height = height

        # Number of columns in the virtual grid
        self.columns = width/cell_size

        # Hashtable mapping a cell to a set of game world entities that exist
        # in said cell
        self.table = {}

        # Set of the objects (i.e. bounding volumes) being tracked
        self.dynamic_objects = set([])
        self.static_objects = set([])

    ### Public methods ###

    ## Returns a string representation of the spatial hashing dictionary. This
    #  is intended to be machine-readable.
    def __repr__(self):
        rep = "{"
        for cell in self.table:
            objects = ", ".join(str(obj) for obj in self.table[cell])
            rep += str(cell) + ":Set([" + objects + "]),"

        # Trim the last comma before appending the closing brace.
        return rep[:-1] + "}" if not rep == "{" else rep + "}"

    ## Returns a string representation of the spatial hashing dictionary. THis
    #  is intended to be human-readable
    def __str__(self):
        rep = "{"
        for cell in self.table:
            objects = ", ".join(str(obj) for obj in self.table[cell])
            rep += str(cell) + ":Set([" + objects + "]),\n"

        # Trim the last newline and comma before appending the closing brace.
        return rep[:-2] + "}" if not rep == "{" else rep + "}"

    ## Adds a list of bounding volumes to the dictionary. These bounding
    #  represent the hitboxes of the game world entities.
    #
    #  Note: The bounding volumes MUST be hashable.
    #
    #  @param objs A list of _hashable_ bounding volumes
    #  @param static A boolean signifying whether the objects are stationary
    def add_multiple(self, objs, static=False):
        for obj in objs:
            self.add(obj, static)

    ## Adds a single bounding volume to the dictionary. The bounding volume
    #  represents the hitbox of a game world entity.
    #
    #  Note: The bounding volume MUST be hashable.
    #
    #  @param obj A single bounding volume.
    #  @param static A boolean signifying whether the object is stationary
    def add(self, obj, static=False):
        cells = self._get_covered_cells(obj)
        for cell in cells:
            self._add(cell, obj)

    ## Removes a list of bounding volumes from the dictionary. The bounding
    #  volumes represent the hitboxes of the game world entities.
    #
    #  @param objs The list of bounding volumes to be removed.
    def remove_multiple(self, objs):
        for obj in objs:
            self.remove(obj)

    ## Removes a single bounding volumes from the dictionary. The bounding
    #  volume represents the hitbox of the game world entity.
    #
    #  @param objs The single bounding volumes to be removed.
    def remove(self, obj):
        cells = self._get_covered_cells(obj)
        for cell in cells:
            self._remove(cell, obj)

    ## Updates all the bounding volumes in the dictionary. If bounding volumes
    #  have moved to new cells since the last time update was called, then it
    #  must be called again before calling get_all_collisions.
    def update(self):
        objects = self.dynamic_objects.copy()

        self.remove_multiple(objects)
        self.add_multiple(objects)

    ## Determines all the collisions that are occuring given the current state
    #  of the spatial hashing dictionary.
    #
    #  @return A list of (Bounding Volume, Bounding Volume) frozensets of
    #          colliding game world entities.
    def get_all_collisions(self):
        static_collisions = self._get_collisions(self.static_objects)
        dynamic_collisions = self._get_collisions(self.dynamic_objects)

        static_collisions.update(dynamic_collisions)
        return list(static_collisions)

    ## Finds all the collisions between the given set of objects and all other
    #  objects in the dictionary.
    #
    #  @param objs A set of objects to be checked for collisions
    #  @return A set of (Bounding Volume, Bounding Volume) frozensets
    #          representing the colliding objects.
    def _get_collisions(self, objs):
        collisions = set([])

        for obj in objs:
            nearby_objects = self._get_nearby_objects(obj)
            for nearby_object in nearby_objects:
                if obj.colliderect(nearby_object):
                    collisions.add(frozenset([obj, nearby_object]))

        return collisions

    ## @return A list of all the bounding volumes currently being tracked.
    def get_all_objects(self):
        return list(self.static_objects) + list(self.dynamic_objects)

    ## @return True if we're tracking the provided bounding volume and false
    #   otherwise.
    def exists(self, obj):
        cells = self._get_covered_cells(obj)
        for cell in cells:
            if (cell not in self.table or obj not in self.table[cell]):
                return False

        return True

    ## @return The number of objects in the dictionary.
    def size(self):
        return len(self.static_objects) + len(self.dynamic_objects)

    ## Resets the spatial hashing dictionary.
    def clear(self):
        self.static_objects = set([])
        self.dynamic_objects = set([])
        self.table.clear()

    ### Private helper methods ###

    ## Adds a bounding volume to a cell.
    #
    #  @param cell The cell index that contains the bounding volume.
    #  @param obj The bounding volume that we're adding to the cell.
    #  @param static A boolean signifying whether the object is stationary.
    def _add(self, cell, obj, static=False):
        if static:
            self.static_objects.add(obj)
        else:
            self.dynamic_objects.add(obj)

        if cell in self.table:
            self.table[cell].add(obj)
        else:
            self.table.setdefault(cell, set()).add(obj)

    ## Removes a bounding volume from a cell.
    #
    #  @param cell The cell index that contains the bounding volume.
    #  @param obj The bounding volume that we're removing from the cell.
    def _remove(self, cell, obj):
        if obj in self.static_objects:
            self.static_objects.discard(obj)
        else:
            self.dynamic_objects.discard(obj)

        if cell in self.table:
            self.table[cell].discard(obj)

    ## Maps a given (x, y) position in the game world, to a cell's index in the
    #  spatial dictionary.
    #
    #  @param x The x-coordinate
    #  @param y The y-coordinate
    def _hash(self, x, y):
        return (int(x/self.cell_size) +
                int(y/self.cell_size) * self.columns)

    ## @return A list of bounding volumes that are in the same cell(s) as
    #   the given one.
    def _get_nearby_objects(self, obj):
        nearby_objects = set([])
        cells = self._get_covered_cells(obj)
        for cell in cells:
            nearby_objects = nearby_objects | self._objs_in(cell)

        # Exclude the object from this list.
        nearby_objects.discard(obj)
        return list(nearby_objects)

    ## @return A list of cells that a given bounding volume overlaps.
    def _get_covered_cells(self, obj):
        x = obj.x
        y = obj.y
        w = obj.width
        h = obj.height

        tl_cell = self._hash(x, y)
        tr_cell = self._hash(x + w, y)
        bl_cell = self._hash(x, y + h)

        covered_cells = set()
        row_count = self._get_num_covered_rows(tl_cell, bl_cell)
        for i in range(0, row_count):
            col_start = tl_cell + (i * self.columns)
            col_stop = tr_cell + (i * self.columns) + 1
            covered_cells |= set(range(col_start, col_stop))

        return list(covered_cells)

    ## Computes the number of rows in the grid that a bounding volume overlaps.
    #
    #  @param start The cell that contains the top left corner of the bounding
    #   volume.
    #  @param stop The cell that contains the bottom left corner of the
    #   bounding volume.
    #  @return The number of rows a bounding volume overlaps.
    def _get_num_covered_rows(self, start, stop):
        return (stop - start)/self.columns + 1

    ## @return A set containing all the bounding volumes in a given cell. The
    #  cell is assumed to exist in the table.
    def _objs_in(self, cell):
        if cell in self.table:
            return self.table[cell]
        else:
            return set()


