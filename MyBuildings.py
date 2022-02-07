# -*- coding: utf-8 -*-
import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem, QDialog


class QMyBuildings(QDialog, QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('frontend\MyBuildings.ui', self)
        self.con = sqlite3.connect("db_subjects.db")
        self.push_delBuild.clicked.connect(self.del_build)
        self.push_newBuild.clicked.connect(self.add_build)
        self.clear_all.clicked.connect(self.clear_builds)
        self.update_combo_box()
        self.loadTable()

    def update_combo_box(self):
        cur = self.con.cursor()
        self.comboDelBuild.clear()
        self.comboDelBuild.addItems(
            [i[0] for i in cur.execute("SELECT name FROM builds").fetchall()])

    def del_build(self):
        build = self.comboDelBuild.currentText()
        cur = self.con.cursor()
        sql_update_query = """DELETE from builds where name = ?"""
        cur.execute(sql_update_query, (build,))
        self.con.commit()
        self.loadTable()
        self.update_combo_box()

    def add_build(self):
        name = self.name_biuld.text()
        address = self.address_build.text()
        if not name.isalnum() and not address.isalnum():
            pass
        cur = self.con.cursor()
        if len(name) != 0 and len(address) != 0:
            cur.execute("INSERT INTO builds(name, address) VALUES(?, ?)", [name, address])
        self.con.commit()
        self.loadTable()
        self.name_biuld.clear()
        address = self.address_build.clear()
        self.update_combo_box()

    def loadTable(self):
        res = self.con.cursor().execute('SELECT * FROM builds').fetchall()
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()

    def clear_builds(self):
        cur = self.con.cursor()
        cur.execute('DELETE FROM builds;', )
        self.con.commit()
        self.loadTable()
        self.update_combo_box()

