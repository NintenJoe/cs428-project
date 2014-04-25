##  @file Animation.py
#   @author Joseph Ciurej, Edwin Chan
#   @date Fall 2012 (Updated Winter 2014)
#
#   Module file for the "Animation" Type
#
#   @TODO
#   High Priority:
#   - Change the automated loading strategy to make the specification for
#     frame width easier.
#   - Change the automated loading strategy to make it possible to indicate
#     whether an animation is looping or non-looping.
#   Low Priority:
#   - 

import pygame as PG
from pygame.locals import *
import Globals

##  Blueprint class for standard game animations.  Specialized derivatives of 
#   the "Sprite" class may contain several different animation instances and 
#   cycle between them based on state.
class Animation( object ):
    ### Constructors ###

    ##  Constructs an animation from a sprite sheet file given the amount of time 
    #   per frame and a looping behavior.
    #   
    #   @param filename The path containing the animation sprite sheet file.
    #   @param frame_time The amount of time that each frame will be displayed.
    #   @param is_looping True if the animation should loop, false otherwise.
    def __init__( self, filename, frame_time=33, is_looping=False ):
        self._sheet_surface = Globals.load_image( filename, PG.Color(255, 0, 255) )
        surface_rect = self._sheet_surface.get_rect()

        self._frame_width = self._calc_frame_width( filename )
        self._frame_height = self._calc_frame_height( filename )
        self._frame_count = int( surface_rect.width / self._frame_width )

        self._frame_time = frame_time
        self._looping = is_looping

    ### Methods ###

    ##  Returns the animation frame associated with the given time delta since
    #   the beginning of the first animation frame.
    #   
    #   @param time_delta The amount of time since the beginning of the animation.
    #   @return A reference to the image that represents the current animation frame.
    def get_frame( self, time_delta ):
        frame_num = self._get_frame_number( time_delta )
        frame_rect = PG.Rect(
            frame_num * self._frame_width, 0,
            self._frame_width, self._frame_height
        )

        return self._sheet_surface.subsurface( frame_rect )

    ##  @return A reference to the `Surface` that contains the animation.
    def get_sheet( self ):
        return self._sheet_surface

    ### Helper Functions ###

    ##  Returns the number for the current frame given the current game time,
    #   which can be used to position the subsurface for the current frame.
    #   
    #   @param time_delta The time since the beginning of the animation for
    #    which the frame will be retrieved.
    #   @return The 0-based index of the frame at the time within the animation.
    def _get_frame_number( self, time_delta ):
        frame_num = int( time_delta / self._frame_time )

        if self._looping:
            frame_num = frame_num % self._frame_count
        else:
            frame_num = Globals.clamp( frame_num, 0, self._frame_count - 1 )

        return frame_num

    ##  Detects the frame width of the animation specified by the given filename
    #   by looking for the pixel with alpha=0 on the top bar (indicates the
    #   beginning of the second frame).
    #
    #   @param filename The path to the animation file.
    #   @return The width of the frames of the animation in pixel number.
    def _calc_frame_width( self, filename ):
        sheet_surface = Globals.load_image( filename, PG.Color(0,0,0,0) )

        for x in range( 0, sheet_surface.get_width() ):
            color = sheet_surface.get_at( (x, 0) )

            if (color.a == 0) or (color.r == 255 and color.g == 255 and color.b == 255):
                return x

        return sheet_surface.get_width()

    ##  Detects the frame height of the animation specified by the given filename.
    #
    #   @param filename The path to the animation file.
    #   @return The height of the frames of the animation in pixel number.
    def _calc_frame_height( self, filename ):
        sheet_surface = Globals.load_image( filename, PG.Color(0,0,0,0) )

        return sheet_surface.get_height()

