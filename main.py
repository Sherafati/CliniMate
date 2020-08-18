from PyQt5 import QtCore, QtGui, QtWidgets, QtSql
from form import Ui_MainWindow
from PyQt5.QtCore import QModelIndex
import sqlite3
import sys


class Example(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.createDatabase()

        self.showInfo()

        self.ui.pushButton_AddPatient.clicked.connect(self.add)
        self.ui.pushButton_AddPatient.clicked.connect(self.clearLine)
        self.ui.pushButton_DeletePatient.clicked.connect(self.deleteinfo)
        self.ui.pushButton.clicked.connect(lambda : self.search(self.ui.lineEdit.text()))

        self.ui.pushButton_ShowPAtient.clicked.connect(self.showall)
        self.show()


    def createDatabase(self):
        self.db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('patients.db')
        self.db.open()
        if not self.db.open():
            QtGui.QMessageBox.critical(None, QtGui.qApp.tr("Cannot open database"),
                                       QtGui.qApp.tr("Unable to establish a database connection.\n"
                                                     "This example needs SQLite support. Please read "
                                                     "the Qt SQL driver documentation for information "
                                                     "how to build it.\n\n" "Click Cancel to exit."),
                                       QtGui.QMessageBox.Cancel)

            return False
        query = QtSql.QSqlQuery()
        query.exec_(

        """
        CREATE TABLE  IF NOT EXISTS patients (name VARCHAR, Phone VARCHAR , address TEXT ,date VARCHAR , systemic TEXT ,  treatment VARCHAR, info TEXT,Pay VARCHAR  );
        """
        )



    def clearLine(self):

        self.ui.lineEdit_Name.clear()
        self.ui.lineEdit_Phone.clear()
        self.ui.lineEdit_Address.clear()
        self.ui.lineEdit_Date.clear()
        self.ui.lineEdit_Systemic.clear()
        self.ui.lineEdit_Treatment.clear()
        self.ui.lineEdit_Info.clear()
        self.ui.lineEdit_Pay.clear()


    def add(self):

        record = self.model.record()
        dic = {

            "name": self.ui.lineEdit_Name.text(),
            "phone": self.ui.lineEdit_Phone.text(),
            "address": self.ui.lineEdit_Address.text(),
            "date": self.ui.lineEdit_Date.text(),
            "systemic": self.ui.lineEdit_Systemic.text(),
            "treatment": self.ui.lineEdit_Treatment.text(),
            "info": self.ui.lineEdit_Info.text(),
            "Pay": self.ui.lineEdit_Pay.text()
        }

        for field,value in dic.items():
            index = self.model.fieldIndex(field)
            record.setValue(index,value)
        x = self.model.rowCount()
        self.model.insertRecord(x,record)


        self.model.select()

    def showall(self):

        self.model.setTable('patients')

        

        self.model.select()

    def showInfo(self):


        self.model = MySqlModel()

        self.model.setTable('patients')

        self.ui.tableView.setModel(self.model)
        self.ui.tableView.setSelectionMode(QtWidgets.QTableView.SingleSelection)
        self.ui.tableView.setSelectionBehavior(QtWidgets.QTableView.SelectRows)

        self.model.select()

    def deleteinfo(self):

        current = self.ui.tableView.selectedIndexes()

        for item in current:
              self.model.removeRow(item.row())
        self.model.select()

    def search(self, item):
        self.model.setFilter("name LIKE '%{}%'".format(item))
        self.model.select()


class MySqlModel(QtSql.QSqlTableModel):
    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.TextAlignmentRole:
            return QtCore.Qt.AlignCenter
        return QtSql.QSqlTableModel.data(self,index,role)

    # def closeDatabase(self):
    #
    #     self.ui.tableView.setModel(None)
    #
    #     del self.model
    #
    #     self.db.close()
    #
    #     del self.db
    #
    #     QtSql.QSqlDatabase.removeDatabase("patients")
    #
    # def closeEvent(self, event):
    #
    #     self.closeDatabase()

app = QtWidgets.QApplication(sys.argv)

ex = Example()
sys.exit(app.exec_())

