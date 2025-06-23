from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from ui.main_window import MainWindow
from database.db import init_db
import sys
import os

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.abspath(relative_path)

def adb_path():
    return resource_path(os.path.join("utils", "adb.exe"))

if __name__ == "__main__":
    init_db()

    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(resource_path("icono.ico")))
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
