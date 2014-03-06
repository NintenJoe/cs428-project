##  @file SpatialDictionary.py
#   @author Josh Halstead
#   @date Winter 2014
#
#   A spatial hashing collision detection strategy.
#
#   Assumption: Width is a multiple of cell_size.

from CollisionDetector import *
from HashableRect import *


class SpatialDictionary(CollisionDetector):

    # Public methods

    def __init__(self, cell_size=1, width=1, height=1):
        CollisionDetector.__init__(self)

        self.cell_size = cell_size
        self.width = width
        self.height = height
        self.columns = width/cell_size
        self.table = {}

        # Set of the objects (i.e. bounding volumes) being tracked
        self.objects = set([])

    def __repr__(self):
        rep = "{"
        for cell in self.table:
            objects = ", ".join(str(obj) for obj in self.table[cell])
            rep += str(cell) + ":Set([" + objects + "]),"

        return rep + "}"

    def __str__(self):
        rep = "{"
        for cell in self.table:
            objects = ", ".join(str(obj) for obj in self.table[cell])
            rep += str(cell) + ":Set([" + objects + "]),\n"

        # Trim the last newline before appending the closing brace.
        return rep[:-1] + "}"

    def add_multiple(self, objs):
        self.objects.update(objs)

        for obj in objs:
            self.add(obj)

    def add(self, obj):
        self.objects.add(obj)

        cells = self._get_covered_cells(obj)
        for cell in cells:
            self._add(cell, obj)

    def remove_multiple(self, objs):
        self.objects -= set(objs)

        for obj in objs:
            self.remove(obj)

    def remove(self, obj):
        self.objects.discard(obj)

        cells = self._get_covered_cells(obj)
        for cell in cells:
            self._remove(cell, obj)

    def get_all_collisions(self):
        collisions = set([])
        for obj in self.objects:
            nearby_objects = self._get_nearby_objects(obj)
            for nearby_object in nearby_objects:
                if obj.colliderect(nearby_object):
                    collisions.add(frozenset([obj, nearby_object]))

        return list(collisions)

    def get_all_objects(self):
        return list(self.objects)

    def exists(self, obj):
        cells = self._get_covered_cells(obj)
        for cell in cells:
            if (cell not in self.table or obj not in self.table[cell]):
                return False

        return True

    def size(self):
        return len(self.objects)

    def clear(self):
        self.objects = set([])
        self.table.clear()

    # Private helper methods

    def _add(self, cell, obj):
        if cell in self.table:
            self.table[cell].add(obj)
        else:
            self.table.setdefault(cell, set()).add(obj)

    def _remove(self, cell, obj):
        if cell in self.table:
            self.table[cell].discard(obj)

    def _hash(self, x, y):
        return (int(x/self.cell_size) +
                int(y/self.cell_size) * self.columns)

    def _get_nearby_objects(self, obj):
        nearby_objects = set([])
        cells = self._get_covered_cells(obj)
        for cell in cells:
            nearby_objects = nearby_objects | self._objs_in(cell)

        # Exclude the object from this list.
        nearby_objects.discard(obj)
        return list(nearby_objects)

    # Returns a list of cells that a bounding volume overlaps
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

    def _get_num_covered_rows(self, start, stop):
        return (stop - start)/self.columns + 1

    def _objs_in(self, cell):
        if cell in self.table:
            return self.table[cell]
        else:
            return set()
