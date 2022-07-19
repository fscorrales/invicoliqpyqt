import os
import sys
from dataclasses import dataclass

from invicoliqpyqt.utils.logger import log
from invicoliqpyqt.view.form_facturero import Ui_form_facturero
from PyQt5.QtCore import QModelIndex, QRegExp
from PyQt5.QtGui import QPixmap, QRegExpValidator
from PyQt5.QtWidgets import QApplication, QDialog, QDialogButtonBox


@dataclass
class Facturero():
    razon_social: str = ''
    estructura: str = ''
    partida: str = ''

class FormFacturero(QDialog):
    def __init__(self, model, row_edit = None, parent = None):
        super(FormFacturero, self).__init__(parent)
        
        # Set up UI
        self.ui = Ui_form_facturero()
        self.ui.setupUi(self)

        # Set up model
        self.model_facturero = model
        self.row_edit = row_edit

		# Open The Image
        parent_dir = os.path.dirname
        self.fname = os.path.join(parent_dir(parent_dir(__file__)), 
        'static/images/form_facturero_agregar.jpg')
        self.pixmap = QPixmap(self.fname)
        #Scale Pic
        self.ui.lbl_img.setScaledContents(True)
        # Add Pic to label
        self.ui.lbl_img.setPixmap(self.pixmap)

        # Input Mask
        self.ui.txt_estructura.setInputMask('99-99-99-99;_')
        self.ui.txt_partida.setInputMask('999;_')

        # Validator
        self.txt_nombre_validator = QRegExpValidator(QRegExp('\w+'), self.ui.txt_nombre)
        self.ui.txt_nombre.setValidator(self.txt_nombre_validator)

        # Enable / Disable save button
        self.btn_save = self.ui.btn_box.button(QDialogButtonBox.Save)
        self.enable_btn_save()

        #Set slot connection
        self.ui.btn_box.accepted.connect(self.save)
        self.ui.txt_estructura.textChanged.connect(self.enable_btn_save)
        self.ui.txt_partida.textChanged.connect(self.enable_btn_save)

        #Set Modal
        self.setModal(True)

    def enable_btn_save(self):
        if (self.ui.txt_estructura.hasAcceptableInput() and 
        self.ui.txt_partida.hasAcceptableInput()):
            self.btn_save.setEnabled(True)
        else:
            self.btn_save.setEnabled(False)

    def save(self) -> bool:
        if self.ui.txt_estructura.hasAcceptableInput():
            registro = Facturero(
                self.ui.txt_nombre.text(),
                self.ui.txt_estructura.displayText(),
                self.ui.txt_partida.displayText(),
            )
            print(registro)
            try:
                # Create a record
                rec = self.model_facturero.record()
                # Get new row values for the new record
                rec.setGenerated('id', False)
                rec.setValue('razon_social', registro.razon_social)
                rec.setValue('estructura', registro.estructura)
                rec.setValue('partida', registro.partida)
                self.model_facturero.layoutAboutToBeChanged.emit()
                if not self.row_edit:
                    test = self.model_facturero.insertRecord(self.model_facturero.rowCount(), rec)
                else:
                    test = self.model_facturero.updateRowInTable(self.row_edit, rec)
                print(f'¿Se pudo insertar el registro? = {test}')
                self.model_facturero.select()
                return True
            except:
                return False

if __name__ == "__main__":
    app = QApplication(sys.argv)
    UIWindow = FormFacturero()
    app.exec_()
