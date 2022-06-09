import sys
import os
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableView, QLineEdit
from PyQt5.QtSql import QSqlTableModel
from invicoliqpyqt.model.factureros import FacturerosModel


# sys.path.insert(0, dirname(dirname(abspath(__file__))))
# from model.conexion import Conexion

# Type hint for return value
# con = Conexion.obtener_conexion()
# if not con.open():
#     QMessageBox.critical(
#         None,
#         'QTableView Example - Error!',
#         'Database Error: %s' % con.lastError().databaseText(),
#     )

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
        super(MainWindow, self).__init__(parent)
        # Load the ui file
        uic.loadUi(os.path.join(os.path.dirname(__file__), 'main_window.ui'), self)
        # Set the window title
        # Define Our Widgets
        self.table_factureros = self.findChild(QTableView, 'table_factureros')
        # self.setWindowTitle('QTable Example')
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
        # Set up the model
        self.model = QSqlTableModel(self)
        self.model.setTable("factureros")
        # self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model.setHeaderData(0, Qt.Horizontal, "ID")
        self.model.setHeaderData(1, Qt.Horizontal, "Nombre")
        self.model.setHeaderData(2, Qt.Horizontal, "Actividad")
        self.model.setHeaderData(3, Qt.Horizontal, "Partida")
        self.model.select()
        # Set up the view
        self.factureros_model = FacturerosModel(self.model)
        self.table_factureros.setModel(self.factureros_model)
        self.table_factureros.resizeColumnsToContents()
        #self.setCentralWidget(self.table_factureros)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    UIWindow = MainWindow()
    app.exec_()

    # app = QApplication(sys.argv)
    
    # # Open the style sheet file and read it
    # with open('static/css/style.css', 'r') as f:
    #     style = f.read()
    # # Set the current style sheet
    # app.setStyleSheet(style)

    # if not Conexion.obtener_conexion():
    #     sys.exit(1)
    # form = MainWindow()
    # form.show()
    # app.exec_()