import sys
import os
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QMdiArea, QMdiSubWindow
from invicoliqpyqt.view.listado_factureros import ListadoFactureros

# Inherit from QMainWindow
class MainWindow(QMainWindow):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        # Load the ui file
        uic.loadUi(os.path.join(os.path.dirname(__file__), 'main_window.ui'), self)
        # Define Our Widgets
        self.mdi = self.findChild(QMdiArea, "mdiArea")
        # Add Menu Triggers
        self.mnu_listado_factureros.triggered.connect(lambda: self.show_listado_factureros())
    
    def show_listado_factureros(self):
        sub = QMdiSubWindow()
		# Set The Titlebar or the Sub Window
        # sub.setWindowTitle("Subby Window")
        sub.setWidget(ListadoFactureros())
        sub.setAttribute(Qt.WA_DeleteOnClose)
        sub.resize(450, 500)
        sub.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
		# Add The Sub Window Into Our MDI Widget
        self.mdi.addSubWindow(sub)

		# Show the new sub window
        sub.show()
        # Cascade them
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    UIWindow = MainWindow()
    app.exec_()