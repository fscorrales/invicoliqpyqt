import sys
from PyQt5.QtWidgets import QApplication
from invicoliqpyqt.view.main_window import MainWindow
#from invicoliqpyqt.model.conexion import Conexion


app = QApplication(sys.argv)
#Conexion.obtener_conexion()
UIWindow = MainWindow()
app.exec_()