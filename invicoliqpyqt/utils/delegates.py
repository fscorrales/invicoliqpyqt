from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QItemDelegate, QStyle, QStyledItemDelegate


class FloatDelegate(QItemDelegate):
    def __init__(self, highlight_color = None, parent=None):
        QItemDelegate.__init__(self, parent=parent)
        if highlight_color == None:
            self.highlight_color = '#308cc6'
        else:
            self.highlight_color = highlight_color

    def paint(self, painter, option, index):
        painter.save()

        #background color
        painter.setPen(QPen(Qt.NoPen))
        if option.state & QStyle.State_Selected:
            painter.setBrush(QColor(self.highlight_color))
        else:
            painter.setBrush(QBrush(Qt.white))
        painter.drawRect(option.rect)

        #text color when selected and not
        if option.state & QStyle.State_Selected:
            painter.setPen(QPen(Qt.white))
        else:
            painter.setPen(QPen(Qt.black))

        value = index.model().data(index, Qt.EditRole)
        try:
            number = float(value)
            painter.drawText(option.rect, Qt.AlignRight|Qt.AlignVCenter, 
                            "{:,.2f}".format(number))
        except :
            QItemDelegate.paint(self, painter, option, index)

        painter.restore()

class MultipleDelegate(QItemDelegate):
    def __init__(self, float_cols=[], str_cols=[], 
    highlight_color = None ,parent=None):
        QItemDelegate.__init__(self, parent=parent)
        self.float_cols = float_cols
        self.str_cols = str_cols
        if highlight_color == None:
            self.highlight_color = '#308cc6'
        else:
            self.highlight_color = highlight_color

    def paint(self, painter, option, index):
        painter.save()

        #background color
        painter.setPen(QPen(Qt.NoPen))
        if option.state & QStyle.State_Selected:
            painter.setBrush(QColor(self.highlight_color))
        else:
            painter.setBrush(QBrush(Qt.white))
        painter.drawRect(option.rect)

        #text color when selected and not
        if option.state & QStyle.State_Selected:
            painter.setPen(QPen(Qt.white))
        else:
            painter.setPen(QPen(Qt.black))

        #Custom format on selected columns
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
