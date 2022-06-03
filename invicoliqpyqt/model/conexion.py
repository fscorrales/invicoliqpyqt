from PyQt5.QtSql import QSqlDatabase
import sys
from invicoliqpyqt.logger.logger_base import log

class Conexion():
    _DATABASE = 'db/slave.sqlite'
    # _USERNAME = 'postgres'
    # _PASSWORD = 'admin'
    # _DB_PORT = '5432'
    # _HOST = '127.0.0.1'
    _con = None
    # _cursor = None

    def __init__(self) -> None:
        pass

    @classmethod
    def obtener_conexion(cls):
        if cls._con is None:
            try:
                cls._con = QSqlDatabase.addDatabase('QSQLITE')
                cls._con.setDatabaseName(cls._DATABASE)
                log.debug(f'Conexión exitosa: {cls._con}')
                return cls._con
            except Exception as e:
                log.error(f'Ocurrió una excepción al obtener la conexión: {e}')
                sys.exit()
        else:
            return cls._con

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
