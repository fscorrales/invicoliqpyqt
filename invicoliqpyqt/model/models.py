from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlTableModel

class ModelFactureros(QSqlTableModel):
    def __init__(self, *args, **kwargs):
        super(ModelFactureros, self).__init__(*args, **kwargs)
        self.model = QSqlTableModel(self)
        self.model.setTable("factureros")
        self.model.setHeaderData(0, Qt.Horizontal, "ID")
        self.model.setHeaderData(1, Qt.Horizontal, "Nombre Completo")
        self.model.setHeaderData(2, Qt.Horizontal, "Estructura")
        self.model.setHeaderData(3, Qt.Horizontal, "Partida")
        self.model.select()

class ModelHonorariosFactureros(QSqlTableModel):
    def __init__(self, *args, **kwargs):
        super(ModelHonorariosFactureros, self).__init__(*args, **kwargs)
        self.model = QSqlTableModel(self)
        self.model.setTable("honorarios_factureros")
        self.model.setHeaderData(0, Qt.Horizontal, "ID")
        self.model.setHeaderData(1, Qt.Horizontal, "Fecha")
        self.model.setHeaderData(2, Qt.Horizontal, "Nombre Completo")
        self.model.setHeaderData(3, Qt.Horizontal, "Sellos")
        self.model.setHeaderData(4, Qt.Horizontal, "Seguro")
        self.model.setHeaderData(5, Qt.Horizontal, "Comprobante SIIF")
        self.model.setHeaderData(6, Qt.Horizontal, "Tipo")
        self.model.setHeaderData(7, Qt.Horizontal, "Bruto")
        self.model.setHeaderData(8, Qt.Horizontal, "IIBB")
        self.model.setHeaderData(9, Qt.Horizontal, "LP")
        self.model.setHeaderData(10, Qt.Horizontal, "Otras Ret.")
        self.model.setHeaderData(11, Qt.Horizontal, "Ant.")
        self.model.setHeaderData(12, Qt.Horizontal, "Desc.")
        self.model.setHeaderData(13, Qt.Horizontal, "Estructura")
        self.model.setHeaderData(14, Qt.Horizontal, "Partida")
        self.model.select()