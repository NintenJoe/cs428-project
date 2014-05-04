##  @file main.py
#   @author Joseph Ciurej
#   @date Winter 2014
#
#   Main Entry Point File Container for the "Zol" Game
#
#   @TODO
#   High Priority:
#   - Re-integrate the ` type to handle with user inputs once
#     it implements different key-up and key-down events.
#   Low Priority:
#   -
import os
import pygame as PG
from pygame.locals import *

from Globals import *
from GameView import GameView
from GameWorld import GameWorld
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
    game_view = GameView()
    game_world = GameWorld()

    game_running = True
    title_screen = True
    pause_screen = False
    gameover_screen = False

    game_clock = PG.time.Clock()
    prev_game_time = 0.0
    game_time = PG.time.get_ticks()

    game_clock.tick( FRAMES_PER_SECOND )

    ## Primary Game Loop ##
    while game_running:
        # Retrieve/Handle User Inputs #
        for input_event in PG.event.get():
            if input_event.type == PG.QUIT:
                game_running = False
                #MOVE_UP
            elif input_event.type == KEYDOWN or input_event.type == KEYUP:
                input_key = ""
                if input_event.key == K_UP:
                    input_key = MOVE_UP
                elif input_event.key == K_DOWN:
                    input_key = MOVE_DOWN
                elif input_event.key == K_LEFT:
                    input_key = MOVE_LEFT
                elif input_event.key == K_RIGHT:
                    input_key = MOVE_RIGHT
                elif input_event.key == K_SPACE and title_screen == True:
                    title_screen = False
                elif input_event.key == K_SPACE:
                    input_key = SPACE
                elif input_event.key == K_p and input_event.type == KEYDOWN:
                    pause_screen = not pause_screen
                elif input_event.key == K_q:
                    game_running = False
                elif input_event.key == K_r and gameover_screen == True:
                    game_view = GameView()
                    game_world = GameWorld()
                    gameover_screen = False

                event_type = EventType.KEYDOWN if input_event.type == KEYDOWN \
                    else EventType.KEYUP

                key_event = Event( event_type, {"key": input_key} )
                if pause_screen == False:
                    game_world.notify_of( key_event )

        if game_world._player_entity not in game_world._entities:
            gameover_screen = True
        else:
            # Update Game World #
            prev_game_time = game_time
            game_time = PG.time.get_ticks()

            if title_screen == False and gameover_screen == False and pause_screen == False:
                # TODO: Adjust the frame time here in a more elegant fashion.
                game_world.update( (game_time - prev_game_time) / 10 )

                # Render Game World #
                game_view.render( game_world )

            # Frame Stall #
            game_clock.tick( FRAMES_PER_SECOND )
        if title_screen == True:
            game_view._screen.fill( (255, 255, 255) )
            game_view._screen.blit(game_view.TITLE_IMAGE, game_view.IMAGE_RECT)

        if pause_screen == True:
            game_view._screen.fill( (255, 255, 255) )
            game_view._screen.blit(game_view.PAUSE_IMAGE, game_view.IMAGE_RECT)

        if gameover_screen == True:
            game_view._screen.fill( (255, 0 , 0) )
            game_view._screen.blit(game_view.GAMEOVER_IMAGE, game_view.IMAGE_RECT)

        PG.display.flip()
    # Exit the game after the primary game loop has been terminated.
    PG.quit()


if __name__ == "__main__":
    main()
