from re import I
from PyQt5.QtCore import QAbstractTableModel, Qt, QModelIndex

class FacturerosModel(QAbstractTableModel):
    def __init__(self, *args, data=None, **kwargs):
        super(FacturerosModel, self).__init__(*args, **kwargs)
        self._data = data

    def data(self, index, role):
        value = self._data.record(index.row()).value(index.column())
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
            return self._data.headerData(section, orientation, role=role)
    
    # Create the rowCount method
    def rowCount(self, parent: QModelIndex) -> int:
        if self._data != None:
            return self._data.rowCount()
        else:
            return 0
    
    # Create the columnCount method
    def columnCount(self, parent: QModelIndex) -> int:
        if self._data != None:
            return self._data.columnCount()
        else:
            return 0
