import sys
import sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.display_table()

    def display_table(self):
        con = sqlite3.connect("coffee.sqlite")
        cur = con.cursor()
        result = list(cur.execute("Select * From coffee").fetchall())
        con.close()

        self.tableWidget.setColumnCount(len(result[0]))
        self.tableWidget.setRowCount(len(result))
        self.titles = [description[0] for description in cur.description]
        self.tableWidget.setHorizontalHeaderLabels(self.titles)
        for i, row in enumerate(result):
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()

    def except_hook(cls, exception, traceback):
            sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())