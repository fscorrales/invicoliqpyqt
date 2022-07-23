import os
import sys
from dataclasses import dataclass, asdict
from datetime import date

from invicoliqpyqt.utils.logger import log
from invicoliqpyqt.utils.sqlite import sqlite_is_unique, sqlite_get_query
from invicoliqpyqt.view.form_comprobante_siif import Ui_form_comprobante_siif
from PyQt5.QtCore import QDate, QRegExp, Qt
from PyQt5.QtGui import QPixmap, QRegExpValidator
from PyQt5.QtWidgets import QApplication, QDialog, QDialogButtonBox


@dataclass
class ComprobanteSIIF():
    nro_entrada: str = ''
    fecha: date = QDate.currentDate()
    tipo: str = ''
    nro_entrada_prev: str = ''


class FormComprobanteSIIF(QDialog):
    def __init__(self, model, nro_entrada_edit='', parent=None):
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

        # Add items to ComboBox tipo
        self.ui.cmb_tipo.addItem("Honorarios", "H")
        self.ui.cmb_tipo.addItem("Comisiones", "C")
        self.ui.cmb_tipo.addItem("Horas Extras", "E")
        self.ui.cmb_tipo.addItem("L", "L")

        # Open The Image
        parent_dir = os.path.dirname
        self.fname = os.path.join(parent_dir(parent_dir(__file__)),
                                  'static/images/form_comprobante_siif')
        print(self.fname)
        self.pixmap = QPixmap(self.fname)
        # Scale Pic
        self.ui.lbl_img.setScaledContents(True)
        # Add Pic to label
        self.ui.lbl_img.setPixmap(self.pixmap)

        # Validator
        self.txt_nro_entrada_validador = QRegExpValidator(
            QRegExp('\d{1,5}'), self.ui.txt_nro_entrada)
        self.ui.txt_nro_entrada.setValidator(self.txt_nro_entrada_validador)

        # Complete fields if updating info
        if self.nro_entrada_edit != '':
            query = sqlite_get_query('comprobantes_siif', 'nro_entrada',
                                    self.nro_entrada_edit)
            self.ui.txt_nro_entrada.setText(self.nro_entrada_edit[0:5])
            tipo_idx = query.record().indexOf('tipo')
            tipo_idx = self.ui.cmb_tipo.findData(query.value(tipo_idx))
            self.ui.cmb_tipo.setCurrentIndex(tipo_idx)
            fecha_idx = query.record().indexOf('fecha')
            fecha = query.value(fecha_idx)[0:10]
            self.ui.dat_fecha.setDate(QDate.fromString(fecha, 'yyyy-MM-dd'))

        # Enable / Disable save button
        self.btn_save = self.ui.btn_box.button(QDialogButtonBox.Save)
        self.enable_btn_save()

        # Set slot connection
        self.ui.btn_box.accepted.connect(self.save)
        self.ui.txt_nro_entrada.textChanged.connect(self.enable_btn_save)
        self.ui.dat_fecha.dateChanged.connect(self.enable_btn_save)

        # Set Modal
        self.setModal(True)

    def get_complete_nro_entrada(self) -> str:
        self.complete_nro_entrada = (self.ui.txt_nro_entrada.text().zfill(5) + '/' +
                                     str(self.ui.dat_fecha.date().year())[-2:])
        return self.complete_nro_entrada

    def unique_nro_entrada(self) -> bool:
        search_value = self.get_complete_nro_entrada()

        # if editing row
        if (self.nro_entrada_edit != ''):
            if (search_value == self.nro_entrada_edit):
                return True
            else:
                if sqlite_is_unique('comprobantes_siif', 'nro_entrada',
                                    search_value):
                    return True
                else:
                    return False

        if self.ui.txt_nro_entrada.hasAcceptableInput():
            if sqlite_is_unique('comprobantes_siif', 'nro_entrada',
                                search_value):
                return True
            else:
                return False

    def enable_btn_save(self):
        self.btn_save.setEnabled(False)
        if self.unique_nro_entrada():
            self.btn_save.setEnabled(True)

    def save(self) -> bool:
        registro = ComprobanteSIIF(
            self.complete_nro_entrada,
            self.ui.dat_fecha.date(),
            self.ui.cmb_tipo.currentData(),
            self.nro_entrada_edit,
        )
        if self.nro_entrada_edit == '':
            self.model_comprobante_siif.add_row(registro=asdict(registro))
        else:
            self.model_comprobante_siif.edit_row(registro=asdict(registro))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    UIWindow = FormComprobanteSIIF()
    app.exec_()
