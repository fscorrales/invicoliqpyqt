from PyQt5.QtSql import QSqlQuery


def sqlite_is_unique(db_table: str, field: str,
                    search_value) -> bool:
    query = QSqlQuery()
    query.exec_('PRAGMA foreign_keys = ON')
    query.prepare(f'SELECT * FROM {db_table} ' +
                f'WHERE {field} = ?')
    query.bindValue(0, search_value)
    result = query.exec_()
    if result and query.first():
        return False
    else:
        return True


def sqlite_get_query(db_table: str, field: str,
                    search_value):
    query = QSqlQuery()
    query.prepare(f'SELECT * FROM {db_table} ' +
                f'WHERE {field} = ?')
    query.bindValue(0, search_value)
    result = query.exec_()
    if result and query.first():
        return query
    else:
        return None
