##  @file CollisionDetector.py
#   @author Josh Halstead
#   @date Winter 2014
#
#   An abstract base class that defines the interface that all future collision
#   detection implementations must support.


from abc import ABCMeta, abstractmethod


class CollisionDetector:
    __metaclass__ = ABCMeta

    @abstractmethod
    def add_multiple(self, objs):
        return

    @abstractmethod
    def add(self, obj):
        return

    @abstractmethod
    def remove_multiple(self, objs):
        return

    @abstractmethod
    def remove(self, obj):
        return

    @abstractmethod
    def get_all_collisions(self):
        return []

    @abstractmethod
    def clear(self):
        return

    @abstractmethod
    def exists(self, entity):
        return False
