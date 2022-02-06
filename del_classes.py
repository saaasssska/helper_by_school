import sys
# -*- coding: utf-8 -*-
import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem, QDialog


class My_del_classes(QDialog, QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('frontend/del_classes.ui', self)
        self.con = sqlite3.connect('db_subjects.db')
        self.select_data()
        self.update_combo_box()
        self.push_del_class.clicked.connect(self.del_class)

    def select_data(self):
        con = sqlite3.connect('db_subjects.db')
        res = con.cursor().execute('SELECT * FROM classes').fetchall()
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()

    def update_combo_box(self):
        self.combo_class.clear()
        cur = self.con.cursor()
        classes = [list(i) for i in cur.execute("SELECT number, letter FROM classes").fetchall()]
        classes = [' '.join(i) for i in classes]
        self.combo_class.addItems(classes)

    def del_class(self):
        class_name = self.combo_class.currentText().split()
        num = class_name[0]
        letter = class_name[1]
        cur = self.con.cursor()
        cur.execute("DELETE from classes where number = ? AND letter = ?", [num, letter])
        self.con.commit()
        self.select_data()
        self.update_combo_box()

