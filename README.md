# Zol: An Experimental 2D Game Engine #

## Required Software ##
- [Python v2.7.6][py]
- [PyGame v1.9.1][pygame]
- [Doxygen v1.8.6][doxygen] (Documentation generation only)

## Software Resources ##
- [Continuous Integration][travis] [![Build Status](https://travis-ci.org/NintenJoe/zol.png?branch=master)](https://travis-ci.org/NintenJoe/zol)
- [Code Coverage][coveralls] [![Coverage Status](https://coveralls.io/repos/NintenJoe/zol/badge.png?branch=Final-Iteration)](https://coveralls.io/r/NintenJoe/zol?branch=Final-Iteration)

## Installation Instructions ##
* Verify that the required software (e.g. `python` and `pygame`) is installed.
* Checkout the repository from GitHub.
    * `git clone https://github.com/NintenJoe/zol.git`
* Run `./zol` from the top-level `zol` directory.

## Documentation Instructions ##
* View online at [http://jhalstead85.github.io/zol/](http://jhalstead85.github.io/zol/)
* Or generate it locally with the following instructions:
   * Verify that the required software (e.g. `doxygen`) is installed.
   * Run `make docs` from the top-level `zol` directory.
   * Open `zol/doc/htmlindex.html` with your favortie web browser.

## Running Instructions ##
* To run the example game demo, either run the command `./zol` or the command `make main`
  while in the top level project directory.
* To run the tests for the game engine infrastructure code, run the command `make tests`
  while in the top level project directory.

## Credits ##
Project originally developed as a course project for CS428 (Software Engineering II) at
the University of Illinois Urbana-Champaign.

### Authors ###

| Author Name | Author Network ID | Author GitHub ID |
| ----------- | ----------------- | ---------------- |
| Joshua Halstead | halstea2 | jhalstead85 |
| Joseph Ciurej | ciurej2 | NintenJoe |
| Andrew Exo | exo1 | andrewexo |
| Nick Jeffrey | njeffre2 | Mortech |
| Eric Christianson | christ39 | T1g |
| Edwin Chan | chan100 | edchan110 |


[py]: http://www.python.org/download/releases/2.7.6/ 
[pygame]: http://www.pygame.org/install.html
[travis]: https://travis-ci.org/NintenJoe/zol
[coveralls]: https://coveralls.io/r/NintenJoe/zol
[cs428-wiki]: https://wiki.engr.illinois.edu/display/cs428sp14/Zol+(Video+Game)
[doxygen]: http://www.stack.nl/~dimitri/doxygen/
