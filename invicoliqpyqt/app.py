import sys
from PyQt5.QtWidgets import QApplication
from invicoliqpyqt.view.main_window import MainWindow
from invicoliqpyqt.db.conexion import Conexion


app = QApplication(sys.argv)
with Conexion() as db:
    UIWindow = MainWindow()
    UIWindow.show()
    app.exec_()