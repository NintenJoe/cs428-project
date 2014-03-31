##  @file main.py
#   @author Joseph Ciurej
#   @date Winter 2014
#
#   Main Entry Point File Container for the "Zol" Game
#
#   @TODO
#   High Priority:
#   - Re-integrate the `InputController` type to handle with user inputs once
#     it implements different key-up and key-down events.
#   Low Priority:
#   -

import pygame as PG
from pygame.locals import *

from Globals import GAME_NAME, FRAMES_PER_SECOND
#from GameView import GameView
from GameWorld import GameWorld
from InputController import InputController
from Event import Event, EventType

##  The primary entry point for the game.  This function handles the primary
#   game loop and logic.  This function should serve as a high level manager for
#   the game and should not need to perform complex operations.
#
#   The industry standard for the logic run in the primary game loop is as follows:
#       1. Retrieve User Inputs
#       2. Run the AI               --+
#       3. Update Positions           |--- Update Game World
#       4. Resolve Collisions       --+
#       5. Draw Graphics
#       6. Play Sounds
def main():
    PG.init()

    ## Game Variables ##
    #game_view = GameView()
    PG.display.set_mode((640,480))
    game_world = GameWorld()
    input_controller = InputController()

    game_clock = PG.time.Clock()
    prev_game_time = 0.0
    game_time = PG.time.get_ticks()
    game_running = True

    ## Primary Game Loop ##
    while game_running:
        # Retrieve/Handle User Inputs #
        for input_event in PG.event.get():
            if input_event.type == PG.QUIT:
                game_running = False
                InputController.MOVE_UP
            elif input_event.type == KEYDOWN or input_event.type == KEYUP:
                input_key = ""
                if input_event.key == K_UP:
                    input_key = InputController.MOVE_UP
                elif input_event.key == K_DOWN:
                    input_key = InputController.MOVE_DOWN
                elif input_event.key == K_LEFT:
                    input_key = InputController.MOVE_LEFT
                elif input_event.key == K_RIGHT:
                    input_key = InputController.MOVE_RIGHT

                event_type = EventType.KEYDOWN if input_event.type == KEYDOWN \
                    else EventType.KEYUP

                key_event = Event( event_type, {"key": input_key} )
                game_world.notify_of( key_event )

        # Update Game World #
        prev_game_time = game_time
        game_time = PG.time.get_ticks()
        game_world.update( game_time - prev_game_time )

        # Render Game World #
        #game_view.render( game_world )
        player_entity = game_world.get_entities()[1]
        print player_entity.get_physical_state().get_volume()

        # Frame Stall #
        game_clock.tick( FRAMES_PER_SECOND )

    # Exit the game after the primary game loop has been terminated.
    PG.quit()


if __name__ == "__main__":
    main()
