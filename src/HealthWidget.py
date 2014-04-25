##  @file HealthWidget.py
#   @author Joseph Ciurej
#   @date Spring 2014
#
#   Source File for the "HealthWidget" Type
#
#   @TODO
#   High Priority:
#   - Add more extensive padding options to the module (currently using static
#     padding amount of 5).
#   Low Priority:
#   - Determine whether the `HealthWidget` should be more tightly coupled
#     with the `GameView` (sharing rendering surfaces).
#   - Determine whether the `HealthWidget` or the `GameView` should be
#     responsible for rendering the `Entity` objects health.
#       > Current Decision: The `GameView` is responsible to telling the
#         `HealthWidget` what to render (`HealthWidget` independent of `Entity`).
#   - Merge the images loaded in this class into the `GameView` type so that
#     image loading is centralized instead of distributed.
#   - Refine the default values for the constructor's render volume to be
#     proportional to the screen size instead of static values.

import os.path
import copy
import pygame as PG
from pygame.locals import *

import Globals

##  The representation of a user interface widget that's used in order to display
#   the health (i.e. hit points) of a particular in-game object.
class HealthWidget( object ):
    ### Constructors ###

    ##  Constructs a health widget instance, setting this instance to render its
    #   contents to the given location in screen space.
    #
    #   @param widget_space The rectangular space to which the widget's contents
    #    will be rendered (with coordinates in screen space).
    def __init__( self, widget_space=PG.Rect( 10, 10, 90, 30 ) ):
        self._render_space = copy.deepcopy( widget_space )
        self._widget_surface = PG.Surface(
            (self._render_space.w, self._render_space.h),
            PG.locals.SRCALPHA
        )

        self._health_icon = PG.transform.scale(
            Globals.load_image( "ui/health-icon.png", PG.Color(255, 0, 255) ),
            ( int((self._render_space.w-(4+1)*5)/4), int((self._render_space.h-2*5)) )
        )

    ### Methods ###

    ##  Renders the contents of the health widget with the given health amount
    #   on top of the given viewport.
    #
    #   @param view_surface The viewport surface that will be rendered to.
    #   @param health_amount The integer amount of health points to be rendered.
    def render_to( self, view_surface, health_amount ):
        # Set Up Widget Surface #
        self._widget_surface.fill( (255, 255, 255, 255) )

        for health_idx in range( health_amount ):
            health_icon_x = 5 + health_idx * ( self._health_icon.get_width() + 5 )
            health_icon_y = 5
            self._widget_surface.blit(
                self._health_icon,
                ( health_icon_x, health_icon_y )
            )

        # Render Widget Surface #
        view_surface.blit(
            self._widget_surface,
            self._render_space.topleft
        )

