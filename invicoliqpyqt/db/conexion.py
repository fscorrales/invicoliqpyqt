from PyQt5.QtSql import QSqlDatabase
import sys
import os
from invicoliqpyqt.utils.logger import log

class Conexion(object):
    _DATABASE = 'slave.sqlite'
    # _USERNAME = 'postgres'
    # _PASSWORD = 'admin'
    # _DB_PORT = '5432'
    # _HOST = '127.0.0.1'
    con = None
    _nombre_conexion = None
    # _cursor = None

    def __init__(self, nombre_conexion = None):
        if nombre_conexion != None:
            self._nombre_conexion = nombre_conexion

    def __enter__(self):
        log.info('Creamos la conexión a la BD')
        self.obtener_conexion()
        print(f'Listado Tablas: {self.con.tables()}')

    def __exit__(self, exc_type, exc_val, exc_tb):
        log.info(f'Cerramos la conexión: {self.con}')
        self.con.close()

    @classmethod
    def obtener_conexion(cls):
        if cls.con is None:
            try:
                if cls._nombre_conexion == None:
                    cls.con = QSqlDatabase.addDatabase('QSQLITE')
                else:
                    cls.con = QSqlDatabase.addDatabase('QSQLITE', connectionName=cls._nombre_conexion)
                cls.con.setDatabaseName(os.path.join(os.path.dirname(__file__), cls._DATABASE))
                cls.con.open()
                log.info(f'Conexión exitosa: {cls.con}')
            except Exception as e:
                log.error(f'Ocurrió una excepción al obtener la conexión: {e}')
                sys.exit()
        else:
            return cls.con

    @classmethod
    def cerrar_conexion(cls):
        cls.con.close()

    # @classmethod
    # def obtenerCursor(cls):
    #     if cls._cursor is None:
    #         try:
    #             cls._cursor = cls.obtenerConexion().cursor()
    #             log.debug(f'Se abrió correctamente el cursor: {cls._cursor}')
    #             return cls._cursor
    #         except Exception as e:
    #             log.error(f'Ocurrió una excepción al obtener el cursor: {e}')
    #             sys.exit()
    #     else:
    #         return cls._cursor

if __name__ == '__main__':
    Conexion.obtener_conexion()
    # Conexion.obtenerCursor()
