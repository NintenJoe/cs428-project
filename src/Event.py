##  @file Event.py
#   @author Joseph Ciurej
#   @date Spring 2014
#
#   Source File for the "Event" Type
#
#   @TODO
#   - Update the 'repr' and 'str' methods in the 'Event' type as requirements
#     for event string representations change.
#   - Determine how user requests events will be classified as enumerated items
#     in the 'EventType' enumeration.
#   - Add functions that transform event classifications into regular
#     expressions.

##  An enumeration that contains the broad classifications for events that occur
#   within the game world.  These classifications are used to help better identify
#   events and their related contents.
class EventType():
    ### General Events ###

    ##  Indicates that the event is a simple notification event with no associated
    #   information.
    #   Parameters: { }
    NOTIFY = "notify"

    ##  Indicates that the event represents a state timeout for the given game
    #   world object.
    #   Parameters: { "objects": Entity }
    TIMEOUT = "timeout"

    ### Collision-Related Events ###

    ##  Indicates that the event represents a collision between two game world
    #   objects.
    #   Parameters: { "objects": (Entity, Entity), "volumes": (Rect list, Rect list) }
    COLLISION = "collision"


##  A representation of a discrete event that has occured within the scope of the
#   game world.  These events are used to encapsulate interactions between objects
#   and environments in the game world and to communicate this information to
#   relevant game world objects.
class Event():
    ### Constructors ###

    ##  Creates an event with the specified type and parameters.
    #
    #   @param etype The broad classification for the event instance, which should
    #    be one of the 'EventType' types.
    #   @param params The parameters for the event, which should match the
    #    required parameters for the given event type.
    def __init__( self, etype=EventType.NOTIFY, params={} ):
        self._type = etype
        self._params = params

    ### Overloaded Operators ###

    ##  Returns true if all aspects of the event operands are equivalent (i.e.
    #   type, parameters, etc.).
    #
    #   @return True if the instance event is equivalent to the given event and
    #    false otherwise.
    def __eq__( self, other ):
        return self._type == other._type and \
            self._params == other._params

    ##  @return A string of the form "[type],[paramName]:[paramValue], ..."
    #    (where the parameters are listed in an arbitrary order).
    def __repr__( self ):
        string = str( self._type )

        for param_name, param_value in self._params.iteritems():
            string += "," + str( param_name ) + ":" + repr( param_value )

        return string

    ##  @return A string of the form "[[type]( [paramName]->[paramValue] ... )"
    #    (where the parameters are listed in an arbitrary order).
    def __str__( self ):
        string = "[" + str( self._type ) + "]("

        for param_name, param_value in self._params.iteritems():
            string += " " + str( param_name ) + "->" + repr( param_value )

        string += " )"

        return string

    ### Methods ###

    ##  @return The type of the instance event as an 'EventType' instance.
    def get_type( self ):
        return self._type

    ##  @return The parameters for the event as a dictionary.  The contents
    #    of this dictionary depends on the event type.
    def get_parameters( self ):
        return self._params
