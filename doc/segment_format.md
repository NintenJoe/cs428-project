## This is the specification for the format of segment files ##

Segments are two dimensional grids of tiles that the player occupies
and explores. To store these segments we will save them as GIF files.

This has the following benefits:

 - Easy to create. Segments can be quickly created in Photoshop, GIMP, etc.
 - Provides a visual preview of the segment.
 - Small file sizes. GIF files use indexing to represent a small palette of
   colors efficiently. Segments of size 100x100 should be less than 1kB.

Each pixel in the image will represent a tile. We are free to choose how each
color is interpreted. I will define a simple format that we could use. The
Segment class will use this format, but it can easily be changed.

 - Black (#000000)
 	This will represent a solid wall.

 - White (#FFFFFF)
 	This will represent the ground.

 - Red (#FF0000)
 	This will represent the entry point for a Level. There should only be one
 	entry point in a set of connected segments (a Level).

 - Gray (#XXX)
 	This will represent a transition to another tile of the same shade of gray.
 	There should be exactly two tiles of a specific shade of gray in a Level.

Other game world entities such as enemies, items, obstacles, etc. can be represented
by specific colors. Those colors will be specified later.




Segment file names will follow the form:

	X.Y.gif

where X is the level number the segment belongs to
and   Y is the segment id number for that level.

For example, if the first level has three segments they would be named:

	1.1.gif
	1.2.gif
	1.3.gif




Each level will have an additional file associated with it named:

	X.tiles

where X is the level number.

This file will contain pairs of colors and tile names in the format:

#RRGGBBAA:X