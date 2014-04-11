##  @file Transition.py
#   @author Joseph Ciurej
#   @date 06/03/2014
#
#   Source File for the "Transition" Type
#
#   @TODO
#   - Determine if this is more appropriate for this module file or if it 
#     should be contained within the "StateMachine" module instead.

import re

##  The representation of a directed edge within a state machine.  Each transition
#   encodes a set of events that invoke the transition from the source state of
#   the transition to the destination state.
class Transition( object ):
    ### Constructors ###

    ##  Creates a transition that encodes a transition from the given source state
    #   to the given destination state when an event in the given classification
    #   occurs.
    #
    #   @param src_name The name identifier for the source state.
    #   @param dst_name The name identifier for the destination state.
    #   @param event_class A regular expression that describes the events that
    #    will invoke the instance transition.
    def __init__( self, src_name, dst_name, event_class=".*" ):
        self._src_state = src_name
        self._dst_state = dst_name

        self._event_class = re.compile( event_class )

    ### Methods ###

    ##  Determines whether the given event object invokes the given transition,
    #   returning a Boolean value indicating the result.
    #
    #   @param event The event object that will be checked for transition invocation.
    #   @return True if the given event invokes the instance transition and
    #    false otherwise.
    def invoked_by( self, event ):
        return True if self._event_class.search( repr(event) ) else False

    ##  @return The name identifier for the source state of the transition.
    def get_source( self ):
        return self._src_state

    ##  @return The name identifier for the destination state of the transition.
    def get_destination( self ):
        return self._dst_state

    ## @return a unique string for this object
    def __repr__(self):
        return self._source_state+"->"+self._dst_state+","+_event_class

