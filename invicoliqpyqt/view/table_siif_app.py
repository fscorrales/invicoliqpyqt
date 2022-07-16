import sys

from invicoliqpyqt.model.models import ModelHonorariosFactureros
from invicoliqpyqt.model.comprobantes_siif import ModelComprobantesSIIF
from invicoliqpyqt.utils.delegates import FloatDelegate, MultipleDelegate
from invicoliqpyqt.view.table_siif import Ui_table_siif
from PyQt5.QtCore import QSortFilterProxyModel, Qt
from PyQt5.QtSql import QSqlQuery
from PyQt5.QtWidgets import QApplication, QTableWidgetItem, QWidget, QMessageBox


# Inherit from QMainWindow
class TableSIIF(QWidget):
    def __init__(self, model_object, parent = None):
        super(TableSIIF, self).__init__(parent)
        
        # Set up ui
        self.ui = Ui_table_siif()
        self.ui.setupUi(self)

        #Set up model
        self.model_comprobantes_siif = ModelComprobantesSIIF(self)
        self.proxy_comprobantes_siif = QSortFilterProxyModel(self)
        self.proxy_comprobantes_siif.setSourceModel(self.model_comprobantes_siif.model)
        self.model_honorarios = ModelHonorariosFactureros(self).model
        self.proxy_honorarios = QSortFilterProxyModel(self)
        self.proxy_honorarios.setSourceModel(self.model_honorarios)

        #Connect view with model
        self.ui.table_comprobantes.setModel(self.proxy_comprobantes_siif)
        self.ui.table_honorarios.setModel(self.proxy_honorarios)

        #Get default highlight color
        self.highlight_color = self.ui.table_comprobantes.palette().highlight().color().name()

        #Set table properties
        self.ui.table_comprobantes.hideColumn(0)
        self.ui.table_comprobantes.setItemDelegate(MultipleDelegate([5], [3], highlight_color=self.highlight_color))
        self.ui.table_comprobantes.resizeColumnsToContents()
        self.ui.table_comprobantes.setSortingEnabled(True)
        self.ui.table_comprobantes.sortByColumn(3, Qt.DescendingOrder)
        self.ui.table_honorarios.hideColumn(0)
        self.ui.table_honorarios.hideColumn(1)
        self.ui.table_honorarios.setItemDelegate(MultipleDelegate(range(3,11), highlight_color=self.highlight_color))
        self.ui.table_honorarios.verticalHeader().setVisible(False)
        # self.ui.table_honorarios.setItemDelegateForColumn(4, FloatDelegate())
        self.ui.table_honorarios.setSortingEnabled(True)
        self.ui.table_honorarios.resizeColumnsToContents()

        #Set slot connection
        self.ui.table_comprobantes.selectionModel().selectionChanged.connect(self.show_detail)
        self.ui.btn_delete.clicked.connect(self.delete_comprobante_siif)

        #Select first row
        self.ui.tab_siif.setCurrentIndex(0)
        self.ui.table_comprobantes.selectRow(0)

    def show_detail(self):
        indexes = self.ui.table_comprobantes.selectedIndexes()
        if indexes:
            #Get N° Entrada SIIF
            index = indexes[0]
            row = index.row()
            cyo_id = self.proxy_comprobantes_siif.index(row, 0)
            cyo_id = self.proxy_comprobantes_siif.data(cyo_id, role=0)
            
            #Update table imputaciones
            self.ui.table_imputaciones.setRowCount(0)
            self.ui.table_imputaciones.setColumnCount(3)
            self.ui.table_imputaciones.setHorizontalHeaderLabels(["Estructura", "Partida", "Ejecutado"])
            query = QSqlQuery('SELECT estructura, partida, ' + 
                                'sum(importe_bruto) as ejecutado ' + 
                                'FROM honorarios_factureros ' + 
                                f'WHERE nro_entrada = "{cyo_id}" '
                                'GROUP BY estructura, partida')
            while query.next():
                rows = self.ui.table_imputaciones.rowCount()
                self.ui.table_imputaciones.setRowCount(rows + 1)
                self.ui.table_imputaciones.setItem(rows, 0, QTableWidgetItem(query.value(0)))
                self.ui.table_imputaciones.setItem(rows, 1, QTableWidgetItem(query.value(1)))
                self.ui.table_imputaciones.setItem(rows, 2, QTableWidgetItem(str(query.value(2))))
            self.ui.table_imputaciones.setItemDelegateForColumn(2, FloatDelegate(highlight_color=self.highlight_color))
            self.ui.table_imputaciones.resizeColumnsToContents()
            
            #Update table retenciones
            # self.ui.table_retenciones.setRowCount(0)
            # self.ui.table_retenciones.setColumnCount(3)
            # self.ui.table_retenciones.setHorizontalHeaderLabels(["Estructura", "Partida", "Ejecutado"])
            # query = QSqlQuery('SELECT estructura, partida, ' + 
            #                     'sum(importe_bruto) as ejecutado ' + 
            #                     'FROM honorarios_factureros ' + 
            #                     f'WHERE nro_entrada = "{cyo_id}" '
            #                     'GROUP BY estructura, partida')
            # while query.next():
            #     rows = self.ui.table_retenciones.rowCount()
            #     self.ui.table_retenciones.setRowCount(rows + 1)
            #     self.ui.table_retenciones.setItem(rows, 0, QTableWidgetItem(query.value(0)))
            #     self.ui.table_retenciones.setItem(rows, 1, QTableWidgetItem(query.value(1)))
            #     self.ui.table_retenciones.setItem(rows, 2, QTableWidgetItem(str(query.value(2))))
            # self.ui.table_retenciones.setItemDelegateForColumn(2, FloatDelegate())
            # self.ui.table_retenciones.resizeColumnsToContents()
            
            #Update table honorarios (tab_honorarios)
            self.proxy_honorarios.layoutAboutToBeChanged.emit()
            self.proxy_honorarios.setFilterFixedString(str(cyo_id))
            self.proxy_honorarios.setFilterKeyColumn(1)
            self.proxy_honorarios.layoutChanged.emit()

    def delete_comprobante_siif(self):
        #Get index of the selected items
        indexes = self.ui.table_comprobantes.selectedIndexes()
        if indexes:
            #Retrive the index row
            index = self.proxy_comprobantes_siif.mapToSource(indexes[0])
            row = index.row()
            #Get index of first column of selected row
            nro_entrada_idx = self.model_comprobantes_siif.model.index(row, 0)
            #Get data of selected index
            nro_entrada = self.model_comprobantes_siif.model.data(nro_entrada_idx, role=0)
            if QMessageBox.question(self, "Comprobante SIIF - Eliminar", 
            f"¿Desea ELIMINAR el Nro de Comprobante SIIF: {nro_entrada}?",
            QMessageBox.Yes|QMessageBox.No) == QMessageBox.Yes: 
                # log.info(f'Agente {agente} eliminado')
                self.proxy_comprobantes_siif.layoutAboutToBeChanged.emit()
                result = self.model_comprobantes_siif.delete_row(nro_entrada)
                # print(f'Pudo borrarse la Fila Nro: {row}? {test}')
                self.proxy_comprobantes_siif.layoutChanged.emit()
                if result:
                    return True

if __name__ == "__main__":
    app = QApplication(sys.argv)
    UIWindow = TableSIIF()
    app.exec_()
