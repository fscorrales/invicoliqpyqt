import sys

from invicoliqpyqt.view.table_siif import Ui_table_siif
from PyQt5.QtWidgets import QApplication, QWidget


# Inherit from QMainWindow
class TableSIIF(QWidget):
    def __init__(self, model, parent = None):
        super(TableSIIF, self).__init__(parent)
        
        # Set up ui
        self.ui = Ui_table_siif()
        self.ui.setupUi(self)

        #Set up model
        self.model = model

        #Connect view with model
        self.ui.table_comprobantes.setModel(self.model)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    UIWindow = TableSIIF()
    app.exec_()
