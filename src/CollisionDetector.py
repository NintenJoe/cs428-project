##  @file CollisionDetector.py
#   @author Josh Halstead
#   @date Winter 2014
#
#   A collision detection class that takes a list of game objects and
#   returns a list of tupler of colliding objects. 


from SpatialDictionary import SpatialDictionary 


class CollisionDetector:

    def __init__(self, objects=[], cell_size=1, width=1, height=1):
        self.objs = objects
        self.sp_dict = SpatialDictionary(cell_size, width, height)
        self.sp_dict.add_objs(objects)

    def clear(self):
        self.sp_dict.clear()

    def add_objs(self, objs):
        self.sp_dict.add_objs(objs)

    def add_obj(self, obj):
        self.sp_dict.add_obj(obj)

    def remove_objs(self, objs):
        for obj in self.objs:
            self.remove_obj(obj)

    def remove_obj(self, obj):
        self.sp_dict.remove_obj(obj)

    def get_all_collisions(self):
        collision_set = set([])

        for obj in self.objs:
            nearby_objs = self.sp_dict.get_nearby_objs(obj)
            collision_set = (collision_set |
                             _get_set_of_collisions(obj, nearby_objs))

        return collision_set

    def _get_set_of_collisions(self, target, objs):
        collision_set = set([])

        for obj in objs:
            if target.bounding_volume.colliderect(obj.bounding_volume):
                collision_set.add(frozenset([target, obj]))

        return collision_set

    def exists(self, obj):
        return self.sp_dict.exists(obj)
