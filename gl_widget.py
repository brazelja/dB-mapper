import math

from PyQt5.QtCore import pyqtSignal, QPoint, QSize, Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QOpenGLWidget, QSlider, QWidget

import OpenGL.GL as gl
import OpenGL.GLU as glu
import OpenGL.GLUT as glut
import numpy as np

from fileloader import *
from raytracing.raytracer import RayTracer
from formulas.geometric_formulas import volume, surface_area, calc_center
from geometry.vec3 import Vec3


class GLWidget(QOpenGLWidget):
    x_rotation_changed = pyqtSignal(int)
    y_rotation_changed = pyqtSignal(int)
    z_rotation_changed = pyqtSignal(int)
    x_position_changed = pyqtSignal(int)
    y_position_changed = pyqtSignal(int)
    zoom_degree_changed = pyqtSignal(int)

    def __init__(self, parent=None, filename=""):
        super().__init__(parent)

        self.filename = filename
        self.object = None
        self.object_volume = 0
        self.object_surface_area = 0
        self.object_center = Vec3(0, 0, 0)
        self.raytracer = 0
        self.rays = None
        self.x_rot = 0
        self.y_rot = 0
        self.z_rot = 0
        self.x_pos = 0
        self.y_pos = 0
        self.zoom = -5.0
        self.sound_source = None

        self.last_pos = QPoint()

        self.color_black = QColor.fromRgb(0, 0, 0)
        self.color_white = QColor.fromRgb(255, 255, 255)

    def set_x_rotation(self, angle):
        """
        Sets the X rotation of the model.
        """
        angle = self.normalize_angle(angle)
        if angle != self.x_rot:
            self.x_rot = angle
            self.x_rotation_changed.emit(angle)
            self.update()

    def set_y_rotation(self, angle):
        """
        Sets the Y rotation of the model.
        """
        angle = self.normalize_angle(angle)
        if angle != self.y_rot:
            self.y_rot = angle
            self.y_rotation_changed.emit(angle)
            self.update()

    def set_z_rotation(self, angle):
        """
        Sets the Z rotation of the model.
        """
        angle = self.normalize_angle(angle)
        if angle != self.z_rot:
            self.z_rot = angle
            self.z_rotation_changed.emit(angle)
            self.update()

    def set_x_position(self, units):
        """
        Sets the X position of the camera.
        """
        if units != self.x_pos:
            self.x_pos = units
            self.x_position_changed.emit(units)
            self.update()

    def set_y_position(self, units):
        """
        Sets the Y position of the camera.
        """
        if units != self.y_pos:
            self.y_pos = units
            self.y_position_changed.emit(units)
            self.update()

    def set_zoom(self, angle):
        """
        Sets the zoom factor of the camera.
        """
        if angle < 0:
            angle = self.object_center.z * 0.2
        else:
            angle = -self.object_center.z * 0.2
        self.zoom += angle
        self.zoom_degree_changed.emit(angle)
        self.update()

    def set_sound_source(self, x, y, z):
        """
        Sets the visual position of the sound source.
        """
        self.sound_source = Vec3(x, y, z)
        self.update()

    def load_model(self, filename):
        """
        Loads the specified file and generates the corresponding model.
        """
        self.filename = filename
        self.obj_file = ObjLoader(filename)
        self.object_vertices = self.obj_file.vertices
        self.object_faces = self.obj_file.faces

        # Calculate object geometric properties
        self.object_volume = volume(self.object_vertices, self.object_faces)
        self.object_surface_area = surface_area(self.object_faces)
        self.object_center = calc_center(self.object_vertices, self.object_faces)

        self.x_pos = -self.object_center.x
        self.y_pos = -self.object_center.y
        self.zoom = -self.object_center.z * 10
        self.sound_source = Vec3(*self.object_center)
        self.object = self.obj_file.render()
        self.update()

    def refresh_model(self, material_view):
        """
        Refreshes the model to show any material or view changes.
        """
        self.object = self.obj_file.render(material_view)
        self.update()

    def initializeGL(self):
        """
        OpenGL Lifecycle method. Do not change name. 
        """
        self.set_clear_color(self.color_white)
        self.set_color(self.color_black)

        gl.glShadeModel(gl.GL_FLAT)
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        gl.glEnable(gl.GL_BLEND)

    def paintGL(self):
        """
        OpenGL Lifecycle method. Do not change name. 
        """
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glLoadIdentity()

        # Centers on the model
        gl.glTranslate(self.x_pos, self.y_pos, self.zoom)

        # Rotates model around its center
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glPushMatrix()
        gl.glTranslate(self.object_center.x, self.object_center.y, self.object_center.z)

        gl.glRotated(self.x_rot / 16.0, 1.0, 0.0, 0.0)
        gl.glRotated(self.y_rot / 16.0, 0.0, 1.0, 0.0)
        gl.glRotated(self.z_rot / 16.0, 0.0, 0.0, 1.0)

        gl.glTranslate(
            -self.object_center.x, -self.object_center.y, -self.object_center.z
        )

        if self.object is not None:
            gl.glCallList(self.object)
        if self.sound_source is not None:
            gl.glPointSize(10)
            gl.glBegin(gl.GL_POINTS)
            gl.glColor3f(1.0, 0, 0)
            gl.glVertex3fv(self.sound_source.vec)
            gl.glEnd()
        if self.rays is not None:
            gl.glCallList(self.rays)

        gl.glPopMatrix()

    def resizeGL(self, width, height):
        """
        OpenGL Lifecycle method. Do not change name. 
        """
        side = min(width, height)
        if side < 0:
            return

        gl.glViewport(0, 0, side, side)

        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        glu.gluPerspective(45.0, float(width) / float(height), 0.1, 100000.0)
        gl.glMatrixMode(gl.GL_MODELVIEW)

    def run_raytracer(self, start_db=120, freq=1000, reflections=0):
        """
        Runs the raytracing algorithm to generate the decibel map of the model.
        """
        self.raytracer = RayTracer(
            self.sound_source, 1000, self.obj_file.faces, start_db, freq, reflections
        )
        self.rays = self.raytracer.render()
        self.update()

    def mousePressEvent(self, event):
        """
        Records where the mouse was clicked.
        """
        self.last_pos = event.pos()

    def mouseMoveEvent(self, event):
        """
        Records what mouse buttons were clicked when it moves.
        """
        dx = event.x() - self.last_pos.x()
        dy = event.y() - self.last_pos.y()

        modifiers = QApplication.keyboardModifiers()

        # Drag to move object
        # Shift + Drag to rotate object
        if event.buttons() & Qt.LeftButton and modifiers == Qt.ShiftModifier:
            self.set_x_rotation(self.x_rot + 8 * dy)
            self.set_y_rotation(self.y_rot + 8 * dx)
        elif event.buttons() & Qt.LeftButton:
            self.set_x_position(self.x_pos + dx / 100)
            self.set_y_position(self.y_pos - dy / 100)
        elif event.buttons() & Qt.RightButton and modifiers == Qt.ShiftModifier:
            self.set_x_rotation(self.x_rot + 8 * dy)
            self.set_z_rotation(self.z_rot + 8 * dx)

        self.last_pos = event.pos()

    def wheelEvent(self, event):
        """
        Records what how much the mouse wheel was moved.
        """
        # Use the mouse wheel to zoom in/out
        self.last_pos = event.pos()
        d = -float(event.angleDelta().y())
        self.set_zoom(d)

    def normalize_angle(self, angle):
        """
        Normalizes the angle the mouse wheel turns.
        """
        while angle < 0:
            angle += 360 * 16
        while angle > 360 * 16:
            angle -= 360 * 16
        return angle

    def set_clear_color(self, c):
        """
        Sets the clear color of the scene.
        """
        gl.glClearColor(c.redF(), c.greenF(), c.blueF(), c.alphaF())

    def set_color(self, c):
        """
        Sets the color set of the scene.
        """
        gl.glColor4f(c.redF(), c.greenF(), c.blueF(), c.alphaF())
