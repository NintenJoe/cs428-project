##	@file Camera.py
#	@author Joseph Ciurej
#	@date Fall 2012 (Updated Winter 2014)
#
#	Module file for the "Camera" Type
#
#	@TODO
#	High Priority:
#	- Clean up the comments within this file, especially the in-line comments.
#	- Reformat the comments so that they follow the new style guidelines (triple
#	  punctuation on class areas, etc.).
#	- Enforce an 80-character limit on the code contained within this file.
#	- Stop camera before it runs off the world's borders
#	- Implement smooth camera transitions
#	- Implement offset
#	- Implement zooming
#	Low Priority:
#	- Fix the problems associated with fixed to free camera transitioning.

from pygame.locals import *
from Globals import lerp

##	Blueprint class for a camera that exists within a two-dimensional world.  
#	The camera has the ability to target a particular entity within the game world 
#	and follow that objects movements.
class Camera():
	# Constructors #

	##	Constructs a camera through which the player may observe the game world.
	#	Optionally, a  target can be marked for the camera to follow and a 
	#	shifting time for target changes can be specified.
	#	
	#	@param target The game world object that will be followed by the camera 
	#		(often the in-game avatar for the player).
	#	@param shift_time The amount of time the camera takes to switch between targets.
	#	@param border The current segment to which the camera is attached
	def __init__(self, target=None, shift_time=1000, border=None):
		self.prev_focal_position = None
		self.focus = target
		self.offset = [0,0]
		self.segment = border

		self.shift_time = float(shift_time)
		self.shift_start_time = -1

		self.position = [ 0, 0 ] if self.focus == None else [ self.focus.rect.centerx, self.focus.rect.centery ]

	# Methods #

	##	Retrieves the current focal position for the camera, returning this value
	#	as a tuple of the form (xPos, yPos).
	#	
	#	@return A tuple that contains the positioning information for the camera
	#	of the form (xPos, yPos).
	def get_position(self):
		return self.position

	##	Offsets the position of the camera by the given amount.  This offset will
	#	last until it is set back to 0, 0
	#	
	#	@todo Units of the shift?
	#	
	#	@param x_shift The horizontal shift to be applied to the camera.
	#	@param y_shift The vertical shift to be applied to the camera.
	def set_offset(self, x_shift, y_shift):
		self.offset[0] = x_shift
		self.offset[1] = y_shift

	##  Sets the new segment when moving the camera from one segment
	#	to another. Since this happens on the border of segments, 
	#	there needs to be some transition logic as well.
	#	
	#	@todo transition logic
	#
	#	@param new_segment The segment which the camera is moving into
	def set_segment(self, new_segment):
		self.segment = new_segment

	##	Establishes a new target for the camera to follow with a new offset.  
	#	The camera will  adjust so that the target given will be located in the 
	#	center of its viewpoint (with a given offset).  Setting the target to
	#	'None' will cause the camera to remain stationary.
	#
	#	@param game_time The time at which the new target is set relative to the
	#		starting time of the game (measured in milliseconds).
	#	@param new_target The object which the camera will follow (default none).
	def set_target(self, game_time, new_target=None):
		self.shift_start_time = game_time

		# Update occurs between the center points of the foci.
		self.prev_focal_position = ( self.position[0], self.position[1] )
		self.focus = new_target

	##	Updates the positioning of the camera given the current game time.
	#	
	#	@param game_time The time at which the new target is set relative to the
	#		starting time of the game (measured in milliseconds).
	def update(self, game_time):
		# Track targets, perform interpolation.
		if self.focus != None:
			if self.prev_focal_position != None:
				assert self.shift_start_time >= 0, "Multiple targets assigned to camera without shift time."

				delta = (game_time - self.shift_start_time) / self.shift_time
				# If the change hasn't reached the final value, then calculate 
				# the camera position based on linear interpolation between 
				# the targets.
				if delta < 1:
					self.position[0] = lerp(self.prev_focal_position[0],
						self.focus.rect.centerx, delta)
					self.position[1] = lerp(self.prev_focal_position[1],
						self.focus.rect.centery, delta)
				# Otherwise, if the delta indicates that the transition is over, 
				# set the camera's position to the position of the current target
				# and stop the transitioning.
				else:
					self.position[0] = self.focus.rect.centerx
					self.position[1] = self.focus.rect.centery

					self.prev_focal_position = None
					self.shift_start_time = -1
			# If the camera is attached to one target, simply follow that target
			# with the camera.
			else:
				self.position[0] = self.focus.rect.centerx
				self.position[1] = self.focus.rect.centery

		self.position[0] = int( self.position[0] + self.offset[0] )
		self.position[1] = int( self.position[1] + self.offset[1] )
