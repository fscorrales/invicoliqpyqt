import sys

from invicoliqpyqt.model.factureros import ModelFactureros
from invicoliqpyqt.view.form_facturero_app import FormFacturero
from invicoliqpyqt.view.main_window import Ui_main_window
from invicoliqpyqt.view.table_factureros_app import TableFactureros
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QMdiSubWindow


# Inherit from QMainWindow
class MainWindow(QMainWindow):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        
        # Set up ui
        self.ui = Ui_main_window()
        self.ui.setupUi(self)

        #Initialize Model
        self.model_factureros = ModelFactureros(self)

        # Add Menu Triggers
        self.ui.mnu_add_facturero.triggered.connect(lambda: self.show_add_facturero())
        self.ui.mnu_listado_factureros.triggered.connect(lambda: self.show_listado_factureros())
    
    def show_add_facturero(self):
        # Open second window
        self.window_add_facturero = FormFacturero(self.model_factureros.model)
        self.window_add_facturero.show()

    def show_listado_factureros(self):
        sub = QMdiSubWindow()
		# Set The Titlebar or the Sub Window
        # sub.setWindowTitle("Subby Window")
        sub.setWidget(TableFactureros(self.model_factureros.model))
        sub.setAttribute(Qt.WA_DeleteOnClose, True)
        sub.resize(450, 500)
        sub.setWindowFlags(Qt.CustomizeWindowHint | 
        Qt.WindowCloseButtonHint | 
        Qt.WindowMinimizeButtonHint)
		# Add The Sub Window Into Our MDI Widget
        self.ui.mdi_area.addSubWindow(sub)

		# Show the new sub window
        sub.show()
        # Cascade them
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    UIWindow = MainWindow()
    app.exec_()
