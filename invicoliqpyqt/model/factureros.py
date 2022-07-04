from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlTableModel

class ModelFactureros(QSqlTableModel):
    def __init__(self, *args, **kwargs):
        super(ModelFactureros, self).__init__(*args, **kwargs)
        self.model = QSqlTableModel(self)
        self.model.setTable("factureros")
        self.model.setHeaderData(0, Qt.Horizontal, "ID")
        self.model.setHeaderData(1, Qt.Horizontal, "Nombre")
        self.model.setHeaderData(2, Qt.Horizontal, "Actividad")
        self.model.setHeaderData(3, Qt.Horizontal, "Partida")
        self.model.select()