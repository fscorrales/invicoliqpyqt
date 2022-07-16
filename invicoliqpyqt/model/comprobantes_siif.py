import re

from PyQt5.QtSql import QSqlQuery, QSqlQueryModel
from PyQt5.QtCore import QModelIndex
from PyQt5.QtWidgets import QMessageBox


class ModelComprobantesSIIF(QSqlQueryModel):
    def __init__(self, *args, **kwargs):
        super(ModelComprobantesSIIF, self).__init__(*args, **kwargs)
        self.main_query = ("SELECT c.nro_entrada, substr(c.nro_entrada, 1, 5) AS comprobante, " +
                "'20' || substr(c.nro_entrada, 7, 8) AS ejercicio, "+ 
                "c.fecha, c.tipo, h.importe_bruto "+ 
                "FROM comprobantes_siif AS c LEFT JOIN " +
                "(SELECT nro_entrada, sum(importe_bruto) AS importe_bruto " + 
                "FROM honorarios_factureros GROUP BY nro_entrada) AS h " +
                "ON c.nro_entrada = h.nro_entrada " +
                "ORDER BY fecha DESC, comprobante DESC")
        
        self.model = QSqlQueryModel()
        
        self.model.setQuery(self.main_query)

    def delete_row(self, nro_entrada):
        msg = QMessageBox()
        patron = r'\d{5}/\d{2}'
        self.validator = re.compile(patron)
        self.id = nro_entrada
        if self.validator.match(self.id) is not None and len(self.id) == 8:
            self.model.beginRemoveRows(QModelIndex(), self.model.rowCount(), self.model.rowCount())
            query = QSqlQuery()
            query.exec_('PRAGMA foreign_keys = ON')
            query.prepare('DELETE FROM comprobantes_siif WHERE nro_entrada = ?')
            query.bindValue(0, self.id)
            result = query.exec_()
            if result:
                self.model.setQuery(self.main_query)
                self.model.endRemoveRows()
                msg.setText(f'Comprobante Nro {self.id} ELIMINADO')
                msg.exec_()
                return True
            else:
                query.lastError()
                return False
        else:
            return False
