from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlTableModel, QSqlQueryModel

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
        self.model.setHeaderData(1, Qt.Horizontal, "Comprobante SIIF")
        self.model.setHeaderData(2, Qt.Horizontal, "Nombre Completo")
        self.model.setHeaderData(3, Qt.Horizontal, "Honorarios")
        self.model.setHeaderData(4, Qt.Horizontal, "IIBB")
        self.model.setHeaderData(5, Qt.Horizontal, "LP")
        self.model.setHeaderData(6, Qt.Horizontal, "Sellos")
        self.model.setHeaderData(7, Qt.Horizontal, "Seguro")
        self.model.setHeaderData(8, Qt.Horizontal, "Otras Ret.")
        self.model.setHeaderData(9, Qt.Horizontal, "Ant.")
        self.model.setHeaderData(10, Qt.Horizontal, "Desc.")
        self.model.setHeaderData(11, Qt.Horizontal, "Estructura")
        self.model.setHeaderData(12, Qt.Horizontal, "Partida")
        self.model.select()

class ModelComprobantesSIIF(QSqlQueryModel):
    def __init__(self, *args, **kwargs):
        super(ModelComprobantesSIIF, self).__init__(*args, **kwargs)
        query = ("SELECT c.nro_entrada, c.fecha, c.tipo, h.importe_bruto "+ 
                "FROM comprobantes_siif AS c LEFT JOIN " +
                "(SELECT nro_entrada, sum(importe_bruto) AS importe_bruto " + 
                "FROM honorarios_factureros GROUP BY nro_entrada) AS h " +
                "ON c.nro_entrada = h.nro_entrada " +
                "ORDER BY fecha DESC")
        
        self.model = QSqlQueryModel()
        
        self.model.setQuery(query)