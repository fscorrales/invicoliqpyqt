from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QItemDelegate


class FloatDelegate(QItemDelegate):
    def __init__(self, decimals=None, parent=None):
        QItemDelegate.__init__(self, parent=parent)
        # self.nDecimals = decimals

    def paint(self, painter, option, index):
        value = index.model().data(index, Qt.EditRole)
        try:
            number = float(value)
            painter.drawText(option.rect, Qt.AlignRight|Qt.AlignVCenter, 
                            "{:,.2f}".format(number))
        except :
            QItemDelegate.paint(self, painter, option, index)
