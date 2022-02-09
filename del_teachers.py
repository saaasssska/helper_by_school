import sys
# -*- coding: utf-8 -*-
from PyQt5 import uic
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QDialog, QTableWidgetItem


class MyDelTeachers(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('frontend/del_teachers.ui', self)
        self.con = sqlite3.connect("db_subjects.db")
        self.push_del_teacher.clicked.connect(self.del_teacher)

    def update_combo_box(self):
        self.combo_SNP.clear()
        cur = self.con.cursor()
        teachers = [list(i) for i in cur.execute("SELECT surname, name, patronymic FROM teachers").fetchall()]
        teachers = [' '.join(i) for i in teachers]
        self.combo_SNP.addItems(teachers)

    def del_teacher(self):
        teacher = self.combo_SNP.currentText().split()
        surname = teacher[0]
        name = teacher[1]
        patronymic = teacher[2]
        cur = self.con.cursor()
        cur.execute("DELETE FROM teachers WHERE name = ?"
                    "AND surname = ? AND patronymic = ?", (name, surname, patronymic,))
        self.con.commit()
        self.update_combo_box()
        self.loadTable()

    def loadTable(self):
        self.tableWidget.setHorizontalHeaderLabels(["Фамилия", "Имя", "Отчество"])
        res = self.con.cursor().execute('SELECT surname, name, patronymic FROM teachers').fetchall()
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()
