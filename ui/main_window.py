# ui/main_window.py

from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QTabWidget, QLabel
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from ui.tabs.hls import HLSTab
import sys, os

def resource_path(relative_path):
    """ Devuelve la ruta absoluta del archivo, compatible con PyInstaller """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
        return os.path.abspath(relative_path)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Protocol Control")
        self.setWindowIcon(QIcon(resource_path("icono.ico")))
        self.setMinimumSize(800, 600)

        self.tabs = QTabWidget()
        
        self.tabs.addTab(HLSTab(), "HLS")
        self.tabs.addTab(self._create_placeholder_tab("DASH"), "DASH")

        self.setCentralWidget(self.tabs)

    def _create_placeholder_tab(self, name):
        widget = QWidget()
        layout = QVBoxLayout()
        label = QLabel(f"{name} not yet implemented.")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        widget.setLayout(layout)
        return widget
