import sys

from invicoliqpyqt.utils.logger import log
from invicoliqpyqt.view.form_facturero_app import FormFacturero
from invicoliqpyqt.view.table_factureros import Ui_table_factureros
from invicoliqpyqt.utils.editable_headers import EditableHeaderView
from PyQt5 import QtCore
from PyQt5.QtSql import QSqlTableModel
from PyQt5.QtWidgets import (QAbstractItemView, QApplication, QMessageBox,
                             QWidget, QMenu, QAction)


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
        # headerview = EditableHeaderView(self.ui.table)
        # self.ui.table.setHorizontalHeader(headerview)

        #Initialize proxy model
        self._proxy = QtCore.QSortFilterProxyModel(self)
        self._proxy.setSourceModel(self.model)

        #Connect view with model
        self.ui.table.setModel(self._proxy)

        #Set up table properties
        self.ui.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.table.verticalHeader().setVisible(False)
        self.ui.table.hideColumn(0)
        self.ui.table.resizeColumnsToContents()
        self.ui.table.setSortingEnabled(True)
        self.ui.table.sortByColumn(1, QtCore.Qt.AscendingOrder)

        # allow drag to rearrange columns
        # self.table_factureros.horizontalHeader().setMovable(True)

        #self.setCentralWidget(self.table_factureros)

        #Set editable (filter) headers
        # headerview.setEditable(1, True)
        # headerview.setEditable(2, True)
        # headerview.setEditable(3, True)

        #Set slot connection
        # headerview.textChanged.connect(self.on_text_changed)
        self.ui.btn_add.clicked.connect(self.add_facturero)
        self.ui.btn_edit.clicked.connect(self.edit_facturero)
        self.ui.btn_del.clicked.connect(self.del_facturero)
        self.horizontalHeader = self.ui.table.horizontalHeader()
        self.horizontalHeader.sectionClicked.connect(self.on_view_horizontalHeader_sectionClicked)

    # @QtCore.pyqtSlot(int, str)
    # def on_text_changed(self, col, text):
    #     self._proxy.setFilterKeyColumn(col)
    #     self._proxy.setFilterWildcard("*{}*".format(text.upper()) if text else "")

    def add_facturero(self):
        # Open second window
        self.window_add_facturero = FormFacturero(self.model)
        self.window_add_facturero.show()

    def edit_facturero(self):
        #Get index of the selected items
        indexes = self.ui.table.selectedIndexes()
        if indexes:
            #Retrive the index row
            index = self._proxy.mapToSource(indexes[0])
            row = index.row()
            #Get index of each column of selected row
            facturero_id = self.model.index(row, 0)
            facturero_nombre = self.model.index(row, 1)
            facturero_estructura = self.model.index(row, 2)
            facturero_partida = self.model.index(row, 3)
            #Get data of selected row
            facturero_id = self.model.data(facturero_id, role=0)
            facturero_nombre = self.model.data(facturero_nombre, role=0)
            facturero_estructura = self.model.data(facturero_estructura, role=0)
            facturero_partida = self.model.data(facturero_partida, role=0)
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

    @QtCore.pyqtSlot(int)
    def on_view_horizontalHeader_sectionClicked(self, logicalIndex):

        self.logicalIndex   = logicalIndex
        self.menuValues     = QMenu(self)
        self.signalMapper   = QtCore.QSignalMapper(self)
        # self.comboBox.blockSignals(True)
        # self.comboBox.setCurrentIndex(self.logicalIndex)
        # self.comboBox.blockSignals(True)

        if self.logicalIndex != 1:
            # valuesUnique = self.model._df.iloc[:, self.logicalIndex].unique()
            data = []
            for row in range(self.model.rowCount()):
                index = self.model.index(row, self.logicalIndex)
                # We suppose data are strings
                data.append(str(self.model.data(index)))

            valuesUnique = list(set(data))

            actionAll = QAction("All", self)
            actionAll.triggered.connect(self.on_actionAll_triggered)
            self.menuValues.addAction(actionAll)
            self.menuValues.addSeparator()
            for actionNumber, actionName in enumerate(sorted(list(set(valuesUnique)))):
                action = QAction(actionName, self)
                self.signalMapper.setMapping(action, actionNumber)
                action.triggered.connect(self.signalMapper.map)
                self.menuValues.addAction(action)
            self.signalMapper.mapped.connect(self.on_signalMapper_mapped)
            headerPos = self.ui.table.mapToGlobal(self.horizontalHeader.pos())
            posY = headerPos.y() + self.horizontalHeader.height()
            posX = headerPos.x() + self.horizontalHeader.sectionPosition(self.logicalIndex)

            self.menuValues.exec_(QtCore.QPoint(posX, posY))

    @QtCore.pyqtSlot()
    def on_actionAll_triggered(self):
        filterColumn = self.logicalIndex
        filterString = QtCore.QRegExp(  "",
                                        QtCore.Qt.CaseInsensitive,
                                        QtCore.QRegExp.RegExp
                                        )

        self._proxy.setFilterRegExp(filterString)
        self._proxy.setFilterKeyColumn(filterColumn)

    @QtCore.pyqtSlot(int)
    def on_signalMapper_mapped(self, i):
        stringAction = self.signalMapper.mapping(i).text()
        filterColumn = self.logicalIndex
        filterString = QtCore.QRegExp(  stringAction,
                                        QtCore.Qt.CaseSensitive,
                                        QtCore.QRegExp.FixedString
                                        )

        self._proxy.setFilterRegExp(filterString)
        self._proxy.setFilterKeyColumn(filterColumn)

    @QtCore.pyqtSlot(str)
    def on_lineEdit_textChanged(self, text):
        search = QtCore.QRegExp(    text,
                                    QtCore.Qt.CaseInsensitive,
                                    QtCore.QRegExp.RegExp
                                    )

        self._proxy.setFilterRegExp(search)

    @QtCore.pyqtSlot(int)
    def on_comboBox_currentIndexChanged(self, index):
        self._proxy.setFilterKeyColumn(index)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    UIWindow = TableFactureros()
    app.exec_()
