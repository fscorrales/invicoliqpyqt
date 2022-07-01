import os
import sys
from dataclasses import asdict, dataclass

from invicoliqpyqt.utils.logger import log
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QApplication, QDialog, QDialogButtonBox, QLabel,
                             QLineEdit)


@dataclass
class Facturero():
    nombre: str = ''
    estructura: str = ''
    partida: str = ''

class AddFacturero(QDialog):
    def __init__(self, model, parent = None):
        super(AddFacturero, self).__init__(parent)
        self.model_facturero = model
        # Load the ui file
        uic.loadUi(os.path.join(os.path.dirname(__file__), 'add_facturero.ui'), self)
        # Define Our Widgets
        # self.table_factureros = self.findChild(QTableView, 'table_factureros')
        # self.btn_add = self.findChild(QPushButton, 'btn_add')
        # self.btn_edit = self.findChild(QPushButton, 'btn_edit')
        # self.btn_del = self.findChild(QPushButton, 'btn_del')
        self.lbl_img = self.findChild(QLabel, 'lbl_img')
        self.txt_nombre = self.findChild(QLineEdit, 'txt_nombre')
        self.txt_estructura = self.findChild(QLineEdit, 'txt_estructura')
        self.txt_partida = self.findChild(QLineEdit, 'txt_partida')
        self.btn_box = self.findChild(QDialogButtonBox, 'btn_box')

		# Open The Image
        parent_dir = os.path.dirname
        self.fname = os.path.join(parent_dir(parent_dir(__file__)), 
        'static/images/form_factureros_agregar.jpg')
        self.pixmap = QPixmap(self.fname)
        #Scale Pic
        self.lbl_img.setScaledContents(True)
        # Add Pic to label
        self.lbl_img.setPixmap(self.pixmap)

        #Set slot connection
        self.btn_box.accepted.connect(self.save)
        # self.btn_del.pressed.connect(self.delete)

        #Set Modal
        self.setModal(True)


    def save(self):
        registro = Facturero(
            self.txt_nombre.text(),
            self.txt_estructura.text(),
            self.txt_partida.text(),
        )
        self.model_facturero.insert_row(asdict(registro))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    UIWindow = AddFacturero()
    app.exec_()
