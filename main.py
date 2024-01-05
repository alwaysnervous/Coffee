import sqlite3
import sys

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QTableWidgetItem, QHeaderView


class CoffeeApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.load_coffee_data()

    def load_coffee_data(self):
        connection = sqlite3.connect('coffee.sqlite')
        cursor = connection.cursor()

        query = "SELECT * FROM coffee"
        cursor.execute(query)
        coffee_data = cursor.fetchall()

        self.coffeeTable.setRowCount(len(coffee_data))

        for i, elem in enumerate(coffee_data):
            for j, val in enumerate(elem):
                self.coffeeTable.setItem(i, j, QTableWidgetItem(str(val)))

        horizontal_header = self.coffeeTable.horizontalHeader()

        for column_number in range(len(coffee_data[0])):
            horizontal_header.setSectionResizeMode(column_number, QHeaderView.Stretch)

        self.coffeeTable.resizeRowsToContents()

        cursor.close()
        connection.close()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


def main():
    app = QtWidgets.QApplication([])
    window = CoffeeApp()
    window.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
