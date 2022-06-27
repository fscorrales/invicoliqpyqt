import sys
import os
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QDialog, QLabel
from PyQt5.QtGui import QPixmap
from invicoliqpyqt.utils.logger import log

# Inherit from QWidget
class AddFacturero(QDialog):
    def __init__(self, parent = None):
        super(AddFacturero, self).__init__(parent)
        # Load the ui file
        uic.loadUi(os.path.join(os.path.dirname(__file__), 'add_facturero.ui'), self)
        # Define Our Widgets
        # self.table_factureros = self.findChild(QTableView, 'table_factureros')
        # self.btn_add = self.findChild(QPushButton, 'btn_add')
        # self.btn_edit = self.findChild(QPushButton, 'btn_edit')
        # self.btn_del = self.findChild(QPushButton, 'btn_del')
        self.lbl_img = self.findChild(QLabel, 'lbl_img')
        self.setFixedSize(500, 300)

		# Open The Image
        parent_dir = os.path.dirname
        self.fname = os.path.join(parent_dir(parent_dir(__file__)), 
        'static/images/form_factureros_agregar.jpg')
        self.pixmap = QPixmap(self.fname)
        # Add Pic to label
        self.lbl_img.setScaledContents(True)
        self.lbl_img.setPixmap(self.pixmap)

        #Set slot connection
        # self.btn_del.pressed.connect(self.delete)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    UIWindow = AddFacturero()
    app.exec_()