import sys

from invicoliqpyqt.model.comprobantes_siif import (ModelComprobantesSIIF,
                                                   ModelImputacionesSIIF,
                                                   ModelRetencionesSIIF)
from invicoliqpyqt.model.models import ModelHonorariosFactureros
from invicoliqpyqt.utils.delegates import FloatDelegate, MultipleDelegate
from invicoliqpyqt.view.table_siif import Ui_table_siif
from PyQt5.QtCore import QSortFilterProxyModel, Qt
from PyQt5.QtWidgets import (QApplication, QMessageBox,
                             QWidget)


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

    def get_selected_nro_entrada(self) -> str:
        indexes = self.ui.table_comprobantes.selectedIndexes()
        if indexes:
            #Get N° Entrada SIIF
            index = indexes[0]
            row = index.row()
            cyo_id = self.proxy_comprobantes_siif.index(row, 0)
            cyo_id = self.proxy_comprobantes_siif.data(cyo_id, role=0)
            return cyo_id
        else:
            return False

    def show_detail(self):
        cyo_id = self.get_selected_nro_entrada()
        if cyo_id:            
            #Update table Imputaciones
            self.model_imputaciones_siif = ModelImputacionesSIIF(id = cyo_id)
            self.ui.table_imputaciones.setModel(self.model_imputaciones_siif.model)
            self.ui.table_imputaciones.setItemDelegateForColumn(2, FloatDelegate(highlight_color=self.highlight_color))
            self.ui.table_imputaciones.resizeColumnsToContents()

            #Update table retenciones
            self.model_retenciones_siif = ModelRetencionesSIIF(id = cyo_id)
            self.ui.table_retenciones.setModel(self.model_retenciones_siif.model)
            self.ui.table_retenciones.setItemDelegateForColumn(1, FloatDelegate(highlight_color=self.highlight_color))
            self.ui.table_retenciones.resizeColumnsToContents()
                        
            #Update table honorarios (tab_honorarios)
            self.proxy_honorarios.layoutAboutToBeChanged.emit()
            self.proxy_honorarios.setFilterFixedString(str(cyo_id))
            self.proxy_honorarios.setFilterKeyColumn(1)
            self.proxy_honorarios.layoutChanged.emit()

    def delete_comprobante_siif(self):
        nro_entrada = self.get_selected_nro_entrada()
        if nro_entrada:
            if QMessageBox.question(self, "Comprobante SIIF - Eliminar", 
            f"¿Desea ELIMINAR el Nro de Comprobante SIIF: {nro_entrada}?",
            QMessageBox.Yes|QMessageBox.No) == QMessageBox.Yes: 
                # log.info(f'Agente {agente} eliminado')
                self.proxy_comprobantes_siif.layoutAboutToBeChanged.emit()
                result = self.model_comprobantes_siif.delete_row(nro_entrada)
                # print(f'Pudo borrarse la Fila Nro: {row}? {test}')
                self.proxy_comprobantes_siif.layoutChanged.emit()
                

if __name__ == "__main__":
    app = QApplication(sys.argv)
    UIWindow = TableSIIF()
    app.exec_()
