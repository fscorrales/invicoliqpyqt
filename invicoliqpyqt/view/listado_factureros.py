import sys
import os
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QTableView, QWidget, QPushButton, QLabel, QMessageBox
from invicoliqpyqt.model.factureros import FacturerosModel
from invicoliqpyqt.utils.logger import log

# Inherit from QWidget
class ListadoFactureros(QWidget):
    def __init__(self, parent = None):
        super(ListadoFactureros, self).__init__(parent)
        # Load the ui file
        uic.loadUi(os.path.join(os.path.dirname(__file__), 'listado_factureros.ui'), self)
        # Define Our Widgets
        self.table_factureros = self.findChild(QTableView, 'table_factureros')
        self.btn_add = self.findChild(QPushButton, 'btn_add')
        self.btn_edit = self.findChild(QPushButton, 'btn_edit')
        self.btn_del = self.findChild(QPushButton, 'btn_del')
        self.lbl_test = self.findChild(QLabel, 'lbl_test')

        #Initialize model
        self.model_factureros = FacturerosModel(self)

        #Connect view with model
        self.table_factureros.setModel(self.model_factureros)
        self.table_factureros.resizeColumnsToContents()

        #self.setCentralWidget(self.table_factureros)

        #Set slot connection
        self.btn_del.pressed.connect(self.delete)

    def delete(self):
        #Get index of the selected items
        indexes = self.table_factureros.selectedIndexes()
        if indexes:
            #Retrive the index row
            index = indexes[0]
            row = index.row()
            #Get index of first column of selected row
            agente_idx = self.model_factureros.index(row, 1)
            #Get data of selected index
            agente = self.model_factureros.data(agente_idx, role=0)
            if QMessageBox.question(self, "Facturero - Eliminar", 
            f"¿Desea ELIMINAR el Agente: {agente}?",
            QMessageBox.Yes|QMessageBox.No) == QMessageBox.Yes: 
                log.info(f'Agente {agente} eliminado')
                self.lbl_test.setText(f'Agente {agente} eliminado')
                return self.model_factureros.delete_row(row)

    # def sortTable(self, section):
    #     if section in (ships.OWNER, ships.COUNTRY):
    #         self.model.sortByCountryOwner() 
    #     else:
    #         self.model.sortByName()
    #         self.resizeColumns()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    UIWindow = ListadoFactureros()
    app.exec_()