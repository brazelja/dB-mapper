import sys

from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import (
    QSizePolicy,
    QGridLayout,
    QTabWidget,
    QWidget,
    QApplication,
    QMainWindow,
    QLineEdit,
)

import numpy as np
import webbrowser

from UI.menu_bar import MenuBar
from UI.opengl_box import OpenGLBox
from UI.statistics_box import StatBox
from UI.material_box import MaterialBox


class App(QMainWindow):
    windowResized = pyqtSignal(int, int)
    windowMoved = pyqtSignal(int, int)

    def __init__(self):
        super().__init__()
        self.title = "dB-mapper"
        self.left = 50
        self.top = 30
        self.width = 1400
        self.height = 900
        self.model_loaded = False
        self.minSizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.freq = 1000
        self.reflection = 0
        self.material_view = False
        self.initUI()

    def initUI(self):
        """
        Sets up the UI elements of the application.
        """
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # self.createMenuBar()
        self.menu_bar = MenuBar(parent=self)
        self.setMenuBar(self.menu_bar)
        self.menu_bar.open.connect(self.load_model)
        self.menu_bar.save.connect(self.save_model)
        # self.createOpenGLBox()
        self.opengl_box = OpenGLBox("Modelview")
        # self.createStatBox()
        self.stat_box = StatBox("Acoustic Calculations", parent=self)
        self.stat_box.update_sound_source.connect(self.update_sound_source)
        self.stat_box.update_freq.connect(self.update_freq)
        self.stat_box.calc_db_map.connect(self.calc_db_map)
        self.stat_box.calc_rt60.connect(self.calc_rt60)
        self.stat_box.calc_crit_dist.connect(self.calc_crit_dist)
        # self.createTreatmentBox()
        self.material_box = MaterialBox("Materials")
        self.material_box.update_view.connect(self.update_view)

        mainLayout = QGridLayout()
        mainLayout.addWidget(self.opengl_box, 0, 0, 2, 2)

        tabs = QTabWidget()
        tabs.setTabPosition(QTabWidget.East)
        tabs.addTab(self.stat_box, "Statistics")
        tabs.addTab(self.material_box, "Materials")
        tabs.setSizePolicy(self.minSizePolicy)

        mainLayout.addWidget(tabs, 0, 2, 2, 1)

        widget = QWidget()
        widget.setLayout(mainLayout)
        self.setCentralWidget(widget)

        self.statusBar().showMessage("v1.0.0")
        self.show()

    def resizeEvent(self, event):
        """
        Qt Event\n
        Triggers when the window is resized.
        """
        w = event.size().width()
        h = event.size().height()

        self.width = w
        self.height = h

        self.windowResized.emit(w, h)

    def moveEvent(self, event):
        """
        Qt Event\n
        Triggers when the window is moved.
        """
        l = event.pos().x()
        t = event.pos().y()

        self.left = l
        self.top = t

        self.windowMoved.emit(l, t)

    @pyqtSlot(str)
    def load_model(self, filename):
        """
        Signaled when a file is selected to be loaded.
        """
        self.opengl_box.load_model(filename)
        model_faces = self.opengl_box.get_model_faces()
        self.material_box.update_material_box(model_faces, self.freq)
        self.model_loaded = True

    @pyqtSlot(str)
    def save_model(self, filename):
        """
        Signaled when a file is selected to have the current 
        frame buffer saved to.
        """
        if self.model_loaded:
            self.opengl_box.save_frame_buffer(filename)

    @pyqtSlot(list)
    def update_stat_box(self, model_center: list):
        """
        TODO\n
        Update the statbox fields when a model is loaded. 
        i.e. setting sound source fields to object center coordinates.
        """
        pass

    @pyqtSlot(float, float, float)
    def update_sound_source(self, x: float, y: float, z: float):
        """
        Signaled when the sound source fields are updated.
        """
        self.opengl_box.update_sound_source(x, y, z)

    @pyqtSlot(int)
    def update_freq(self, freq: int):
        """
        Signaled when the frequency field is updated.
        """
        self.freq = freq
        self.material_box.update_freq(freq)

    @pyqtSlot(int, int)
    def calc_db_map(self, start_db: int, r_num: int):
        """
        Signaled when the calculate button is clicked to render the 
        decibel map of the model.
        """
        self.opengl_box.calc_db_map(start_db, self.freq, r_num)

    @pyqtSlot(QLineEdit)
    def calc_rt60(self, out):
        """
        Signaled when the calculate button is clicked to determine 
        the RT60 value of the model.
        """
        reverb = self.opengl_box.calc_rt60()
        out.setText(str(np.round(reverb, 3)))

    @pyqtSlot(QLineEdit)
    def calc_crit_dist(self, out):
        """
        Signaled when the calculate button is clicked to determine 
        the Critical Distance value of the model.
        """
        crit_dist = self.opengl_box.calc_crit_dist()
        out.setText(str(np.round(crit_dist, 3)))

    @pyqtSlot(bool)
    def update_view(self, material_view):
        """
        Signaled when a surface has its material changed or the 
        material view checkbox is clicked.
        """
        self.opengl_box.update_view(material_view)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
