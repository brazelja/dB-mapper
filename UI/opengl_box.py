from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QGroupBox, QHBoxLayout, QLayout

from gl_widget import GLWidget
from geometry.vec3 import Vec3
from geometry.face import Face
import formulas.db_formulas as db


class OpenGLBox(QGroupBox):
    update_stat_box = pyqtSignal(Vec3)

    def __init__(self, str, parent=None):
        super().__init__(str)
        self.gl_widget = GLWidget()
        layout = QHBoxLayout()
        layout.addWidget(self.gl_widget)
        self.setLayout(layout)

    def load_model(self, filename: str):
        """
        Loads the specified file's model into OpenGL.
        """
        self.gl_widget.load_model(filename)

        self.update_stat_box.emit(self.gl_widget.object_center)

    def get_model_faces(self) -> [Face]:
        return self.gl_widget.object_faces

    def update_sound_source(self, x: float, y: float, z: float):
        """
        Updates the position of the sound source.
        """
        self.gl_widget.set_sound_source(x, y, z)

    def calc_db_map(self, start_db: int, freq: int, r_num: int):
        """
        Runs the raytacing algorithm to calculate the decibel map of the model.
        """
        self.gl_widget.run_raytracer(start_db=start_db, freq=freq, reflections=r_num)

    def calc_rt60(self) -> float:
        """
        Calculates the RT60 value of the model.
        """
        return db.rt60(self.gl_widget.object_volume, self.gl_widget.object_faces,)

    def calc_crit_dist(self) -> float:
        """
        Calculates the Critical Distance value of the model.
        """
        return db.crit_dist(self.gl_widget.object_volume, self.gl_widget.object_faces,)

    def update_view(self, material_view):
        """
        Updates the models materials and if material view is active or not.
        """
        self.gl_widget.refresh_model(material_view)

    def save_frame_buffer(self, filename: str):
        """
        Saves the current frame buffer to the specified file.
        """
        image = self.gl_widget.grabFramebuffer()
        image.save(filename, "PNG")
