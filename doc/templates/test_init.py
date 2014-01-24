##	@file __init__.py
#	@author Joseph Ciurej
#	@date Winter 2014
#
#	Initialization Script for the Game Library Tests
#
#	@TODO
#	- Find a more elegant means of importing all classes/functions from the src 
#	  'module' so that they can be accessed by the tests.


### Initialization Imports ###

import os, sys


### Initialization Logic ###

# Adds the 'src' directory to the directory search path for the Python interpreter.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
