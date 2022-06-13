import sys
import os
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView, QWidget
from PyQt5.QtSql import QSqlTableModel
from invicoliqpyqt.model.factureros import FacturerosModel

# Inherit from QWidget
class ListadoFactureros(QMainWindow):
    def __init__(self, parent = None):
        super(ListadoFactureros, self).__init__(parent)
        # Load the ui file
        uic.loadUi(os.path.join(os.path.dirname(__file__), 'listado_factureros.ui'), self)
        # Define Our Widgets
        self.table_factureros = self.findChild(QTableView, 'table_factureros')

        # Set up the model
        self.model = QSqlTableModel(self)
        self.model.setTable("factureros")
        # self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model.setHeaderData(0, Qt.Horizontal, "ID")
        self.model.setHeaderData(1, Qt.Horizontal, "Nombre")
        self.model.setHeaderData(2, Qt.Horizontal, "Actividad")
        self.model.setHeaderData(3, Qt.Horizontal, "Partida")
        self.model.select()
        # Set up the view
        self.factureros_model = FacturerosModel(data = self.model)
        self.table_factureros.setModel(self.factureros_model)
        self.table_factureros.resizeColumnsToContents()
        #self.setCentralWidget(self.table_factureros)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    UIWindow = ListadoFactureros()
    app.exec_()