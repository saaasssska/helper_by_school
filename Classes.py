import sys
# -*- coding: utf-8 -*-
import csv
import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem, QDialog


class MyClasses(QDialog, QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('frontend\MyClasses.ui', self)
        self.con = sqlite3.connect('db_subjects.db')
        self.buildss = []
        self.subjects = []
        self.col_lessons = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15']
        self.num = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11']
        self.letters = 'АБВГДЕЖЗИКЛМНОПРСТУФХЦЧШЩЫЭЮЯ'
        self.class_number.addItems(self.num)
        self.class_letter.addItems(list(self.letters))
        self.push_add_class.setEnabled(False)
        self.push_open_plan.clicked.connect(self.open_plan)
        self.push_add_class.clicked.connect(self.add_class)
        self.update_class_teachers()

    def update_builds(self):
        cur = self.con.cursor()
        self.choice_build.clear()
        self.choice_build.addItems(
            [i[0] for i in cur.execute("SELECT name FROM builds").fetchall()])
        self.con.commit()

    def update_school_plans(self):
        self.combo_school_plans.clear()
        cur = self.con.cursor()
        self.combo_school_plans.addItems(
            [i[0] for i in cur.execute("SELECT name FROM files").fetchall()])

    def update_class_teachers(self):
        self.line_class_teacher.clear()
        cur = self.con.cursor()
        FIO = [' '.join(i) for i in self.con.cursor().execute('SELECT surname, name, patronymic FROM teachers').fetchall()]
        print(FIO)
        self.line_class_teacher.addItems(FIO)

    def open_plan(self):
        name = self.combo_school_plans.currentText()
        with open(name, encoding="windows-1251") as csvfile:
            reader = csv.reader(csvfile,
                                delimiter=';', quotechar='"')
            title = next(reader)
            self.table_plan.setColumnCount(len(title))
            self.table_plan.setHorizontalHeaderLabels(title)
            self.table_plan.setRowCount(0)
            for i, row in enumerate(reader):
                self.table_plan.setRowCount(
                    self.table_plan.rowCount() + 1)
                for j, elem in enumerate(row):
                    self.table_plan.setItem(
                        i, j, QTableWidgetItem(elem))
        self.table_plan.resizeColumnsToContents()
        csvfile.close()
        self.push_add_class.setEnabled(True)

    def add_class(self):
        build = self.choice_build.currentText()
        num = self.class_number.currentText()
        letter = self.class_letter.currentText()
        plan = self.combo_school_plans.currentText()
        teacher = self.line_class_teacher.currentText()
        cur = self.con.cursor()
        cur.execute("INSERT INTO classes(number, letter, plan, build, teacher) VALUES(?, ?, ?, ?, ?)", [num, letter, plan, build, teacher])
        self.con.commit()
        self.select_data()

    def select_data(self):
        res = self.con.cursor().execute('SELECT * FROM classes').fetchall()
        self.tableClasses.setColumnCount(5)
        self.tableClasses.setRowCount(0)
        for i, row in enumerate(res):
            self.tableClasses.setRowCount(
                self.tableClasses.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableClasses.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        self.tableClasses.resizeColumnsToContents()
        self.table_plan.setHorizontalHeaderLabels(["Предмет", "Количество"])
        self.table_plan.setColumnCount(2)
        self.table_plan.setRowCount(0)
        self.table_plan.resizeColumnsToContents()
        self.push_add_class.setEnabled(False)



