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

    #     if option.state & QStyle.State_Selected:
    #         option.palette.setColor(QPalette.HighlightedText, Qt.black)
    #         color = self.combineColors(self.color_default, self.background(option, index))
    #         option.palette.setColor(QPalette.Highlight, color)
    #     QStyledItemDelegate.paint(self, painter, option, index)

    # color_default = QColor("#aaedff")

    # def background(self, option, index):
    #     item = self.parent().itemFromIndex(index)
    #     if item:
    #         if item.background() != QBrush():
    #             return item.background().color()
    #     if self.parent().alternatingRowColors():
    #         if index.row() % 2 == 1:
    #             return option.palette.color(QPalette.AlternateBase)
    #     return option.palette.color(QPalette.Base)

    # @staticmethod
    # def combineColors(c1, c2):
    #     c3 = QColor()
    #     c3.setRed((c1.red() + c2.red()) / 2)
    #     c3.setGreen((c1.green() + c2.green()) / 2)
    #     c3.setBlue((c1.blue() + c2.blue()) / 2)

    #     return c3

    # https://stackoverflow.com/questions/46039595/selection-highlight-in-pyqt4-qtablewidget-fill-selected-cells-background-with-f

    # See also:
    # https://www.saltycrane.com/blog/2008/01/pyqt4-qitemdelegate-example-with/