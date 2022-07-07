import sys

from invicoliqpyqt.utils.logger import log
from invicoliqpyqt.view.form_facturero_app import FormFacturero
from invicoliqpyqt.view.table_factureros import Ui_table_factureros
from invicoliqpyqt.utils.editable_headers import EditableHeaderView
from PyQt5.QtCore import Qt, pyqtSlot, QSortFilterProxyModel
from PyQt5.QtSql import QSqlTableModel
from PyQt5.QtWidgets import (QAbstractItemView, QApplication, QMessageBox,
                             QWidget)


# Inherit from QWidget
class TableFactureros(QWidget):
    def __init__(self, model):
        super(TableFactureros, self).__init__()

        #Set up ui
        self.ui = Ui_table_factureros()
        self.ui.setupUi(self)

        #Set up model
        self.model = model
        # self.model = QSqlTableModel(self)
        # self.model.setTable("factureros")
        # self.model.setHeaderData(0, Qt.Horizontal, "ID")
        # self.model.setHeaderData(1, Qt.Horizontal, "Nombre")
        # self.model.setHeaderData(2, Qt.Horizontal, "Actividad")
        # self.model.setHeaderData(3, Qt.Horizontal, "Partida")
        # self.model.select()

        # Initialize editable headers
        headerview = EditableHeaderView(self.ui.table)
        self.ui.table.setHorizontalHeader(headerview)

        #Initialize proxy model
        self._proxy = QSortFilterProxyModel(self)
        self._proxy.setSourceModel(self.model)

        #Connect view with model
        self.ui.table.setModel(self._proxy)

        #Set up table properties
        self.ui.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.table.verticalHeader().setVisible(False)
        self.ui.table.hideColumn(0)
        self.ui.table.resizeColumnsToContents()
        self.ui.table.setSortingEnabled(True)
        self.ui.table.sortByColumn(1, Qt.AscendingOrder)

        # allow drag to rearrange columns
        # self.table_factureros.horizontalHeader().setMovable(True)

        #self.setCentralWidget(self.table_factureros)

        #Set editable (filter) headers
        headerview.setEditable(1, True)
        headerview.setEditable(2, True)
        headerview.setEditable(3, True)

        #Set slot connection
        headerview.textChanged.connect(self.on_text_changed)
        self.ui.btn_add.clicked.connect(self.add_facturero)
        self.ui.btn_edit.clicked.connect(self.edit_facturero)
        self.ui.btn_del.clicked.connect(self.del_facturero)

    @pyqtSlot(int, str)
    def on_text_changed(self, col, text):
        self._proxy.setFilterKeyColumn(col)
        self._proxy.setFilterWildcard("*{}*".format(text.upper()) if text else "")

    def add_facturero(self):
        # Open second window
        self.window_add_facturero = FormFacturero(self.model)
        self.window_add_facturero.show()

    def edit_facturero(self):
        #Get index of the selected items
        indexes = self.ui.table.selectedIndexes()
        if indexes:
            #Retrive the index row
            index = indexes[0]
            row = index.row()
            #Get index of each column of selected row
            facturero_id = self._proxy.index(row, 0)
            facturero_nombre = self._proxy.index(row, 1)
            facturero_estructura = self._proxy.index(row, 2)
            facturero_partida = self._proxy.index(row, 3)
            #Get data of selected row
            facturero_id = self._proxy.data(facturero_id, role=0)
            facturero_nombre = self._proxy.data(facturero_nombre, role=0)
            facturero_estructura = self._proxy.data(facturero_estructura, role=0)
            facturero_partida = self._proxy.data(facturero_partida, role=0)
            
            # Open second window in edit mode
            self.window_add_facturero = FormFacturero(self.model, row)
            self.window_add_facturero.ui.txt_nombre.setText(facturero_nombre)
            self.window_add_facturero.ui.txt_estructura.setText(facturero_estructura)
            self.window_add_facturero.ui.txt_partida.setText(facturero_partida)
            self.window_add_facturero.show()

    def del_facturero(self):
        #Get index of the selected items
        indexes = self.ui.table.selectedIndexes()
        if indexes:
            #Retrive the index row
            index = indexes[0]
            row = index.row()
            #Get index of first column of selected row
            agente_idx = self._proxy.index(row, 1)
            #Get data of selected index
            agente = self._proxy.data(agente_idx, role=0)
            if QMessageBox.question(self, "Facturero - Eliminar", 
            f"¿Desea ELIMINAR el Agente: {agente}?",
            QMessageBox.Yes|QMessageBox.No) == QMessageBox.Yes: 
                log.info(f'Agente {agente} eliminado')
                self.ui.lbl_test.setText(f'Agente {agente} eliminado')
                return self._proxy.removeRow(row), self.model.select()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    UIWindow = TableFactureros()
    app.exec_()
