##  @file TransitionTests.py
#   @author Joseph Ciurej
#   @date Spring 2014
#
#   Test File for the "Transition" Type
#
#   @TODO

import unittest
import src
from src.Transition import *
from src.Event import *

##  Container class for the test suite that tests the functionality of the
#   "Transition" type.
class TransitionTest( unittest.TestCase ):
    ### Testing Constants ###

    ##  The string identifier for the source node in the test transition.
    SRC_NAME = "source"

    ##  The string identifier for the destination node in the test transition.
    DST_NAME = "destination"

    ##  The only event that will invoke the test transition.
    TRANS_EVENT = Event( EventType.NOTIFY )

    ### Test Set Up/Tear Down ###

    def setUp( self ):
        self._transition = Transition( TransitionTest.SRC_NAME,
            TransitionTest.DST_NAME, repr(TransitionTest.TRANS_EVENT) )

    def tearDown( self ):
        self._transition = None

    ### Testing Functions ###

    def test_constructor( self ):
        self.assertEqual( self._transition.get_source(), TransitionTest.SRC_NAME,
            "Incorrect source node identifier on default construction." )
        self.assertEqual( self._transition.get_destination(), TransitionTest.DST_NAME,
            "Incorrect destination node identifier on default construction." )

    def test_invocation_by_valid_events( self ):
        valid_event = TransitionTest.TRANS_EVENT

        self.assertEqual( self._transition.invoked_by( valid_event ), True,
            "Transition not invoked by a valid invocation (exact same event)." )

        diffparam_event = Event( EventType.NOTIFY, { "derp" : None } )

        self.assertEqual( self._transition.invoked_by( diffparam_event ), True,
            "Transition not invoked by a valid invocation (different event params)." )

    def test_invocation_by_invalid_events( self ):
        difftype_event = Event( EventType.COLLISION )

        self.assertEqual( self._transition.invoked_by( difftype_event ), False,
            "Transition invoked by an invalid invocation (different event type)." )

