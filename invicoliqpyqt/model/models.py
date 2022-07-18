from PyQt5 import QtCore
from PyQt5.QtSql import QSqlTableModel, QSqlQueryModel


class ModelFactureros(QSqlTableModel):
    def __init__(self, *args, **kwargs):
        super(ModelFactureros, self).__init__(*args, **kwargs)
        self.model = QSqlTableModel(self)
        self.model.setTable("factureros")
        self.model.setHeaderData(0, QtCore.Qt.Horizontal, "ID")
        self.model.setHeaderData(1, QtCore.Qt.Horizontal, "Nombre Completo")
        self.model.setHeaderData(2, QtCore.Qt.Horizontal, "Estructura")
        self.model.setHeaderData(3, QtCore.Qt.Horizontal, "Partida")
        self.model.select()

class ModelHonorariosFactureros(QSqlTableModel):
    def __init__(self, *args, **kwargs):
        super(ModelHonorariosFactureros, self).__init__(*args, **kwargs)
        self.model = QSqlTableModel(self)
        self.model.setTable("honorarios_factureros")
        self.model.setHeaderData(0, QtCore.Qt.Horizontal, "ID")
        self.model.setHeaderData(1, QtCore.Qt.Horizontal, "Comprobante SIIF")
        self.model.setHeaderData(2, QtCore.Qt.Horizontal, "Nombre Completo")
        self.model.setHeaderData(3, QtCore.Qt.Horizontal, "Honorarios")
        self.model.setHeaderData(4, QtCore.Qt.Horizontal, "IIBB")
        self.model.setHeaderData(5, QtCore.Qt.Horizontal, "LP")
        self.model.setHeaderData(6, QtCore.Qt.Horizontal, "Sellos")
        self.model.setHeaderData(7, QtCore.Qt.Horizontal, "Seguro")
        self.model.setHeaderData(8, QtCore.Qt.Horizontal, "Otras Ret.")
        self.model.setHeaderData(9, QtCore.Qt.Horizontal, "Ant.")
        self.model.setHeaderData(10, QtCore.Qt.Horizontal, "Desc.")
        self.model.setHeaderData(11, QtCore.Qt.Horizontal, "Estructura")
        self.model.setHeaderData(12, QtCore.Qt.Horizontal, "Partida")
        self.model.select()
        while self.model.canFetchMore():
            self.model.fetchMore()

class ModelImputacionesSIIF(QSqlQueryModel):
    def __init__(self,*args, **kwargs):
        super(ModelImputacionesSIIF, self).__init__(*args, **kwargs)
        query = ('SELECT nro_entrada, estructura, partida, ' + 
                'sum(importe_bruto) as ejecutado ' + 
                'FROM honorarios_factureros ' + 
                'GROUP BY nro_entrada')
        
        self.model = QSqlQueryModel()
        
        self.model.setQuery(query)

class CustomMultipleFilter(QtCore.QSortFilterProxyModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._filters = dict()

    @property
    def filters(self):
        return self._filters

    def setFilter(self, expresion, column):
        if expresion:
            self.filters[column] = expresion
        elif column in self.filters:
            del self.filters[column]
        self.invalidateFilter()

    def filterAcceptsRow(self, source_row, source_parent):
        for column, expresion in self.filters.items():
            text = self.sourceModel().index(source_row, column, source_parent).data()
            regex = QtCore.QRegExp(
                expresion, QtCore.Qt.CaseInsensitive, QtCore.QRegExp.RegExp
            )
            if regex.indexIn(text) == -1:
                return False
        return True