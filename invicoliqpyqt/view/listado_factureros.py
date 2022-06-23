import sys
import os
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QTableView, QWidget, QPushButton, QLabel
from PyQt5.QtSql import QSqlTableModel
from invicoliqpyqt.model.factureros import FacturerosModel

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
            index = self.model_factureros.index(row, 0)
            #Get data of selected index
            prueba = self.model_factureros.data(index, role=0)
            self.model_factureros.delete_row(row)
            self.lbl_test.setText(str(prueba))

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