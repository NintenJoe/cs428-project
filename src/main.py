##  @file main.py
#   @author Joseph Ciurej
#   @date Winter 2014
#
#   Main Entry Point File Container for the "Zol" Game
#
#   @TODO
#   High Priority:
#   - Update the logic of the main game loop (current contents are examples).
#   Low Priority:
#   - Move the global game variables (i.e. 'GAME_NAME', 'SCREEN_SIZE') to
#     the 'Globals' module.
#   - Spruce up the file and remove unnecessary comments.

import pygame as PG
from pygame.locals import *
from World import World
from Camera import Camera
from Animation import Animation
from InputController import InputController
from GameView import GameView


### Global Variables ###
GAME_NAME = "Zol"                   # Name for the prototype game
SCREEN_SIZE = ( 640, 480 )          # Default size for the game screen
FRAMES_PER_SECOND = 60              # Number of update frames per second


### Primary Entry Point ###

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
    gameView = GameView()
    GAME_RUNNING = True

    #Set initial level
    gameView.change_environment('1','2')
    gameView.load_tilemap()

    print gameView.loaded_tiles

    move_x = 0
    move_y = 0
    move_tgt = PG.Rect(move_x, move_y, 640, 480)

    border = PG.Rect(0, 0, 960, 960)
    shift_time = 3000
    accumulated_shift = 0
    camera = Camera( move_tgt, shift_time, border)

    player = gameView.generate_entity([(16,0,16,40),(0,0,16,40)],'entities/man/man.bmp',1, 33, False)
    playerflag = 1

    input_controller = InputController()

    # Primary Game Loop #
    while GAME_RUNNING:
        # Retrieve/Handle User Inputs #
        key_events = PG.event.get([PG.KEYDOWN, PG.KEYUP])
        input_controller.processKeyEvents(key_events)

        for event in PG.event.get():
            if event.type == PG.QUIT:
                GAME_RUNNING = False
            elif event.type == InputController.MOVE_LEFT:
                move_x-=10
            elif event.type == InputController.MOVE_RIGHT:
                move_x+=10
            elif event.type == InputController.MOVE_UP:
                move_y-=10
            elif event.type == InputController.MOVE_DOWN:
                move_y+=10

            # TODO: Add more input handling.

        # TODO: Write updating logic here.

        move_tgt.left = move_x
        move_tgt.top = move_y

        accumulated_shift += PG.time.get_ticks() - gameView.GAME_TIME
        gameView.GAME_TIME = PG.time.get_ticks()

        if accumulated_shift > shift_time:
            accumulated_shift = 0

        camera.update( gameView.GAME_TIME )

        # Draw Graphics #
        # TODO: Write the draw logic for the game here.
        gameView.render(camera, SCREEN_SIZE)
        gameView.render_entity(camera, player, move_tgt, SCREEN_SIZE)

        # Stalls the current frame until a sufficient amount of time passes to
        # achieve the given frame rate.
        gameView.GAME_CLOCK.tick(FRAMES_PER_SECOND)

    # Exit the game after the primary game loop has been terminated.
    gameView.exit_game()


if __name__ == "__main__":
    main()
