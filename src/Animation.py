##	@file
#	Module file for the "Animation" type, which represents game animations.
#       @authors Joseph Ciurej / Edwin Chan

# Pygame Imports #
import pygame as PG
from pygame.locals import *

# Game Library Imports #
from Globals import load_image
from Globals import clamp

##	Blueprint class for standard game animations.  Specialized derivatives of 
#	the "Sprite" class may contain several different animation instances and 
#	cycle between them based on state.
class Animation(object):
	# Constructors #

	##	Constructs an animation from a sprite sheet file given the amount of time 
	#	per frame and the width of each frame in the sprite sheet.
	#	
	#	@param filename A string that points to the file in the "assets/graphics/" 
	#		file folder that conatins the sprite sheet for the given animation.
	#	@param frame_count The total number of frames contained within the 
	#		animation depicted by the given sprite sheet (default value 1).
	#	@param frame_time The amount of time that each frame will play before 
	#		the next frame is shown (in milliseconds) (default value 33 milliseconds).
	#	@param is_looping A boolean value that indicates whether or not the animation
	#		represented should loop or not (default value false).
	def __init__(self, filename, frame_count=1, frame_time=33, is_looping=False):

                self.sprite_sheet = load_image(filename, (255, 0, 255))		
                sheet_rect = self.sprite_sheet.get_rect()

                self.sheet_path = filename
                self.frame_width = int(sheet_rect.width / frame_count)
                self.frame_height = sheet_rect.height
                self.frame_time = frame_time
                self.frame_count = frame_count
                self.is_looping = is_looping

                # Initializes the starting time for the animation to a negative value to 
                # track bugs related to animations that are polled for frames but that
                # haven't been queued to start.
                self.start_time = -1


	# Methods #

	##      Returns the uploaded image
	#
	
        def get_full_image(self):
                return self.sprite_sheet

	##      Loads a specific sprite from the spritesheet
	#
        #       @param rectangle The coordinates of the 4 corners of the sprite rectangle in
        #       the sprite sheet. i.e. (X, Y, width, height)
        #

        def get_image_at(self, rectangle):
                rect = PG.Rect(rectangle)
                img = PG.Surface(rect.size).convert()
                img.blit(self.sprite_sheet, (0,0), rect)
                return img

        ##      Loads several specific sprite from the spritesheet and puts them into a list
	#
        #       @param rectangles The coordinates of the 4 corners of the sprite rectangle in
        #       the sprite sheet. i.e. (X, Y, width, height)
        #

        def get_images_at(self, rectangles):
                return [self.get_image_at(rect) for rect in rectangles]
        
	##	Starts the animation at the given time (which should be measured in 
	#	milliseconds since the game started up).
	#
	#	@param game_time The time relative to the start of the game at which the
	#		the animation is queued to start.
	def start(self, game_time):
		self.start_time = game_time

	##	Retrieves the frame for the given update period based on the given time 
	#	(which should be given in terms of milliseconds since the game started up).
	#	
	#	@param game_time The time at which the frame is being retrieved (in terms
	#		of milliseconds since the game started).
	#	@return A reference to the image that represents the current frame for 
	#		the animation.
	def get_frame(self, game_time):
		assert self.start_time >= 0, "Animation '%s' not started before frame retrieval." % self.sheet_path

		frame_num = _get_frame_number(game_time)
		frame_rect = PG.Rect(frame_num * self.frame_width, 0, self.frame_width, self.frame_height)

		return self.sprite_sheet.subsurface(frame_rect)

	##	A courtesy function that resets the timer for an animation instance.  
	#	This function should be called whenever an animation should stop playing.
	def end(self):
		self.start_time = -1

	# Helper Functions #

	##	Returns the number for the current frame given the current game time,
	#	which can be used to position the subsurface for the current frame.
	#	
	#	@param game_time The time at which the frame is being retrieved (in terms
	#		of milliseconds since the game started).
	#	@return A number that uniquely identifies the current frame that will be
	#		displayed in the animation.
	def _get_frame_number(self, game_time):
		frame_num = int((game_time - self.start_time) / self.frame_time)

		if self.is_looping:
			frame_num = frame_num % self.frame_count
		else:
			frame_num = clamp(frame_num, 0, self.frame_count - 1)

		return frame_num
