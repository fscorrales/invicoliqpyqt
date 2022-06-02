import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableView
from PyQt5.QtSql import QSqlDatabase, QSqlRelation, QSqlRelationalTableModel
from invicoliqpyqt.model.conexion import Conexion

# Type hint for return value
con = Conexion.obtener_conexion()
if not con.open():
    QMessageBox.critical(
        None,
        'QTableView Example - Error!',
        'Database Error: %s' % con.lastError().databaseText(),
    )

# def createConnection() -> bool:
#     # SQLite type database connection instance    
#     con = QSqlDatabase.addDatabase('QSQLITE') 
#     # Connect to the database file
#     con.setDatabaseName('testDB.db')
#     # Show message box when there is a connection issue
#     if not con.open():
#         QMessageBox.critical(
#             None,
#             'QTableView Example - Error!',
#             'Database Error: %s' % con.lastError().databaseText(),
#         )
#         return False
#     return True

# Inherit from QMainWindow
class MainWindow(QMainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)
        # Set the window title
        self.setWindowTitle('QTable Example')
        # Create the model
        # model = QSqlRelationalTableModel(self)
        # # Set the table to display
        # model.setTable('orders')
        # # Set relations for related columns to be displayed
        # model.setRelation(1, QSqlRelation('products', 'ProductID', 'Price'))
        # model.setRelation(2, QSqlRelation('customers', 'CustomerID', 'Customer'))
        # model.setRelation(3, QSqlRelation('products', 'ProductID', 'Product'))
        # model.select()
        # # Setup the view
        # # Create the view = a table widget
        # view = QTableView(self)
        # # Set the data model for table widget
        # # Create the presentation model, which gets data from relational table model
        # #presentation_model = MyTableModel(model)
        # #view.setModel(presentation_model)
        # view.setModel(model)
        # # Adjust column widths to their content
        # view.resizeColumnsToContents()
        # # Add the widget to main window
        # self.setCentralWidget(view)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Open the style sheet file and read it
    with open('static/css/style.css', 'r') as f:
        style = f.read()
    # Set the current style sheet
    app.setStyleSheet(style)

    if not Conexion.obtener_conexion():
        sys.exit(1)
    form = MainWindow()
    form.show()
    app.exec()