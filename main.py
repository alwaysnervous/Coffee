import sqlite3
import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QHeaderView
from PyQt5.uic import loadUi

con = sqlite3.connect('coffee.sqlite')
cursor = con.cursor()


class AddOrEdit(QtWidgets.QMainWindow):
    def __init__(self, parent):
        super().__init__(parent)
        loadUi('addEditCoffeeForm.ui', self)
        self.setup_ui()

    def setup_ui(self):
        self.saveButton.clicked.connect(self.save)

    def save(self):
        id_edit = self.idEdit.text()
        name_edit = self.nameEdit.text()
        roast_level_edit = self.roastLevelEdit.text()
        ground_edit = self.groundEdit.text()
        flavor_description_edit = self.flavorDescriptionEdit.text()
        price_edit = self.priceEdit.text()
        package_volume_edit = self.packageVolumeEdit.text()

        edits = [name_edit, roast_level_edit, ground_edit,
                 flavor_description_edit, price_edit, package_volume_edit,
                 id_edit]

        if not all(edits):
            print('Заполнены не все поля!')
            return

        try:
            id_edit = int(id_edit)
            roast_level_edit = int(roast_level_edit)
            ground_edit = bool(int(ground_edit))
            price_edit = int(price_edit)
            package_volume_edit = int(package_volume_edit)
        except ValueError:
            print('Указана информация с некорректным типом данных!')
            return

        edits = [name_edit, roast_level_edit, ground_edit,
                 flavor_description_edit, price_edit, package_volume_edit,
                 id_edit]

        if id_edit <= 0:
            print('ID должен быть натуральным числом!')
            return

        # заполнены все поля и указана информация с корректными типами данных

        # узнаем, существует ли такой id, и может ли он быть вообще
        query = 'SELECT * FROM coffee WHERE id=?'
        cursor.execute(query, (id_edit,))
        data = cursor.fetchall()

        if data:
            # id существует
            query = """UPDATE coffee 
                       SET name=?, roast_level=?, ground=?, flavor_description=?, price=?, package_volume=?
                       WHERE id=?"""
            cursor.execute(query, edits)
            con.commit()
            self.parent().load_coffee_data()
            self.close()
        else:
            # id не существует
            query = """INSERT INTO coffee (name, roast_level, ground, flavor_description, price, package_volume, id)
                       VALUES (?, ?, ?, ?, ?, ?, ?)"""
            cursor.execute(query, edits)
            con.commit()
            self.parent().load_coffee_data()
            self.close()


class CoffeeApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi('main.ui', self)
        self.load_coffee_data()
        self.setup_ui()

    def setup_ui(self):
        self.addOrEditButton.clicked.connect(self.add_or_edit)

    def add_or_edit(self):
        window = AddOrEdit(self)
        window.show()

    def load_coffee_data(self):
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
