import os
import sys

from invicoliqpyqt.view.form_facturero_app import FormFacturero
from invicoliqpyqt.view.table_factureros_app import TableFactureros
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QMdiArea, QMdiSubWindow

from invicoliqpyqt.view.table_factureros_app import TableFactureros


# Inherit from QMainWindow
class MainWindow(QMainWindow):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        # Load the ui file
        uic.loadUi(os.path.join(os.path.dirname(__file__), 'main_window.ui'), self)
        # Define Our Widgets
        self.mdi = self.findChild(QMdiArea, "mdiArea")
        
        # Add Menu Triggers
        self.mnu_add_facturero.triggered.connect(lambda: self.show_add_facturero())
        self.mnu_listado_factureros.triggered.connect(lambda: self.show_listado_factureros())
    
    def show_add_facturero(self):
        # Open second window
        self.window_add_facturero = FormFacturero()
        self.window_add_facturero.show()

    def show_listado_factureros(self):
        sub = QMdiSubWindow()
		# Set The Titlebar or the Sub Window
        # sub.setWindowTitle("Subby Window")
        sub.setWidget(TableFactureros())
        sub.setAttribute(Qt.WA_DeleteOnClose, True)
        sub.resize(450, 500)
        sub.setWindowFlags(Qt.CustomizeWindowHint | 
        Qt.WindowCloseButtonHint | 
        Qt.WindowMinimizeButtonHint)
		# Add The Sub Window Into Our MDI Widget
        self.mdi.addSubWindow(sub)

		# Show the new sub window
        sub.show()
        # Cascade them
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    UIWindow = MainWindow()
    app.exec_()
