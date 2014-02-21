##  @file SpatialDictionary.py
#   @author Josh Halstead
#   @date Winter 2014
#
#   A sparse dictionary for spatial hashing.
#
#   Assumption: Bounding volumes are much smaller than a cell such that the
#   greatest number of cells that a bounding volume can overlap is 4.


class SpatialDictionary:

    def __init__(self, cell_size=1, width=1, height=1):
        self.cell_size = cell_size
        self.columns = width/cell_size
        self.width = width
        self.height = height
        self.entries = {}

    def add_objs(self, objs):
        for obj in objs:
            self.add_obj(obj)

    def add_obj(self, obj):
        cells = self._get_covered_cells(obj)
        for cell in cells:
            self._add(cell, obj)

    def _add(self, cell, obj):
        if cell in self.entries:
            self.entries[cell].add(obj)
        else:
            self.entries.setdefault(cell, set()).add(obj)

    # Returns a list of cells that a bounding volume overlaps
    def _get_covered_cells(self, obj):
        x = obj.bounding_volume.x
        y = obj.bounding_volume.y
        w = obj.bounding_volume.width
        h = obj.bounding_volume.height

        top_left = self._hash(x, y)
        top_right = self._hash(x + w, y)
        bottom_left = self._hash(x, y + h)
        bottom_right = self._hash(x + w, y + h)

        row_count = (top_left - bottom_left)/self.columns

        # Last resort, just add the cells that the 4 corners lie on and
        # make the assumption that the bounding_volumes are small enough
        # relative to the cell size so that a bounding volume can overlap
        # at most 4 cells.
        covered_cells = set()
        covered_cells.add(top_left)
        covered_cells.add(top_right)
        covered_cells.add(bottom_left)
        covered_cells.add(bottom_right)

#        covered_cells = set()
#        for i in range(0, 1 + row_count):
#            step = i * self.columns
#            lower = top_left + step
#            upper = top_right + step
#            covered_cells = covered_cells | set(range(lower, 1 + upper))

        return list(covered_cells)

    def _hash(self, x, y):
        return (int(x/self.cell_size) +
                int(y/self.cell_size) * self.columns)
   
    def remove_objs(self, objs):
        for obj in objs:
            self.remove_obj(obj)

    def remove_obj(self, obj):
        cells = self._get_covered_cells(obj)
        for cell in cells:
            self._remove(cell, obj)

    def _remove(self, cell, obj):
        if cell in self.entries:
            self.entries[cell].discard(obj)

    def get_nearby_objs(self, obj):
        nearby_objs = set([])
        cells = self._get_covered_cells(obj)
        for cell in cells:
            nearby_objs = nearby_objs | self._objs_in(cell)

        nearby_objs.discard(obj)
        return nearby_objs

    def _objs_in(self, cell):
        if cell in self.entries:
            return self.entries[cell]
        else:
            return set()

    def exists(self, obj):
        cells = self._get_covered_cells(obj)
        present = True
        for cell in cells:
            if cell in self.entries:
                present = present and (obj in self.entries[cell])
            else:
                return False

        return present

    def clear(self):
        self.entries.clear()
