##  @file CollisionDetector.py
#   @author Josh Halstead
#   @date Winter 2014
#
#   An abstract base class that defines the interface that all future collision
#   detection implementations must support.

from abc import ABCMeta, abstractmethod

class CollisionDetector( object ):
    __metaclass__ = ABCMeta

    # Accept an arbitrary argument list
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def add_multiple(self, objs):
        pass

    @abstractmethod
    def add(self, obj):
        pass

    @abstractmethod
    def remove_multiple(self, objs):
        pass

    @abstractmethod
    def remove(self, obj):
        pass

    @abstractmethod
    def get_all_collisions(self):
        pass

    @abstractmethod
    def get_all_objects(self):
        pass

    @abstractmethod
    def exists(self, entity):
        pass

    @abstractmethod
    def clear(self):
        pass
