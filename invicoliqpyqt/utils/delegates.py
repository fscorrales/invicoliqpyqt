from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QItemDelegate, QStyle, QStyledItemDelegate


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
        painter.save()

        painter.setPen(QPen(Qt.NoPen))
        if option.state & QStyle.State_Selected:
            painter.setBrush(QColor('#308cc6'))
        else:
            painter.setBrush(QBrush(Qt.white))
        painter.drawRect(option.rect)

        
        if option.state & QStyle.State_Selected:
            painter.setPen(QPen(Qt.white))
        else:
            painter.setPen(QPen(Qt.black))

        if index.column() in self.float_cols:
            value = index.model().data(index, Qt.EditRole)
            try:
                number = float(value)
                painter.drawText(option.rect, Qt.AlignRight|Qt.AlignVCenter, 
                                "{:,.2f}".format(number))
                
            except:
                QItemDelegate.paint(self, painter, option, index)
        elif index.column() in self.str_cols:
            text = index.model().data(index, Qt.EditRole)
            try:
                text = str(text[0:11])
                painter.drawText(option.rect, Qt.AlignHCenter|Qt.AlignVCenter, 
                                text)
            except:
                QItemDelegate.paint(self, painter, option, index)
            pass
        else:
            QItemDelegate.paint(self, painter, option, index)

        painter.restore()

    # Set background color
    # https://www.saltycrane.com/blog/2008/01/pyqt4-qitemdelegate-example-with/

    #How do I get the or set the native highlight color of a QWidget?
    # https://stackoverflow.com/questions/16348838/how-do-i-get-the-or-set-the-native-highlight-color-of-a-qwidget

    # See also:
    # https://stackoverflow.com/questions/46039595/selection-highlight-in-pyqt4-qtablewidget-fill-selected-cells-background-with-f
