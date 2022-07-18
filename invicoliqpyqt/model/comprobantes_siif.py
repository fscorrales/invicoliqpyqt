import re

from invicoliqpyqt.utils.logger import log
from PyQt5.QtCore import QModelIndex, Qt
from PyQt5.QtSql import QSqlQuery, QSqlQueryModel
from PyQt5.QtWidgets import QMessageBox


class ModelComprobantesSIIF(QSqlQueryModel):
    def __init__(self, *args, **kwargs):
        super(ModelComprobantesSIIF, self).__init__(*args, **kwargs)
        self.main_query = ("SELECT c.nro_entrada, substr(c.nro_entrada, 1, 5) AS comprobante, " +
                "'20' || substr(c.nro_entrada, 7, 8) AS ejercicio, "+ 
                "c.fecha, c.tipo, h.importe_bruto, h.retenciones, "+ 
                "(h.importe_bruto - h.retenciones) AS importe_neto " +
                "FROM comprobantes_siif AS c LEFT JOIN " +
                "(SELECT nro_entrada, sum(importe_bruto) AS importe_bruto, " +
                "sum(iibb + libramiento_pago + sellos + seguro + mutual + embargo + " +
                "otras_retenciones + anticipo) AS retenciones "
                "FROM honorarios_factureros GROUP BY nro_entrada) AS h " +
                "ON c.nro_entrada = h.nro_entrada " +
                "ORDER BY fecha DESC, comprobante DESC")
        
        self.model = QSqlQueryModel()
        
        self.model.setQuery(self.main_query)

        self.model.setHeaderData(0, Qt.Horizontal, "ID")
        self.model.setHeaderData(1, Qt.Horizontal, "Comprobante")
        self.model.setHeaderData(2, Qt.Horizontal, "Ejercicio")
        self.model.setHeaderData(3, Qt.Horizontal, "Fecha")
        self.model.setHeaderData(4, Qt.Horizontal, "Tipo")
        self.model.setHeaderData(5, Qt.Horizontal, "Importe Bruto")
        self.model.setHeaderData(6, Qt.Horizontal, "Retenciones")
        self.model.setHeaderData(7, Qt.Horizontal, "Importe Neto")

    def delete_row(self, nro_entrada):
        msg = QMessageBox()
        msg.setWindowTitle('Eliminación comprobante SIIF')
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
                msg.setIcon(QMessageBox.Information)
                msg.exec_()
                log.info(f'Comprobante SIIF Nro {self.id} eliminado')                
                return True
            else:
                print(query.lastError())
                return False
        else:
            msg.setText(f'Comprobante Nro {self.id} no cumple con el patrón 00000/00')
            msg.setIcon(QMessageBox.Critical)
            msg.exec_()
            return False

class ModelImputacionesSIIF(QSqlQueryModel):
    def __init__(self, id = None, *args, **kwargs):
        super(ModelImputacionesSIIF, self).__init__(*args, **kwargs)
        self.cyo_id = id
        self.main_query = ('SELECT estructura, partida, ' + 
                                'sum(importe_bruto) as ejecutado ' + 
                                'FROM honorarios_factureros ' + 
                                f'WHERE nro_entrada = "{self.cyo_id}" '
                                'GROUP BY estructura, partida')
        
        self.model = QSqlQueryModel()
        
        self.model.setQuery(self.main_query)

        self.model.setHeaderData(0, Qt.Horizontal, "Estructura")
        self.model.setHeaderData(1, Qt.Horizontal, "Partida")
        self.model.setHeaderData(2, Qt.Horizontal, "Importe Ejecutado")

class ModelRetencionesSIIF(QSqlQueryModel):
    def __init__(self, id = None, *args, **kwargs):
        super(ModelRetencionesSIIF, self).__init__(*args, **kwargs)
        self.cyo_id = id
        self.main_query = ('SELECT "101" AS codigo, sum(iibb) AS importe ' +
                        'FROM honorarios_factureros ' +
                        f'WHERE nro_entrada = "{self.cyo_id}" ' +
                        'UNION ALL ' +
                        'SELECT "102" AS codigo, sum(sellos) AS importe '+
                        'FROM honorarios_factureros ' +
                        f'WHERE nro_entrada = "{self.cyo_id}" ' +
                        'UNION ALL ' +
                        'SELECT "104" AS codigo, sum(libramiento_pago) AS importe '+
                        'FROM honorarios_factureros ' +
                        f'WHERE nro_entrada = "{self.cyo_id}" ' + 
                        'UNION ALL ' +
                        'SELECT "255" AS codigo, sum(embargo) AS importe '+
                        'FROM honorarios_factureros ' +
                        f'WHERE nro_entrada = "{self.cyo_id}" ' + 
                        'UNION ALL ' +
                        'SELECT "341" AS codigo, sum(mutual) AS importe '+
                        'FROM honorarios_factureros ' +
                        f'WHERE nro_entrada = "{self.cyo_id}" ' + 
                        'UNION ALL ' +
                        'SELECT "413" AS codigo, sum(seguro) AS importe '+
                        'FROM honorarios_factureros ' +
                        f'WHERE nro_entrada = "{self.cyo_id}"')
        
        self.model = QSqlQueryModel()
        
        self.model.setQuery(self.main_query)

        self.model.setHeaderData(0, Qt.Horizontal, "Codigo Retencion")
        self.model.setHeaderData(1, Qt.Horizontal, "Importe Retenido")