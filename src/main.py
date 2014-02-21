##  @file main.py
#   @author Joseph Ciurej
#   @date Winter 2014
#
#   Main Entry Point File Container for the "Zol" Game
#
#   @TODO
#   High Priority:
#   - Update the logic of the main game loop (current contents are examples).
#   - Remove the 'Entity' class from this file and abstract it to its own
#     file module.
#   Low Priority:
#   - Move the global game variables (i.e. 'GAME_NAME', 'SCREEN_SIZE') to
#     the 'Globals' module.
#   - Spruce up the file and remove unnecessary comments.

import pygame as PG
from pygame.locals import *
from Segment import Segment
from Camera import Camera

# Global Variables #
GAME_NAME = "Zol"               # Name for the prototype game
SCREEN_SIZE = ( 640, 480 )          # Default size for the game screen
FRAMES_PER_SECOND = 60              # Number of update frames per second

# TODO: Abstract this type to a separate module.
class Entity():
    def __init__(self):
        self.rect = None

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

    GAME_SCREEN = PG.display.set_mode( SCREEN_SIZE )
    GAME_CLOCK = PG.time.Clock()
    GAME_FONT = PG.font.Font( None, 14 )
    GAME_RUNNING = True
    GAME_TIME = PG.time.get_ticks()

    PG.display.set_caption( GAME_NAME )
    PG.mouse.set_visible( True )

    segment = Segment( 0 )
    seg_img = segment.get_image()

    #tgt1 = Entity()
    #tgt2 = Entity()
    #tgt1.rect = PG.Rect( 0, 0, 2, 2 )
    #tgt2.rect = PG.Rect( -640, -480, 2, 2 )
    #tgt_i = 0
    #tgt_list = [ tgt1, tgt2 ]

    move_tgt = Entity()
    move_x = 0
    move_y = 0
    move_tgt.rect = PG.Rect(move_x, move_y, 640, 480)

    border = Entity()
    border.rect = PG.Rect(-400, -600, 6400, 4800)

    shift_time = 3000
    accumulated_shift = 0
    camera = Camera( move_tgt, shift_time, border)
    go_left = True

    # Primary Game Loop #
    while GAME_RUNNING:
        # Retrieve/Handle User Inputs #
        for event in PG.event.get():
            if event.type == PG.QUIT:
                GAME_RUNNING = False

            # TODO: Add more input handling.

        # Update Game World #
        # TODO: Write updating logic here.
        accumulated_shift += PG.time.get_ticks() - GAME_TIME
        GAME_TIME = PG.time.get_ticks()

        if accumulated_shift > shift_time:
            #tgt_i = (tgt_i + 1) % len(tgt_list)
            #camera.set_target( GAME_TIME, tgt_list[ tgt_i ] )
            accumulated_shift = 0
        if go_left:
            move_x = move_x - 1
        else:
            move_x = move_x + 1
        move_tgt.rect.left = move_x

        if move_x < -640:
            go_left = False
        if move_x > 640:
            go_left = True

        camera.update( GAME_TIME )

        # Draw Graphics #
        # TODO: Write the draw logic for the game here.
        GAME_SCREEN.fill( (0, 0, 0) )

        camera_pos = camera.get_position()
        #Needed to multiply by negative 1 so that camera movement doesn't look 'backwards'
        GAME_SCREEN.blit( seg_img, ( -1*camera_pos[0] + SCREEN_SIZE[0] / 2, -1*camera_pos[1] + SCREEN_SIZE[1] / 2 ) ) 
        #GAME_SCREEN.blit(GAME_FONT.render("FPS: %.3g" % GAME_CLOCK.get_fps(), 0, (255, 255, 255)), (5, 5))

        PG.display.flip()

        # Stalls the current fram until a sufficient amount of time passes to
        # achieve the given frame rate.
        GAME_CLOCK.tick(FRAMES_PER_SECOND)

    # Exit the game after the primary game loop has been terminated.
    PG.quit()


if __name__ == "__main__":
    main()
