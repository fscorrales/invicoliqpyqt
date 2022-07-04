import os
import sys

from invicoliqpyqt.model.factureros_old import FacturerosModel
from invicoliqpyqt.utils.logger import log
from invicoliqpyqt.view.add_facturero import AddFacturero
from PyQt5 import uic
from PyQt5.QtCore import QSortFilterProxyModel, Qt
from PyQt5.QtSql import QSqlTableModel
from PyQt5.QtWidgets import (QApplication, QLabel, QMessageBox, QPushButton,
                             QTableView, QWidget)


# Inherit from QWidget
class ListadoFactureros(QWidget):
    def __init__(self):
        super(ListadoFactureros, self).__init__()
        #PRUEBA
        # Load the ui file
        uic.loadUi(os.path.join(os.path.dirname(__file__), 'listado_factureros.ui'), self)
        # Define Our Widgets
        self.table_factureros = self.findChild(QTableView, 'table_factureros')
        self.btn_add = self.findChild(QPushButton, 'btn_add')
        self.btn_edit = self.findChild(QPushButton, 'btn_edit')
        self.btn_del = self.findChild(QPushButton, 'btn_del')
        self.lbl_test = self.findChild(QLabel, 'lbl_test')

        #Set up model
        self.model_factureros = QSqlTableModel(self)
        self.model_factureros.setTable("factureros")
        self.model_factureros.setHeaderData(0, Qt.Horizontal, "ID")
        self.model_factureros.setHeaderData(1, Qt.Horizontal, "Nombre")
        self.model_factureros.setHeaderData(2, Qt.Horizontal, "Actividad")
        self.model_factureros.setHeaderData(3, Qt.Horizontal, "Partida")
        self.model_factureros.select()

        # #Initialize model
        # self.model_factureros = FacturerosModel(self)

        # #Try proxy model
        # proxyModel = QSortFilterProxyModel()
        # proxyModel.setSourceModel(self.model_factureros)

        #Connect view with model
        self.table_factureros.setModel(self.model_factureros)
        self.table_factureros.resizeColumnsToContents()

        # try some sorting
        #self.table_factureros.setSortingEnabled(True)
        # self.table_factureros.sortByColumn(1, Qt.AscendingOrder)

        # allow drag to rearrange columns
        # self.table_factureros.horizontalHeader().setMovable(True)

        #self.setCentralWidget(self.table_factureros)

        #Set slot connection
        self.btn_add.pressed.connect(lambda: self.add_facturero())
        self.btn_edit.pressed.connect(self.edit_facturero)
        self.btn_del.pressed.connect(self.del_facturero)

    def add_facturero(self):
        # Open second window
        self.window_add_facturero = AddFacturero(self.model_factureros)
        self.window_add_facturero.show()

    def edit_facturero(self):
        #Get index of the selected items
        indexes = self.table_factureros.selectedIndexes()
        if indexes:
            #Retrive the index row
            index = indexes[0]
            row = index.row()
            #Get index of each column of selected row
            facturero_id = self.model_factureros.index(row, 0)
            facturero_nombre = self.model_factureros.index(row, 1)
            facturero_estructura = self.model_factureros.index(row, 2)
            facturero_partida = self.model_factureros.index(row, 3)
            #Get data of selected row
            facturero_id = self.model_factureros.data(facturero_id, role=0)
            facturero_nombre = self.model_factureros.data(facturero_nombre, role=0)
            facturero_estructura = self.model_factureros.data(facturero_estructura, role=0)
            facturero_partida = self.model_factureros.data(facturero_partida, role=0)
            
            # Open second window in edit mode
            self.window_add_facturero = AddFacturero(self.model_factureros)
            self.window_add_facturero.txt_nombre.setText(facturero_nombre)
            self.window_add_facturero.txt_estructura.setText(facturero_estructura)
            self.window_add_facturero.txt_partida.setText(facturero_partida)
            self.window_add_facturero.show()

    def del_facturero(self):
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
                return self.model_factureros.removeRow(row)

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
