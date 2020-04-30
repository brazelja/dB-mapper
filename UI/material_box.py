from PyQt5.Qt import Qt, pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import (
    QCheckBox,
    QComboBox,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
)

import numpy as np

from geometry.materials import Materials as mtl


class MaterialBox(QGroupBox):
    update_view = pyqtSignal(bool)

    def __init__(self, str, parent=None):
        super().__init__(str)
        layout = QVBoxLayout()
        layout.setSpacing(10)

        self.surface_dropdown = self.create_surface_dropdown()
        self.material_dropdown = self.create_material_dropdown()
        self.set_material_changer(layout)
        self.sabine_table = self.create_sabine_table(freq=1000)
        layout.addWidget(self.sabine_table)
        self.create_material_view(layout)
        self.material_view = False
        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.setLayout(layout)

    def create_surface_dropdown(self, model_faces=None):
        """
        Populates the surfaces dropdown
        """
        self.model_faces = model_faces

        surfaces = QComboBox()

        if model_faces is not None:
            for i, face in enumerate(model_faces):
                if np.array_equal(face.normal.vec, [0.0, 1.0, 0.0]):
                    faceStr = "Ceiling [" + str(i) + "]"
                elif np.array_equal(face.normal.vec, [0.0, -1.0, 0.0]):
                    faceStr = "Floor [" + str(i) + "]"
                else:
                    faceStr = "Wall [" + str(i) + "]"
                surfaces.addItem(faceStr, face)
            surfaces.addItem("All", None)
            surfaces.model().sort(0)

        return surfaces

    def create_material_dropdown(self):
        """
        Populates the material dropdown
        """
        materials = QComboBox()

        materials.addItem("Hardwood", mtl.HARDWOOD)
        materials.addItem("Carpet", mtl.CARPET)
        materials.addItem("Drywall", mtl.DRYWALL)
        materials.addItem("Brick", mtl.BRICK)
        materials.addItem("Concrete", mtl.CONCRETE)
        materials.addItem("Foam", mtl.FOAM)

        return materials

    def set_material_changer(self, layout):
        """
        Creates the material changer section of the Material Box.
        """
        surface_label = QLabel("Surface")
        surface_label.setAlignment(Qt.AlignLeft)
        material_label = QLabel("Material")
        material_label.setAlignment(Qt.AlignLeft)

        set_material_btn = QPushButton("Set Material")
        set_material_btn.setToolTip("Set material for chosen surface")
        set_material_btn.clicked.connect(
            lambda: self.set_material(
                self.surface_dropdown.itemData(self.surface_dropdown.currentIndex()),
                self.material_dropdown.itemData(self.material_dropdown.currentIndex()),
            )
        )

        self.material_changer_layout = QGridLayout()
        self.material_changer_layout.addWidget(surface_label, 0, 0, 1, 1)
        self.material_changer_layout.addWidget(material_label, 0, 1, 1, 1)
        self.material_changer_layout.addWidget(self.surface_dropdown, 1, 0, 1, 1)
        self.material_changer_layout.addWidget(self.material_dropdown, 1, 1, 1, 1)
        self.material_changer_layout.addWidget(set_material_btn, 2, 0, 1, 2)

        layout.addLayout(self.material_changer_layout)

    def create_sabine_table(self, freq) -> QTableWidget:
        """
        Creates the Sabine absorption coefficient reference table for 
        the current frequency
        """
        sabine_table = QTableWidget()
        sabine_table.setRowCount(6)
        sabine_table.setColumnCount(2)
        sabine_table.setHorizontalHeaderLabels(["Material", "Absorption"])

        materials = [
            mtl.HARDWOOD,
            mtl.CARPET,
            mtl.DRYWALL,
            mtl.BRICK,
            mtl.CONCRETE,
            mtl.FOAM,
        ]

        for i, m in enumerate(materials):
            sabine_table.setItem(i, 0, QTableWidgetItem(mtl.name(m)))
            a = QTableWidgetItem(str(mtl.absorption(m, freq)))
            a.setTextAlignment(Qt.AlignCenter)
            sabine_table.setItem(i, 1, a)

        return sabine_table

    def create_material_view(self, layout):
        """
        Creates the checkbox that toggles the material view.
        """
        material_view_label = QLabel("Material View")
        material_view_label.setAlignment(Qt.AlignLeft)

        material_view_checkbox = QCheckBox()
        material_view_checkbox.stateChanged.connect(self.change_material_view)

        material_view_layout = QHBoxLayout()
        material_view_layout.addWidget(material_view_label)
        material_view_layout.addWidget(material_view_checkbox)

        layout.addLayout(material_view_layout)

    def update_material_box(self, model_faces, freq):
        """
        Updates the surface dropdown for the current model.
        """
        new_surface_dropdown = self.create_surface_dropdown(model_faces)
        self.material_changer_layout.replaceWidget(
            self.surface_dropdown, new_surface_dropdown
        )
        self.surface_dropdown.close()
        self.surface_dropdown = new_surface_dropdown

        # Update model based on current status of material view option
        self.update_view.emit(self.material_view)

    def update_freq(self, freq):
        """
        Updates the sabine table based on the current frequency.
        """
        new_sabine_table = self.create_sabine_table(freq)
        self.layout().replaceWidget(self.sabine_table, new_sabine_table)
        self.sabine_table.close()
        self.sabine_table = new_sabine_table

    @pyqtSlot()
    def set_material(self, face, mtl):
        """
        Changes the material of the specified face.
        """
        if face is None:
            for face in self.model_faces:
                face.material = mtl
        else:
            face.material = mtl
        self.update_view.emit(self.material_view)

    @pyqtSlot(int)
    def change_material_view(self, state):
        """
        Toggles the status of the material view option.
        """
        status = state == Qt.Checked
        self.material_view = status
        self.update_view.emit(status)
