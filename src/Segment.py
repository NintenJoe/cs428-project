##	@file
#	Module file for the "Segment" type, which serves as the backdrop to the game
#	world.

# Pygame Imports #
import pygame as PG

# IO Imports #
import struct
from os.path import join as join_paths

# Game Library Imports #
from Globals import *

##	A representation of a portion of the game world, which is composed of a 
#	matrix of tiles.  A segment instance handles all the assets associated with
#	the background and provides collision information for the game world.
#
#	@note The file structure for segment instances is as follows:
#		Location: /data/segdata
#		Extension: .seg
#		Format:	Data Item							|		Number of Bytes
#			Number of Outgoing Segment References	|		2
#			List of Outgoing Segment References
#				X-Coordinate of Reference 			|		2
#				Y-Coordinate of Reference 			|		2
#				ID of Outgoing Segment Reference	|		2
#				X-Coordinate of Outgoing Entry Point|		2
#				Y-Coordinate of Outgoing Entry Point|		2
#			Width of Current Segment 				|		2
#			Height of Current Segment 				|		2
#			List of Columns of Tiles (Column-Major Storage of Tiles!)
#				List of Tiles
#					Tile Identifier					|		2
class Segment():
	# Constructors #

	##	Constructs a segment based on a segment ID and an entry point coordinate.
	#	
	#	@param segment_id The identification number of the segment to be constructed.
	#	@param entry_point The coordinate within the current segment at which the 
	#		player should be placed (defaults to the origin coordinate) (given in
	#		terms of tile coordinates).
	def __init__(self, segment_id, entry_point=(0, 0)):
		# Identifier for the current segment.
		self.id = segment_id
		# The point at which the segment was entered by the player.
		self.entry_point = entry_point

		# A listing of all segments referenced by the current segment, stored
		# as a dictionary of the following form: 
		# { (x_of_ref, y_of_ref ) => ( dest_id, ( dest_x, dest_y ) ) }
		self.segment_references = {}
		# A matrix containing all the tile information for the segment where
		# 'tile_matrix[x][y]' returns the tile at position (x, y). 
		self.tile_matrix = []
		# The width of the tile matrix (in number of tiles).
		self.width = -1
		# The height of the tile matrix (in number of tiles).
		self.height = -1

		# Tracks unique tiles loaded for the segment instance, which is reprenseted 
		# as a dictionary of the form { tile_id => texture }.
		self.tile_list = {}

		self._load_segment(segment_id, entry_point)

	# Methods #

	##	Retrieves the image information regarding the segment and returns it as
	#	a pygame surface.
	#	
	#	@note The dimensions of the individual tiles of the segment are determined
	#	by the uniform dimensions of the tile images associated with the game
	#	project that utilizes the code.  This may cause slowdowns for very high
	#	resolution textures.
	#	
	#	@return A pygame surface that conatins all the image information loaded into
	#	the segment currently.
	def get_image(self):
		tile_tex = self.tile_list[ self.tile_matrix[0][0] ]
		tile_dims = tile_tex.get_rect()

		seg_image = PG.Surface( 
			(tile_dims.width * self.width, tile_dims.height * self.height), 
			tile_tex.get_flags(), tile_tex.get_bitsize(), tile_tex.get_masks() 
		)

		for x in range( 0, self.width ):
			for y in range( 0, self.height ):
				seg_image.blit( self.tile_list[ self.tile_matrix[x][y] ],
					( x * tile_dims.width, y * tile_dims.height ) )

		return seg_image

	##	Retrieves the collision map associated with the segment, which includes
	#	all of the collision information for the segment (i.e. collision information
	#	with the background).
	#	
	#	@return A two-dimensional Boolean array in column-major order that contains
	#	collision information.  If a cell at 'collisionmap[x][y]' is true, then
	#	the segment cell is solid.
	def get_collisionmap(self):
		collisionmap = []

		for x in range( 0, self.width ):
			collision_column = []
			
			for y in range( 0, self.height ):
				collision_column.append( self._tile_tangible(x, y) )

			collisionmap.append( collision_column )

		return collisionmap

	# Helper Functions #

	##	Loads a segment specified by the first parameter from a file stored on 
	#	the hard disk into the current segment instance.
	#
	#	@param segment_id The identification number of the segment to be constructed.
	#	@param entry_point The coordinate within the current segment at which the 
	#		player should be placed (defaults to the origin coordinate).
	def _load_segment(self, segment_id, entry_point):
		segment_file = open(join_paths(ASSET_PATH, "data", "segdata", 
			"%i.seg" % segment_id), "r")

		segment_ref_count = struct.unpack('H', segment_file.read(2))[0]

		for i in range(0, segment_ref_count):
			ref_x_pos = struct.unpack('H', segment_file.read(2))[0]
			ref_y_pos = struct.unpack('H', segment_file.read(2))[0]

			ref_segment_id = struct.unpack('H', segment_file.read(2))[0]
			ref_entry_point_x = struct.unpack('H', segment_file.read(2))[0]
			ref_entry_point_y = struct.unpack('H', segment_file.read(2))[0]

			# Hash the reference based on the coordinates to allow for quick 
			# access when checking for collisions with the segment changing tiles.
			self.segment_references[(ref_x_pos, ref_y_pos)] = (ref_segment_id, 
				(ref_entry_point_x, ref_entry_point_y))

		self.width = struct.unpack('H', segment_file.read(2))[0]
		self.height = struct.unpack('H', segment_file.read(2))[0]

		for x in range(0, self.width):
			tile_column = []

			for y in range(0, self.height):
				tile_id = struct.unpack('H', segment_file.read(2))[0]
				
				# If the current tile ID is not contained on this segment's list
				# of tiles, add an entry to the list of new tiels to prevent
				# redundant tile loading.
				if not self.tile_list.has_key(tile_id):
					self.tile_list[tile_id] = True
		
				tile_column.append(tile_id)

			self.tile_matrix.append(tile_column)

		# Load all tile asset information.
		self._load_tile_info()

	##	A helper loading function that loads all necessary assets based on tile
	#	information loaded for the segment.
	#
	#	@todo There's room here to perform multiple passes over the current
	#	terrain and load textures based on the adjacency of tile types.
	def _load_tile_info(self):
		for tile_id in self.tile_list.keys():
			self.tile_list[tile_id] = load_image(join_paths("tiles", "%i.bmp" % tile_id))

	##	Given the coordinates of a tile within the segment, this function indicates
	#	whether the tile at that location is tangible.
	#	
	#	@todo The current tile tangibility determinant is a bit hacky, but its
	#	efficient.  Because tiles are being stored as integers I don't see a much
	#	better way of partitioning the space to allow for lots of both types.
	#	Tiles with even identiers are tangible while tiles with odd identifiers
	#	are intangible.
	#	
	#	@param x The x-coordinate of the tile that will be tested for tangibility.
	#	@param y The y-coordinate of the tile that will be tested for tangibility.
	#	@return True if the tile is tangible (should cause collisions) and false
	#		otherwise.
	def _tile_tangible(self, x, y):
		return self.tile_matrix[x][y] % 2 == 0
