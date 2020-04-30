from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import (
    QGroupBox,
    QLabel,
    QLineEdit,
    QPushButton,
    QGridLayout,
    QVBoxLayout,
    QComboBox,
    QSizePolicy,
    QMessageBox,
    QSpacerItem,
)
from PyQt5.QtGui import QValidator, QDoubleValidator, QIntValidator

import webbrowser
import numpy as np


class StatBox(QGroupBox):
    update_sound_source = pyqtSignal(float, float, float)
    update_freq = pyqtSignal(int)
    calc_db_map = pyqtSignal(int, int)
    calc_rt60 = pyqtSignal(QLineEdit)
    calc_crit_dist = pyqtSignal(QLineEdit)

    def __init__(self, str, parent=None):
        super().__init__(str, parent)
        self.app = parent
        self.min_size_policy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.start_db = 120
        self.reflection = 0
        self.freq = 1000

        layout = QVBoxLayout()
        layout.setSpacing(10)
        self.add_sound_source(layout)
        self.add_db_map(layout)
        self.add_reverb(layout)
        self.add_crit_dist(layout)
        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.setLayout(layout)

    def add_sound_source(self, layout: QVBoxLayout) -> QGridLayout:
        """
        Adds Sound Source component to the Statistics Box
        """
        sound_source_label = QLabel("Sound Source")
        sound_source_label.setAlignment(Qt.AlignLeft)

        # X Coordinate
        sound_source_x_label = QLabel("X:")
        sound_source_x_label.setAlignment(Qt.AlignRight)
        sound_source_x = QLineEdit()
        # sound_source_x.setValidator(QDoubleValidator())
        sound_source_x.setSizePolicy(self.min_size_policy)
        sound_source_x.setAlignment(Qt.AlignCenter)
        # Y Coordinate
        sound_source_y_label = QLabel("Y:")
        sound_source_y_label.setAlignment(Qt.AlignRight)
        sound_source_y = QLineEdit()
        # sound_source_y.setValidator(QDoubleValidator())
        sound_source_y.setSizePolicy(self.min_size_policy)
        sound_source_y.setAlignment(Qt.AlignCenter)
        # Z Coordinate
        sound_source_z_label = QLabel("Z:")
        sound_source_z_label.setAlignment(Qt.AlignRight)
        sound_source_z = QLineEdit()
        # sound_source_z.setValidator(QDoubleValidator())
        sound_source_z.setSizePolicy(self.min_size_policy)
        sound_source_z.setAlignment(Qt.AlignCenter)

        # Sound Source "Set" Button
        sound_source_set_btn = QPushButton("Set")
        sound_source_set_btn.setToolTip("Sets sound source coordinates")
        sound_source_set_btn.clicked.connect(
            lambda: self.set_sound_source(
                sound_source_x, sound_source_y, sound_source_z
            )
        )

        sound_source_layout = QGridLayout()
        sound_source_layout.setContentsMargins(20, 0, 20, 0)
        sound_source_layout.setSpacing(20)
        sound_source_layout.addWidget(sound_source_x_label, 0, 0, 1, 1)
        sound_source_layout.addWidget(sound_source_x, 0, 1, 1, 1)
        sound_source_layout.addWidget(sound_source_y_label, 1, 0, 1, 1)
        sound_source_layout.addWidget(sound_source_y, 1, 1, 1, 1)
        sound_source_layout.addWidget(sound_source_z_label, 2, 0, 1, 1)
        sound_source_layout.addWidget(sound_source_z, 2, 1, 1, 1)
        sound_source_layout.addWidget(sound_source_set_btn, 0, 3, 3, 2)

        layout.addWidget(sound_source_label)
        layout.addLayout(sound_source_layout)

    def add_db_map(self, layout: QVBoxLayout) -> QGridLayout:
        """
        Adds Decibel Map component to Statistics Box
        """
        # Decibel Map
        db_map_label = QLabel("Generate Decibel Map")
        db_map_label.setAlignment(Qt.AlignLeft)
        # dBMapLabel.setFont(QFont("Arial", 16))

        # Starting Decibel Input
        start_db_label = QLabel("Starting Decibel Level")
        start_db_label.setAlignment(Qt.AlignLeft)

        start_db = QLineEdit()
        start_db.setText("120")
        # start_db.setValidator(QIntValidator(0, 120))
        start_db.setSizePolicy(self.min_size_policy)
        start_db.setAlignment(Qt.AlignCenter)
        start_db.setToolTip("In range 0-120")
        start_db.textChanged.connect(lambda: self.set_start_db(start_db))

        # Frequency Select
        freq_select_label = QLabel("Frequency")
        freq_select_label.setAlignment(Qt.AlignLeft)

        freq_select = QComboBox()
        freq_select.addItems(["125", "250", "500", "1000", "2000", "4000"])
        freq_select.setCurrentText("1000")
        freq_select.currentTextChanged.connect(self.set_freq)

        # Reflections
        reflection_select_label = QLabel("Reflections")
        reflection_select_label.setAlignment(Qt.AlignLeft)

        reflection_select = QComboBox()
        reflection_select.addItems(["0", "1", "2"])
        reflection_select.setCurrentText("0")
        reflection_select.currentTextChanged.connect(self.set_reflection)

        db_map_btn = QPushButton("Calculate")
        db_map_btn.setToolTip("Generates Decibel Map")
        db_map_btn.clicked.connect(self.dB_map)

        db_map_info_btn = QPushButton("View Details")
        db_map_info_btn.setToolTip("View details of the Decibel Map calculation")
        db_map_info_btn.clicked.connect(self.decibel_info)

        db_map_btn_layout = QGridLayout()
        db_map_btn_layout.setContentsMargins(20, 0, 20, 0)
        db_map_btn_layout.setSpacing(20)
        db_map_btn_layout.addWidget(start_db_label, 0, 0, 1, 1)
        db_map_btn_layout.addWidget(start_db, 0, 1, 1, 1)
        db_map_btn_layout.addWidget(freq_select_label, 1, 0, 1, 1)
        db_map_btn_layout.addWidget(freq_select, 1, 1, 1, 1)
        db_map_btn_layout.addWidget(reflection_select_label, 2, 0, 1, 1)
        db_map_btn_layout.addWidget(reflection_select, 2, 1, 1, 1)
        db_map_btn_layout.addWidget(db_map_btn, 3, 0, 1, 1)
        db_map_btn_layout.addWidget(db_map_info_btn, 3, 1, 1, 1)

        layout.addWidget(db_map_label)
        layout.addLayout(db_map_btn_layout)

    def add_reverb(self, layout: QVBoxLayout) -> QGridLayout:
        """
        Add reverberation time component to Stat box.
        """
        reverb_label = QLabel("Reverberation Time")
        reverb_label.setAlignment(Qt.AlignLeft)

        reverb_output = QLineEdit()
        reverb_output.setAlignment(Qt.AlignCenter)
        reverb_output.setReadOnly(True)

        reverb_calc_btn = QPushButton("Calculate")
        reverb_calc_btn.setToolTip("Calculate Reverberation Time")
        reverb_calc_btn.clicked.connect(lambda: self.calculate_rt60(reverb_output))

        reverb_info_btn = QPushButton("View Details")
        reverb_info_btn.setToolTip("View details of the Reverberation Time calculation")
        reverb_info_btn.clicked.connect(self.rt60_info)

        reverb_btn_layout = QGridLayout()
        reverb_btn_layout.setContentsMargins(20, 0, 20, 0)
        reverb_btn_layout.setSpacing(20)
        reverb_btn_layout.addWidget(reverb_output, 0, 1, 1, 2)
        reverb_btn_layout.addWidget(reverb_calc_btn, 1, 0, 1, 2)
        reverb_btn_layout.addWidget(reverb_info_btn, 1, 2, 1, 2)

        layout.addWidget(reverb_label)
        layout.addLayout(reverb_btn_layout)

    def add_crit_dist(self, layout: QVBoxLayout) -> QGridLayout:
        """
        Add critical distance component to Stat box.
        """
        crit_dist_label = QLabel("Critical Distance")
        crit_dist_label.setAlignment(Qt.AlignLeft)

        crit_dist_output = QLineEdit()
        crit_dist_output.setAlignment(Qt.AlignCenter)
        crit_dist_output.setReadOnly(True)

        crit_dist_calc_btn = QPushButton("Calculate")
        crit_dist_calc_btn.setToolTip("Calculate Critical Distance")
        crit_dist_calc_btn.clicked.connect(
            lambda: self.calculate_crit_dist(crit_dist_output)
        )

        crit_dist_info_btn = QPushButton("View Details")
        crit_dist_info_btn.setToolTip(
            "View details of the Critical Distance calculation"
        )
        crit_dist_info_btn.clicked.connect(self.crit_dist_info)

        crit_dist_btn_layout = QGridLayout()
        crit_dist_btn_layout.setContentsMargins(20, 0, 20, 0)
        crit_dist_btn_layout.setSpacing(20)
        crit_dist_btn_layout.addWidget(crit_dist_output, 0, 1, 1, 2)
        crit_dist_btn_layout.addWidget(crit_dist_calc_btn, 1, 0, 1, 2)
        crit_dist_btn_layout.addWidget(crit_dist_info_btn, 1, 2, 1, 2)

        layout.addWidget(crit_dist_label)
        layout.addLayout(crit_dist_btn_layout)

    @pyqtSlot()
    def set_sound_source(self, x_in: QLineEdit, y_in: QLineEdit, z_in: QLineEdit):
        """
        Validates then set the location of the sound source in the model.
        """
        if self.app.model_loaded:
            x, y, z = 0, 0, 0
            validator = QDoubleValidator()
            x_state, _, _ = validator.validate(x_in.text(), 0)
            y_state, _, _ = validator.validate(y_in.text(), 0)
            z_state, _, _ = validator.validate(z_in.text(), 0)

            if x_state == QValidator.Acceptable:
                x = float(x_in.text())
            else:
                x_in.setText("0.0")

            if y_state == QValidator.Acceptable:
                y = float(y_in.text())
            else:
                y_in.setText("0.0")

            if z_state == QValidator.Acceptable:
                z = float(z_in.text())
            else:
                z_in.setText("0.0")
            self.update_sound_source.emit(x, y, z)

    @pyqtSlot(str)
    def set_freq(self, freq_str: str):
        """
        Sets the frequency to use when calculating the decibel map of the model.
        """
        self.freq = int(freq_str)
        self.update_freq.emit(self.freq)

    @pyqtSlot(str)
    def set_start_db(self, input: QLineEdit):
        """
        Sets the starting decibel level to use when calculating the decibel map of the model.
        """
        state, _, _ = QIntValidator(0, 120).validate(input.text(), 0)
        if state == QValidator.Acceptable:
            self.start_db = int(input.text())
        else:
            input.setText("0")

    @pyqtSlot(str)
    def set_reflection(self, reflection_str: str):
        """
        Sets the number of reflections to use when calculating the decibel map of the model.
        """
        self.reflection = int(reflection_str)

    @pyqtSlot()
    def dB_map(self):
        """
        Calculates the decibel map of the object.
        """
        if self.app.model_loaded:
            messageBox = QMessageBox(self)
            messageBox.setWindowTitle("Generate dB Map")
            messageBox.setIcon(QMessageBox.Question)
            messageBox.setText(
                "<p>Do you want to generate the decibel map for this room?</p>"
                "<p><i>This may take some time</i></p>"
            )
            messageBox.addButton(QPushButton("No"), QMessageBox.NoRole)
            messageBox.addButton(QPushButton("Yes"), QMessageBox.YesRole)

            buttonReply = messageBox.exec()

            if buttonReply == 1:  # Yes
                self.calc_db_map.emit(self.start_db, self.reflection)

    @pyqtSlot()
    def decibel_info(self):
        """
        Opens a modal containing information about decibels and the process of how
        the decibel map is calculated.
        """
        infoBox = QMessageBox(self)
        infoBox.setWindowTitle("Decibel Map Information")
        infoBox.setIcon(QMessageBox.Information)
        infoBox.setText(
            """
            <head>
            <style>
            .color-box {
                width: 10px;
                height: 10px;
                display: inline-block;
                background-color: #ccc;
            }
            </style>
            </head>
            <p>Sound pressure level is measured in decibels (dB) which are the objective measurement of how ‘loud’ 
            a sound is at a given distance from the sound’s source. Decibels operate on a logarithmic scale of base 
            10 that aligns very closely with way the human ear percieves sound levels.</p>
            <p>Interesting properties of sound pressure level in decibels include:</p>
            <ul>
            <li>Doubling the listener's distance from the sound source results in a change of -6 dB</li>
            <li>Halving the listener's distace from the sound source results in a change of +6 dB</li>
            </ul>
            <p>The formula for finding the decibel level of a sound source at a new distance r<sub>2</sub> is:</p>
            <p><strong>L<sub>2</sub> = L<sub>1</sub> + 20log(r<sub>2</sub>/r<sub>1</sub>)</p>
            <p>L<sub>1</sub> = the sound pressure level in dB at r<sub>1</sub></p>
            <p>r<sub>2</sub> = the new distance from the sound source</p>
            <p>r<sub>1</sub> = the old distance from the sound source</p>
            <p>The dB-color scale used is:</p>
            <div class="color-box" style="background-color: #ff0000;">120 dB</div>
            <div class="color-box" style="background-color: #ff7f00;">100 dB</div>
            <div class="color-box" style="background-color: #ffff00;">80 dB</div>
            <div class="color-box" style="background-color: #7fff00;">60 dB</div>
            <div class="color-box" style="background-color: #00ff00;">40 dB</div>
            <div class="color-box" style="background-color: #00ff7f;">20 dB</div>
            <div class="color-box" style="background-color: #00ffff;">0 dB</div>
            """
        )
        infoBox.addButton(QPushButton("More Info"), QMessageBox.HelpRole)
        infoBox.addButton(QPushButton("Close"), QMessageBox.RejectRole)
        buttonReply = infoBox.exec()

        if buttonReply == 0:
            webbrowser.open(
                "https://en.wikipedia.org/wiki/Decibel", new=0, autoraise=True
            )

    @pyqtSlot()
    def calculate_rt60(self, out):
        """
        Calculates the RT60 value of the current model.
        """
        if self.app.model_loaded:
            self.calc_rt60.emit(out)

    @pyqtSlot()
    def rt60_info(self):
        """
        Opens a modal containing information about reverberation and the process of how 
        the reverberation time is calculated.
        """
        infoBox = QMessageBox(self)
        infoBox.setWindowTitle("RT60 Information")
        infoBox.setIcon(QMessageBox.Information)
        infoBox.setText(
            """
            <p>Reverberation is the persistence of sound in a room after it is produced and can be easily heard if you make 
            a sound in a large space, like a church, and can hear the sound in the room well after you stopped making it.</p>
            <p>The reverberation of a room is dependent on:</p>
            <ul>
            <li>The frequency band of the sound produced</li>
            <li>The area of the room</li>
            <li>What materials its surfaces are made of and how much sound energy they absorb</li>
            </ul>
            <p>A common objective measurement of reverberation is known as RT60 (Reverberation Time 60dB), which is the measure 
            of how long the sound pressure level of a room takes to drop by 60dB after it was generated.</p>
            <p>The formula used to calcultate the RT60 of a room:</p>
            <p><strong>RT60 = 0.161 * V/A</strong></p>
            <p>V = room volume in m<sup>3</sup></p>
            <p>A = ∑𝑎∗𝑆 where a = the absorption coefficient and S = the surface area in m<sup>2</sup></p>
            """
        )
        infoBox.addButton(QPushButton("More Info"), QMessageBox.HelpRole)
        infoBox.addButton(QPushButton("Close"), QMessageBox.RejectRole)
        buttonReply = infoBox.exec()

        if buttonReply == 0:
            webbrowser.open(
                "https://en.wikipedia.org/wiki/Reverberation", new=0, autoraise=True
            )

    @pyqtSlot()
    def calculate_crit_dist(self, out):
        """
        Calculates the Critical Distance value of the current model.
        """
        if self.app.model_loaded:
            self.calc_crit_dist.emit(out)

    @pyqtSlot()
    def crit_dist_info(self):
        """
        Opens a modal containing information about critical distances and the process of how 
        the critical distance is calculated.
        """
        infoBox = QMessageBox(self)
        infoBox.setWindowTitle("Critical Distance Information")
        infoBox.setIcon(QMessageBox.Information)
        infoBox.setText(
            """
            <p>The critical distance of a room is the point within it where the sound pressure level of the reverberant (reflected) 
            sounds are equal to the sound pressure level directly from the source.</p>
            <p>This ‘sweet spot’ can be found manually if you move around a room while a speaker is playing and can find a spot where 
            the sound is much louder than everywhere around it.</p>
            <p>This location is dependent on the area of the room as well as the makeup of its reflective surfaces and is conveniently 
            calculated with the RT60 value of a room, making it an easy statistic to provide a user if the reverberation time is also being provided.</p>
            <p>The formula used to calcultate the Critical Distance of a room:</p>
            <p><strong>Critical Distance = 0.057 * &radic;(V/RT60)</strong></p>
            <p>V = room volume in m<sup>3</sup></p>
            <p>RT60 = the RT60 measurement for the room</p>
            """
        )
        infoBox.addButton(QPushButton("More Info"), QMessageBox.HelpRole)
        infoBox.addButton(QPushButton("Close"), QMessageBox.RejectRole)
        buttonReply = infoBox.exec()

        if buttonReply == 0:
            webbrowser.open(
                "https://en.wikipedia.org/wiki/Critical_distance", new=0, autoraise=True
            )
