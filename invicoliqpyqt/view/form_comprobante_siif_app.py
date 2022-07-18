import os
import sys
from dataclasses import dataclass

from invicoliqpyqt.utils.logger import log
from invicoliqpyqt.view.form_comprobante_siif import Ui_form_comprobante_siif
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QDialog


@dataclass
class ComprobanteSIIF():
    nro_entrada: str = ''
    fecha: str = ''
    tipo: str = ''

class FormComprobanteSIIF(QDialog):
    def __init__(self, model, nro_entrada_edit = None, parent = None):
        super(FormComprobanteSIIF, self).__init__(parent)
        
        # Set up UI
        self.ui = Ui_form_comprobante_siif()
        self.ui.setupUi(self)

        # Set up model
        self.model_comprobante_siif = model
        self.nro_entrada_edit = nro_entrada_edit

        # Enable the calendarPopup property
        self.ui.dat_fecha.setCalendarPopup(True)
        # self.menuBar().setCornerWidget(self.ui.dat_fecha, Qt.TopLeftCorner)
        self.ui.dat_fecha.setDate(QDate.currentDate())

		# Open The Image
        parent_dir = os.path.dirname
        self.fname = os.path.join(parent_dir(parent_dir(__file__)), 
        'static/images/form_comprobante_siif')
        print(self.fname)
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
        pass
        # registro = Facturero(
        #     self.ui.txt_nombre.text(),
        #     self.ui.txt_estructura.text(),
        #     self.ui.txt_partida.text(),
        # )
        # try:
        #     # Create a record
        #     rec = self.model_facturero.record()
        #     # Get new row values for the new record
        #     rec.setGenerated('id', False)
        #     rec.setValue('razon_social', registro.razon_social)
        #     rec.setValue('estructura', registro.estructura)
        #     rec.setValue('partida', registro.partida)
        #     self.model_facturero.layoutAboutToBeChanged.emit()
        #     if not self.row_edit:
        #         test = self.model_facturero.insertRecord(self.model_facturero.rowCount(), rec)
        #     else:
        #         test = self.model_facturero.updateRowInTable(self.row_edit, rec)
        #     print(f'¿Se pudo insertar el registro? = {test}')
        #     self.model_facturero.select()
        #     return True
        # except:
        #     return False

if __name__ == "__main__":
    app = QApplication(sys.argv)
    UIWindow = FormComprobanteSIIF()
    app.exec_()
