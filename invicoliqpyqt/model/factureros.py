from PyQt5.QtCore import QAbstractTableModel, Qt, QModelIndex
from PyQt5.QtSql import QSqlTableModel

class FacturerosModel(QAbstractTableModel):
    def __init__(self, *args, **kwargs):
        super(FacturerosModel, self).__init__(*args, **kwargs)
        #Set up model
        self.model = QSqlTableModel(self)
        self.model.setTable("factureros")
        self.model.setHeaderData(0, Qt.Horizontal, "ID")
        self.model.setHeaderData(1, Qt.Horizontal, "Nombre")
        self.model.setHeaderData(2, Qt.Horizontal, "Actividad")
        self.model.setHeaderData(3, Qt.Horizontal, "Partida")
        self.model.select()

    def data(self, index, role):
        value = self.model.record(index.row()).value(index.column())
        if role == Qt.ItemDataRole.DisplayRole:
            # if isinstance(value, int) and index.column() == 1:
            #     return "${: ,.2f}".format(value)
            # if isinstance(value, str) and index.column() == 4:
            #     date_object = date.fromisoformat(value)
            #     return date_object.strftime('%x')
            return value

        # if role == Qt.ItemDataRole.DecorationRole:
        #     if isinstance(value, int) and index.column() == 0:
        #         return QtGui.QIcon('data/icons/hashtag_icon.png')
        #     if isinstance(value, str) and index.column() == 4:
        #         return QtGui.QIcon('data/icons/calendar.png')

    # Create the headerData method
    def headerData(self, section: int, orientation: Qt.Orientation, role: int):
        # section is the index of the column/row.
        if role == Qt.ItemDataRole.DisplayRole and orientation == Qt.Orientation.Horizontal:
            return self.model.headerData(section, orientation, role=role)
    
    # Create the rowCount method
    def rowCount(self, parent: QModelIndex) -> int:
        return self.model.rowCount()
    
    # Create the columnCount method
    def columnCount(self, parent: QModelIndex) -> int:
        return self.model.columnCount()

    def delete_row(self, row_int)-> bool:
        try:
            self.model.beginRemoveRows(QModelIndex(), self.model.rowCount(), self.model.rowCount())
            self.model.removeRow(row_int, QModelIndex())
            self.model.endRemoveRows()
            self.model.select()
            return True
        except:
            return False

    def insertRow(self) -> bool:
        try:
            # Create a record
            rec = self.model.record()
            # Get new row values for the new record
            # rec.setValue('Order ID', form.order_record.order_id)
            # rec.setValue('Product', form.order_record.product_id)
            # rec.setValue('Price', form.order_record.product_id)
            # rec.setValue('Customer', form.order_record.customer_id)
            # rec.setValue('Date', form.order_record.getOrderDateISO())
            # rec.setValue('Qty', form.order_record.order_qty)
            # rec.setValue('Order Value', form.order_record.order_value)

            # Begin inserting the new row
            # self.beginInsertRows(QModelIndex(), self._model.rowCount(), self._model.rowCount())
            # self._model.insertRecord(self._model.rowCount(), rec)
            # self.endInsertRows()
            # self._model.select()
            return True
        except:
            return False