from PyQt5.QtSql import QSqlQuery

def sqlite_unique_value(db_table:str, db_column:str, 
                        search_value) -> bool:
    query = QSqlQuery()
    query.exec_('PRAGMA foreign_keys = ON')
    query.prepare(f'SELECT * FROM {db_table} ' +
                f'WHERE {db_column} = ?')
    query.bindValue(0, search_value)
    result = query.exec_()
    if result and query.first():
        return False
    else:
        return True