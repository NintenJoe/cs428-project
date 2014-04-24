##  @file Globals.py
#   @author Joseph Ciurej
#   @date Winter 2014
#
#   A container file for all of the global variables and functions used in the 
#   game library.
#
#   @TODO
#   - Add spherical interpolation through the implementation of a 'slerp' function.
#   - Move 'SLACK' to be a constant member of the camera type.

import os
import os.path
import logging
import pygame as PG
from pygame.locals import *

### Global Variables ###

## General Game Information Variables ##

##  The name of the game, which will appear in various debugging strings and
#   views.
GAME_NAME = "Zol"

## Game Model Variables ##

##  The number of frames per second tha the game will attempt to achieve while
#   running.
FRAMES_PER_SECOND = 60

##  Amount of movement that the camera will not follow comparable to slack 
#   in a rope pulling along the camera.
SLACK = 0

## Game View Variables ##

##  The default dimensions of the screen to which the game will be rendered
#   (given in number of pixels).
SCREEN_DIMS = ( 640, 480 )

##  The dimensions of the tiles that comprise the game world in number of pixels.
TILE_DIMS = ( 20, 20 )

## File System/Path Information Variables ##

##  The base path of the project expressed in terms of its absolute path
#   information.
PROJECT_PATH = os.path.dirname( os.path.dirname(__file__) )

##  The path to the assets folder for the game, which contains all assets 
#   associated with the game.
ASSET_PATH = os.path.join( PROJECT_PATH, "assets" )

##  The path to the graphical content used for the game, which contains all
#   image assets for the game.
GRAPHICS_PATH = os.path.join( ASSET_PATH, "graphics" )


### Global Functions ###

##  Loads the image specified by the file name in the first parameter.
#   
#   @param file_name The name of the image file to be loaded.
#   @param color_key The color that will be turned omitted in the final image. 
#       This parameter is useful when parts of the rectangular image aren't needed.
#   @return The image, which can be drawn to the screen.
def load_image( file_name, color_key=None ):
    file_path = os.path.join( ASSET_PATH, "graphics", file_name )

    if not os.path.isfile( file_path ):
        logging.warning( "Image file '%s' does not exist." % file_name )
        file_path = os.path.join( ASSET_PATH, "graphics", "default.png" )

    try:
        if (color_key != None and color_key.a == 0):
            image = PG.image.load( file_path ).convert_alpha()
        else:
            image = PG.image.load( file_path ).convert()
    except PG.error, message:
        logging.error( "Could not load image file at '%s'... failed with error '%s'." %
            (file_path, message) )
        raise SystemExit

    if color_key != None:
        image.set_colorkey( color_key, RLEACCEL )

    return image

##  Restricts the given value to the range defined by the 2nd and 3rd method 
#   parameters.  That is, the first parameter value will be restricted to the 2nd
#   parameter value if the former is smaller and restricted to the 3rd parameter
#   if it is larger.
#
#   @param value The value to be clamped to the range defined by the second and 
#       third parameter values.
#   @param lower_bound The lower bound for the range to which the first parameter 
#       will be restricted.
#   @param upper_bound The upper bound for the range to which the first parameter 
#       will be restricted.
#   @return A new value that lives within the range defined by the minimum and 
#       maximum parameter values.
def clamp( value, lower_bound, upper_bound ):
    assert lower_bound <= upper_bound, "Clamp lower bound must be < upper bound!"

    if value < lower_bound:
        return lower_bound
    elif value > upper_bound:
        return upper_bound
    else:
        return value

##  Linearly interpolates between the values given in the first two parameters 
#   based on the value given in the final parameter.
#   
#   @param initial The starting value for the interpolation.
#   @param final The ending value for the interpolation.
#   @param delta The current position for the interpolation (represented as a 
#       floating-point value between 0 and 1).
#   @return A value that is in between the two given values based on the current time.
def lerp( initial, final, delta ):
    assert 0.0 <= delta and delta <= 1.0, "Interpolation delta factor out of range [0, 1]!"

    return initial * (1 - delta) + final * delta

##  Quadratic easing in and out between two values based on the time delta
#   Based on code from http://www.gizma.com/easing/
#   
#   @param initial The starting value for the interpolation.
#   @param final The ending value for the interpolation.
#   @param delta The current position for the interpolation (represented as a 
#       floating-point value between 0 and 1).
#   @return A value that is in between the two given values based on the current time.
def ease( initial, final, delta ):
    assert 0.0 <= delta and delta <= 1.0, "Interpolation delta factor out of range [0, 1]!"
    delta = delta*2.0
    change = final - initial
    if(delta < 1):
        return change/2.0*delta*delta + initial
    delta = delta-1
    return -change/2.0 * (delta*(delta-2) - 1) + initial

