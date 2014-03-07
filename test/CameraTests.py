import unittest
import src
import pygame as pg

from src.Globals import *
from src.Camera import *
from pygame.locals import *


class CameraTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pg.init()
        pg.display.set_mode((640,480))

    @classmethod
    def tearDownClass(self):
        pg.quit()

    def setUp(self):
        self.move_tgt = PG.Rect(500, 500, 1, 1)

        self.border = PG.Rect(0, 0, 6400, 4800)

        self.shift_time = 3000
        accumulated_shift = 0
        self.camera = Camera( self.move_tgt, self.shift_time, self.border, 4)

    def tearDown(self):
        pass

    def testCameraConstructor(self):
        self.assertEquals(self.camera.focus, self.move_tgt)
        self.assertEquals(self.border, self.camera.border)
        self.assertEquals(self.camera.shift_time, self.shift_time)
        self.assertEquals(self.camera.position[0], 500)
        self.assertEquals(self.camera.position[1], 500)

    def testOffset(self):
        self.camera.set_offset(5, 6)
        self.assertEquals(self.camera.offset[0], 5)
        self.assertEquals(self.camera.offset[1], 6)
        self.camera.update(1)
        self.assertEquals(self.camera.position[0], 505)
        self.assertEquals(self.camera.position[1], 506)
        #This looks redundant, but it checks if offset is applied more than once
        self.camera.update(2)
        self.assertEquals(self.camera.position[0], 505)
        self.assertEquals(self.camera.position[1], 506)

    def testMovement(self):
        self.move_tgt.left = 460
        self.move_tgt.top = 501
        self.camera.update(1)
        self.assertEquals(self.camera.position[0], 464)
        self.assertEquals(self.camera.position[1], 500)
        #Movement is not accumulative
        self.camera.update(2)
        self.assertEquals(self.camera.position[0], 464)
        self.assertEquals(self.camera.position[1], 500)

    def testMovementWithOffset(self):
        self.camera.set_offset(5,6)
        self.move_tgt.left = 460
        self.move_tgt.top = 501
        self.camera.update(1)
        self.assertEquals(self.camera.position[0], 469)
        self.assertEquals(self.camera.position[1], 506)
        self.move_tgt.left = 468
        self.move_tgt.top = 508
        self.camera.update(2)
        self.assertEquals(self.camera.position[0], 469)
        self.assertEquals(self.camera.position[1], 510)

    def testFocusTransition(self):
        new_focus = PG.Rect(550, 550, 1, 1)
        self.camera.set_target(0, new_focus)
        self.assertEquals(new_focus, self.camera.focus)
        self.camera.update(0)
        self.assertEquals(self.camera.position[0], 500)
        self.assertEquals(self.camera.position[1], 500)
        self.camera.update(1500)
        self.assertEquals(self.camera.position[0], 525)
        self.assertEquals(self.camera.position[1], 525)
        self.camera.update(349802)
        self.assertEquals(self.camera.position[0], 550)
        self.assertEquals(self.camera.position[1], 550)

    def testBorderClamp(self):
        self.move_tgt.left = -50
        self.move_tgt.top = 40
        self.camera.update(1)
        self.assertEquals(self.camera.position[0], 0)
        self.assertEquals(self.camera.position[1], 44)
        self.move_tgt.left = 50
        self.move_tgt.top = -40
        self.camera.update(2)
        self.assertEquals(self.camera.position[0], 46)
        self.assertEquals(self.camera.position[1], 0)