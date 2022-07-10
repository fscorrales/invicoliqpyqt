import sys

from invicoliqpyqt.view.table_siif import Ui_table_siif
from invicoliqpyqt.model.models import ModelImputacionesSIIF
from invicoliqpyqt.utils.delegates import FloatDelegate
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import pyqtSlot, QItemSelection, QSortFilterProxyModel

# Inherit from QMainWindow
class TableSIIF(QWidget):
    def __init__(self, model, parent = None):
        super(TableSIIF, self).__init__(parent)
        
        # Set up ui
        self.ui = Ui_table_siif()
        self.ui.setupUi(self)

        #Set up model
        self.model_comprobantes_siif = model
        self.model_imputaciones_siif = ModelImputacionesSIIF(self).model
        self.proxy_imputaciones_siif = QSortFilterProxyModel(self)
        self.proxy_imputaciones_siif.setSourceModel(self.model_imputaciones_siif)


        #Connect view with model
        self.ui.table_comprobantes.setModel(self.model_comprobantes_siif)
        self.ui.table_imputaciones.setModel(self.proxy_imputaciones_siif)

        #Set table properties
        self.ui.table_imputaciones.setItemDelegateForColumn(3, FloatDelegate())
        self.ui.table_imputaciones.hideColumn(0)
        self.ui.table_comprobantes.setItemDelegateForColumn(3, FloatDelegate())

        #Set slot connection
        self.ui.table_comprobantes.selectionModel().selectionChanged.connect(self.show_imputaciones)

    @pyqtSlot(QItemSelection, QItemSelection)
    def show_imputaciones(self, selected, deselected):
        print("selected: ")
        for ix in selected.indexes():
            row = ix.row()
            cyo_id = self.model_comprobantes_siif.index(row, 0)
            cyo_id = self.model_comprobantes_siif.data(cyo_id, role=0)
            self.proxy_imputaciones_siif.layoutAboutToBeChanged.emit()
            self.proxy_imputaciones_siif.setFilterKeyColumn(0)
            self.proxy_imputaciones_siif.setFilterFixedString(str(cyo_id))
            self.proxy_imputaciones_siif.layoutChanged.emit()

        # print("deselected: ")
        # for ix in deselected.indexes():
        #     print(ix.data())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    UIWindow = TableSIIF()
    app.exec_()
