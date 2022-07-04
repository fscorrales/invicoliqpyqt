import os
import sys
from dataclasses import dataclass

from invicoliqpyqt.utils.logger import log
from invicoliqpyqt.view.form_facturero import Ui_form_facturero
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QDialog, QLabel


@dataclass
class Facturero():
    nombre: str = ''
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
        'static/images/form_factureros_agregar.jpg')
        self.pixmap = QPixmap(self.fname)
        #Scale Pic
        self.ui.lbl_img.setScaledContents(True)
        # Add Pic to label
        self.ui.lbl_img.setPixmap(self.pixmap)

        #Set slot connection
        self.ui.btn_box.accepted.connect(self.save)

        #Set Modal
        self.setModal(True)


    def save(self) -> bool:
        registro = Facturero(
            self.ui.txt_nombre.text(),
            self.ui.txt_estructura.text(),
            self.ui.txt_partida.text(),
        )
        try:
            # Create a record
            rec = self.model_facturero.record()
            # Get new row values for the new record
            rec.setGenerated('id', False)
            rec.setValue('nombre_completo', registro.nombre)
            rec.setValue('actividad', registro.estructura)
            rec.setValue('partida', registro.partida)
            if not self.row_edit:
                test = self.model_facturero.insertRecord(self.model_facturero.rowCount(), rec)
            else:
                test = self.model_facturero.updateRowInTable(self.row_edit, rec)
            print(f'¿Se pudo insertar el registro? = {test}')
            #self.model_facturero.layoutChanged.emit()
            #self.model_facturero.dataChanged.emit()
            return True
        except:
            return False

if __name__ == "__main__":
    app = QApplication(sys.argv)
    UIWindow = FormFacturero()
    app.exec_()
