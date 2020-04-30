from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QAction, QMenuBar, QFileDialog


class MenuBar(QMenuBar):
    open = pyqtSignal(str)
    save = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.app = parent
        self.add_file_tab()
        self.add_edit_tab()
        self.add_view_tab()

    def add_file_tab(self):
        """
        Adds File tab to menu
        """
        file_tab = self.addMenu("File")
        # Open
        open_action = QAction("Open", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file)
        file_tab.addAction(open_action)
        # Export
        export_action = QAction("Export...", self)
        export_action.setShortcut("Ctrl+E")
        export_action.triggered.connect(self.save_file)
        file_tab.addAction(export_action)

    def add_edit_tab(self):
        """
        Adds Edit tab to menu
        """
        edit_tab = self.addMenu("Edit")
        # Undo
        undo_action = QAction("Undo", self)
        undo_action.setShortcut("Ctrl+Z")
        edit_tab.addAction(undo_action)
        # Redo
        redo_action = QAction("Redo", self)
        redo_action.setShortcut("Ctrl+Y")
        edit_tab.addAction(redo_action)

    ### Unimplemented ###
    def add_view_tab(self):
        """
        Adds View tab to menu
        """
        view_tab = self.addMenu("View")
        # Appearance
        appearance_subtab = view_tab.addMenu("Appearance")
        # Fullscreen
        fullscreen_action = QAction("Fullscreen", self)
        fullscreen_action.setShortcut("F11")
        appearance_subtab.addAction(fullscreen_action)
        # Show Sidebar
        view_sidebar_action = QAction("View sidebar", self, checkable=True)
        view_sidebar_action.setChecked(True)
        appearance_subtab.addAction(view_sidebar_action)

    @pyqtSlot()
    def open_file(self):
        """
        Opens the file dialog for the user to select an input file
        """
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getOpenFileName(
            self, "Open File", "", "3D Files (*.obj)", options=options
        )

        if filename:
            self.open.emit(filename)

    @pyqtSlot()
    def save_file(self):
        """
        Opens the file dialog for the user to select a file to save to
        """
        if self.app.model_loaded:
            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            filename, _ = QFileDialog.getSaveFileName(
                self, "Save File", "", "Images (*.png *.xpm *.jpg)", options=options
            )
            self.save.emit(filename)
