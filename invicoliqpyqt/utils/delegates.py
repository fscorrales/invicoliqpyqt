from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QItemDelegate, QStyle


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

class MultipleDelegate(QItemDelegate):
    def __init__(self, float_cols=[], str_cols=[], parent=None):
        QItemDelegate.__init__(self, parent=parent)
        self.float_cols = float_cols
        self.str_cols = str_cols

    def paint(self, painter, option, index):
        if index.column() in self.float_cols:
            value = index.model().data(index, Qt.DisplayRole)
            try:
                number = float(value)
                painter.drawText(option.rect, Qt.AlignRight|Qt.AlignVCenter, 
                                "{:,.2f}".format(number))
                
            except:
                QItemDelegate.paint(self, painter, option, index)
        elif index.column() in self.str_cols:
            text = index.model().data(index, Qt.DisplayRole)
            try:
                text = str(text[0:11])
                painter.drawText(option.rect, Qt.AlignHCenter|Qt.AlignVCenter, 
                                text)
            except:
                QItemDelegate.paint(self, painter, option, index)
            pass
        else:
            QItemDelegate.paint(self, painter, option, index)
