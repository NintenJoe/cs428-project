import pygame as PG
import os.path
import string


## This class processes key events and translates them into custom events.
#
#     This allows user actions such as player movement, pausing the game, etc.
#     to be abstracted to custom events. Changing which key activates which event
#     is done by changing the controls file in assets/prefs/
class InputController():

    # Custom Events
    MOVE_UP = PG.USEREVENT
    MOVE_DOWN = PG.USEREVENT+1
    MOVE_RIGHT = PG.USEREVENT+2
    MOVE_LEFT = PG.USEREVENT+3

    # Constructors #

    ## Loads custom controls
    def __init__(self):
        # has the form { pygame.key => Custom Event }
        self.input_map = {}

        # read controls file
        controls_filename = os.path.join('assets','prefs','controls')
        controls_file = open(controls_filename, 'r')

        for line in controls_file:
            divider = string.find(line,':')
            event_str = line[:divider]
            key_code = line[divider+1:].rstrip()

            if (event_str == 'UP'):
                self.input_map[int(key_code)] = self.MOVE_UP
            elif (event_str == 'DOWN'):
                self.input_map[int(key_code)] = self.MOVE_DOWN
            elif (event_str == 'RIGHT'):
                self.input_map[int(key_code)] = self.MOVE_RIGHT
            elif (event_str == 'LEFT'):
                self.input_map[int(key_code)] = self.MOVE_LEFT

    ## Takes pygame events and translates them into custom events
    #
    #   @param events A list of pygame keydown and keyup events to be processed
    def processKeyEvents(self, events):
        for event in events:
            if (event.key in self.input_map):
                custom_event = PG.event.Event(self.input_map[event.key])
                PG.event.post(custom_event)


