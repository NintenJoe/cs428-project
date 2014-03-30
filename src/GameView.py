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
        self.GAME_TIME = PG.time.get_ticks()
        self.GAME_CLOCK = PG.time.Clock()
        self.GAME_TIME = PG.time.get_ticks()
        PG.display.set_caption( "Zol" )
        PG.mouse.set_visible( True )

        self.environment = None

    ### Methods ###

    ##  Update and draw the Game World
    #
    
    def render_environment(self, camera, SCREEN_SIZE):
        self.GAME_SCREEN.fill( (0, 0, 0) )

        camera_pos = camera.get_position()
        #Needed to multiply by negative 1 so that camera movement doesn't look 'backwards'
        self.GAME_SCREEN.blit(self.environment, ( -1*camera_pos[0] + SCREEN_SIZE[0] / 2, -1*camera_pos[1] + SCREEN_SIZE[1] / 2 ) )

    ##  Update and render a given entity
    #
    #   @param camera
    #   @oaram entity       Entity to be rendered
    #   @param new_loc      Location where entity will be rendered
    #
    
    def render_entity(self, camera, entity, new_loc, SCREEN_SIZE):
        #self.GAME_SCREEN.blit(self.GAME_FONT.render("FPS: %.3g" % self.GAME_CLOCK.get_fps(), 0, (255, 255, 255)), (5, 5))
        camera_pos = camera.get_position()
        self.GAME_SCREEN.blit(entity[0], (new_loc.centerx - camera_pos[0] + SCREEN_SIZE[0] / 2 , new_loc.centery - camera_pos[1] + SCREEN_SIZE[1] / 2))


        PG.display.flip()
    ##  Calls the animation class in order to generate an entity to draw
    #
    #   @param coordinates  Rectangle Coordinates for the sprites on a spritesheet
    #   @param filename     Path and Filename of the spritesheet
    #
    #   @return entity      Returns an entity to be rendered
    #
    
    def generate_entity(self, coordinates, filename, frame_count, frame_time, is_looping):
        img = Animation(filename, frame_count, frame_time, is_looping)
        entity = img.get_images_at(coordinates)
        return entity
    
    ##  Calls the World class in order to switch levels to draw
    #
    #
    #   @param level        Level Name
    #   @param segment      Segment Name
    #
    #   @return environment      Returns a world
    #
    def change_environment(self, level, segment):
        world = World()
        levelselect = world.levels[level]
        environment = levelselect.get_image(segment)
        self.environment = environment

    def exit_game(self):
        PG.quit()

        
