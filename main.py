# main.py

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from ui.main_window import MainWindow
from database.db import init_db
import sys

if __name__ == "__main__":
    init_db() 

    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icono.ico"))
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
