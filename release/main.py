import sys
import sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
"""from main2 import Ui_MainWindow_1
from addEditCoffeeForm import Ui_MainWindow_2"""


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        # self.setupUi(self)
        self.setWindowTitle("Капучино")
        self.tableWidget.itemClicked.connect(self.item_changed)
        self.pushButton.clicked.connect(self.count)
        self.pushButton_2.clicked.connect(self.count)
        self.label.setText("")
        self.datem = []
        self.display_table()

    def display_table(self):
        con = sqlite3.connect("coffee.sqlite")
        cur = con.cursor()
        result = list(cur.execute("Select * From coffee").fetchall())
        con.close()

        self.long = len(result[0])
        self.tableWidget.setColumnCount(self.long)
        self.tableWidget.setRowCount(len(result))
        self.titles = [description[0] for description in cur.description]
        self.tableWidget.setHorizontalHeaderLabels(self.titles)
        for i, row in enumerate(result):
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()

    def item_changed(self, item):
        self.datem = []
        for index in range(self.long):
            self.datem.append(self.tableWidget.item(item.row(), index).text())

    def count(self):
        if self.sender().text() == "Добавить":
            self.label.setText("")
            self.widget = FormChage(name_button=self.sender().text(), iks=self)
        elif self.datem:
            self.label.setText("")
            self.widget = FormChage(*self.datem, name_button=self.sender().text(), iks=self)
        else:
            self.label.setText("Элемент не выделен")

    def except_hook(cls, exception, traceback):
            sys.__excepthook__(cls, exception, traceback)


class FormChage(QMainWindow):
    def __init__(self, *inform, name_button, iks):
        self.inform = inform
        self.titles = iks.titles
        self.iks = iks
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        # self.setupUi(self)
        self.pushButton.setText(name_button)
        self.pushButton.clicked.connect(self.count)
        self.setWindowTitle("")
        self.mode = name_button
        if self.mode == "Изменить":
            self.lineEdit.setEnabled(False)
        self.technical_work()
        self.show()

    def technical_work(self):
        if self.mode == "Изменить":
            names_edit = ("", "_2", "_3", "_4", "_5", "_6", "_7")
            just_name = "lineEdit"
            for index, name in enumerate(names_edit):
                full_name = eval("self." + just_name + name)
                full_name.setText(self.inform[index])

    def count(self):
        self.go = True
        names_edit = ("", "_2", "_3", "_4", "_5", "_6", "_7")
        just_name = "lineEdit"
        for index, name in enumerate(names_edit):
            full_name = eval("self." + just_name + name)
            text = full_name.text()
            if not text:
                self.go = False

        if not self.go:
            self.label_8.setText("Заполните ячейки")
        else:
            self.label_8.setText("")
            con = sqlite3.connect("coffee.sqlite")
            cur = con.cursor()
            if self.mode == "Добавить":
                new_titles = []
                for ch, elem in enumerate(self.titles):
                    if ch in (1, 2, 4, 6):
                        new_titles.append('"' + elem + '"')
                    else:
                        new_titles.append(elem)
                line1 = ", ".join(new_titles)
                new_inform = []
                for index, name in enumerate(names_edit):
                    full_name = eval("self." + just_name + name)
                    text = full_name.text()
                    if index in (1, 2, 3, 4, 6):
                        new_inform.append('"' + text + '"')
                    else:
                        new_inform.append(text)

                line2 = ", ".join(new_inform)
                line3 = "INSERT INTO coffee(" + line1 + ") VALUES(" + line2 + ")"
                try:
                    cur.execute(line3)
                    con.commit()
                    con.close()
                    self.iks.display_table()
                    self.close()
                except:
                    self.label_8.setText("Данные некорректны")
            else:
                new_inform = []
                for index, name in enumerate(names_edit):
                    full_name = eval("self." + just_name + name)
                    text = full_name.text()
                    if index in (1, 2, 3, 4, 6):
                        new_inform.append('"' + text + '"')
                    else:
                        new_inform.append(text)
                new_titles = []
                for ch, elem in enumerate(self.titles):
                    if ch in (1, 2, 4, 6):
                        new_titles.append('"' + elem + '"')
                    else:
                        new_titles.append(elem)
                line = ""
                for index in range(1, len(new_titles)):
                    line += new_titles[index] + " = " + new_inform[index]
                    if index + 1 != len(new_titles):
                        line += ", "
                finish_line = "UPDATE coffee SET " + line + " WHERE id = " + str(new_inform[0])
                cur.execute(finish_line)
                con.commit()
                con.close()
                self.iks.display_table()
                self.close()

    def except_hook(cls, exception, traceback):
            sys.__excepthook__(cls, exception, traceback)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())