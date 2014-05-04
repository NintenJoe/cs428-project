import unittest
import src
import pygame as pg

from src.Globals import *
from src.Camera import *

class CameraTests(unittest.TestCase):

    def setUp(self):
        self.move_tgt = PG.Rect(500, 500, 1, 1)
        self.area = (1,1)

        self.border = PG.Rect(0, 0, 6400, 4800)

        self.shift_time = 3000
        accumulated_shift = 0
        self.camera = Camera( self.move_tgt, self.area, self.shift_time, PG.Rect(0,0,0,0), 4)
        self.camera.set_border(self.border)

    def tearDown(self):
        pass

    def testCameraConstructor(self):
        self.assertEquals(self.camera.focus, self.move_tgt,
            "Camera does not focus on the move target given")
        self.assertEquals(self.border, self.camera.border,
            "Camera does not set border correctly")
        self.assertEquals(self.camera.shift_time, self.shift_time,
            "Camera does not set shift time correctly")
        self.assertEquals(self.camera.get_position()[0], 500,
            "Camera does not set position correctly")
        self.assertEquals(self.camera.get_position()[1], 500,
            "Camera does not set position correctly")

    def testOffset(self):
        self.camera.set_offset(5, 6)
        self.assertEquals(self.camera.offset[0], 5,
            "Camera does not set offset correctly")
        self.assertEquals(self.camera.offset[1], 6,
            "Camera does not set offset correctly")
        self.camera.update(1)
        self.assertEquals(self.camera.position[0], 505,
            "Camera does not apply offset correctly")
        self.assertEquals(self.camera.position[1], 506,
            "Camera does not apply offset correctly")
        self.camera.update(2)
        self.assertEquals(self.camera.position[0], 505,
            "Camera applies offset more than once")
        self.assertEquals(self.camera.position[1], 506,
            "Camera applies offset more than once")

    def testMovement(self):
        self.move_tgt.left = 460
        self.move_tgt.top = 501
        self.camera.update(1)
        self.assertEquals(self.camera.position[0], 464,
            "Camera does not apply movement correctly")
        self.assertEquals(self.camera.position[1], 500,
            "Camera does not apply movement correctly")
        self.camera.update(2)
        self.assertEquals(self.camera.position[0], 464,
            "Camera applies movement more than once")
        self.assertEquals(self.camera.position[1], 500,
            "Camera applies movement more than once")

    def testMovementWithOffset(self):
        self.camera.set_offset(5,6)
        self.move_tgt.left = 460
        self.move_tgt.top = 501
        self.camera.update(1)
        self.assertEquals(self.camera.position[0], 469,
            "Camera does not apply movement correctly with offsets")
        self.assertEquals(self.camera.position[1], 506,
            "Camera does not apply movement correctly with offsets")
        self.move_tgt.left = 468
        self.move_tgt.top = 508
        self.camera.update(2)
        self.assertEquals(self.camera.position[0], 469,
            "Camera does not apply movement correctly with offsets")
        self.assertEquals(self.camera.position[1], 510,
            "Camera does not apply movement correctly with offsets")

    def testFocusTransition(self):
        new_focus = PG.Rect(550, 550, 1, 1)
        self.camera.set_target(0, new_focus)
        self.assertEquals(new_focus, self.camera.focus,
            "Camera does not set focus correctly")
        self.camera.update(0)
        self.assertEquals(self.camera.position[0], 500,
            "Camera focus does not transition correctly")
        self.assertEquals(self.camera.position[1], 500,
            "Camera focus does not transition correctly")
        self.camera.update(1500)
        self.assertEquals(self.camera.position[0], 525,
            "Camera focus does not transition correctly")
        self.assertEquals(self.camera.position[1], 525,
            "Camera focus does not transition correctly")
        self.camera.update(349802)
        self.assertEquals(self.camera.position[0], 550,
            "Camera focus does not transition correctly")
        self.assertEquals(self.camera.position[1], 550,
            "Camera focus does not transition correctly")

    def testBorderClamp(self):
        self.move_tgt.left = -50
        self.move_tgt.top = 40
        self.camera.update(1)
        self.assertEquals(self.camera.position[0], 0,
            "Camera does not clamp correctly")
        self.assertEquals(self.camera.position[1], 44,
            "Camera does not clamp correctly")
        self.move_tgt.left = 50
        self.move_tgt.top = -40
        self.camera.update(2)
        self.assertEquals(self.camera.position[0], 46,
            "Camera does not clamp correctly")
        self.assertEquals(self.camera.position[1], 0,
            "Camera does not clamp correctly")

    def testViewPort(self):
        self.assertEquals(self.camera.get_viewport().width, 1,
            "Camera viewport not set correctly")
        self.assertEquals(self.camera.get_viewport().height, 1,
            "Camera viewport not set correctly")
        self.assertEquals(self.camera.get_viewport().x, 500,
            "Camera viewport not set correctly")
        self.assertEquals(self.camera.get_viewport().y, 500,
            "Camera viewport not set correctly")
