##  @file EventTests.py
#   @author Joseph Ciurej
#   @date Spring 2014
#
#   Test File for the "Event" Type
#
#   @TODO
#   - The tests for the 'repr' and 'str' functions of the event type are
#     volatile and should be made more general.
#   - The tests for the 'repr' and 'str' non-empty functions shouldn't rely
#     on the arbitrary orderings given by the 'Event' type.

import unittest
import src
from src.Event import *

##  Container class for the test suite that tests the functionality of the
#   "Event" type.
class EventTest( unittest.TestCase ):
    ### Testing Constants ###

    ##  The event type that will be assigned to the test event.
    EVENT_TYPE = EventType.NOTIFY

    ##  The parameter listing that will be assigned to the test event.
    EVENT_PARAMS = { "one": 1, "two": 2 }

    ### Test Set Up/Tear Down ###

    def setUp( self ):
        self._event = Event( EventTest.EVENT_TYPE, EventTest.EVENT_PARAMS )

    def tearDown( self ):
        self._event = None

    ### Testing Functions ###

    def test_default_constructor( self ):
        default_event = Event()

        self.assertEqual( default_event.get_type(), EventType.NOTIFY,
            "Incorrect type on default initialization." )
        self.assertEqual( default_event.get_parameters(), {},
            "Incorrect parameters on default initialization." )


    def test_value_contructor( self ):
        self.assertEqual( self._event.get_type(), EventTest.EVENT_TYPE,
            "Incorrect type on explicit value initialization." )
        self.assertEqual( self._event.get_parameters(), EventTest.EVENT_PARAMS,
            "Incorrect parameters on explicit value initialization." )


    def test_equality_operator( self ):
        event1 = Event()
        event2 = Event()

        self.assertTrue( event1 == event1,
            "Equality operator doesn't return true for self equality in simple case." )
        self.assertTrue( self._event == self._event,
            "Equality operator doesn't return true for self equality in complex case." )
        self.assertTrue( event1 == event2,
            "Equality operator doesn't return true for two equivalent objects." )
        self.assertTrue( event1 != self._event,
            "Equality operator improperly returns true for two unequivalent objects." )


    def test_repr_empty( self ):
        event_repr = repr( Event() )

        self.assertEqual( event_repr, EventType.NOTIFY,
            "Incorrect representation string for an empty event." )


    def test_repr_nonempty( self ):
        event_repr = repr( self._event )
        repr_components = event_repr.split( "," )

        self.assertEqual( repr_components[0], EventTest.EVENT_TYPE,
            "Incorrect type within string representation of non-empty event." )
        self.assertEqual( repr_components[1],
            "two:" + str( EventTest.EVENT_PARAMS["two"] ),
            "The first entry in the parameter dictionary shows up improperly " \
            "in event representation." )
        self.assertEqual( repr_components[2],
            "one:" + str( EventTest.EVENT_PARAMS["one"] ),
            "The second entry in the parameter dictionary shows up improperly " \
            "in event representation." )


    def test_str_empty( self ):
        event_str = str( Event() )

        self.assertEqual( event_str, "[" + EventType.NOTIFY + "]( )",
            "Incorrect string form for an empty event." )


    def test_str_nonempty( self ):
        event_str = str( self._event )

        self.assertEqual( event_str, "[" + EventTest.EVENT_TYPE + "]( " +
            "two->" + str( EventTest.EVENT_PARAMS["two"] ) + " "
            "one->" + str( EventTest.EVENT_PARAMS["one"] ) + " )",
            "Incorrect string formatting for a non-empty event." )

