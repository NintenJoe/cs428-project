##  @file GameView.py
#   @author Edwin Chan
#   @date 3/27/2014
#
#   Source File for Viewing 
#
#   @TODO
#   - Implement everything

import os.path
import glob
import string
import pygame as PG
from pygame.locals import *
from Level import Level
from Segment import Segment
from World import World
from Animation import Animation
from Event import Event


##  This class is a container and viewing methods for camera,
#   world, and all entities. Its job is to load and construct the
#   GameWorld.
class GameView():
    ### Constructors ###

    ##  
    #   
    def __init__(self, SCREEN_SIZE):
        #self.eventManager = event
        
        PG.init()
        self.GAME_SCREEN = PG.display.set_mode( SCREEN_SIZE )
        self.GAME_FONT = PG.font.Font( None, 14 )
        PG.display.set_caption( "Zol" )
        PG.mouse.set_visible( True )

    ### Methods ###

    ## Calls the load function from World.py to render a new new level 

    def draw_tick(self, camera, player, move_tgt, seg_img, SCREEN_SIZE):
        self.GAME_SCREEN.fill( (0, 0, 0) )

        camera_pos = camera.get_position()
        #Needed to multiply by negative 1 so that camera movement doesn't look 'backwards'
        self.GAME_SCREEN.blit( seg_img, ( -1*camera_pos[0] + SCREEN_SIZE[0] / 2, -1*camera_pos[1] + SCREEN_SIZE[1] / 2 ) )
        #GAME_SCREEN.blit(GAME_FONT.render("FPS: %.3g" % GAME_CLOCK.get_fps(), 0, (255, 255, 255)), (5, 5))
        self.GAME_SCREEN.blit(player, (move_tgt.centerx - camera_pos[0] + SCREEN_SIZE[0] / 2 , move_tgt.centery - camera_pos[1] + SCREEN_SIZE[1] / 2))


        PG.display.flip()
    ## Calls the animation class in order to render an entity to draw
    def render_entity(self, coordinates, filename, frame_count, frame_time, is_looping):
        img = Animation(filename, frame_count, frame_time, is_looping)
        entity = img.get_image_at(coordinates)
        return entity

    def exit_game(self):
        PG.quit()

        
