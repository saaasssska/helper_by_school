import sys
import sqlite3
# -*- coding: utf-8 -*-
import csv
from PyQt5 import uic
from PyQt5.QtGui import QFontDatabase, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox,\
    QDialog, QWidget, QGridLayout, QComboBox, QLabel, QTableWidgetItem


class MyCreate_workload(QDialog):
    def __init__(self):
        super().__init__()
        self.con = sqlite3.connect("db_subjects.db")
        uic.loadUi('frontend\create_workload.ui', self)
        self.update_combo_box()
        self.widget = QWidget()
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        self.workload = []
        self.names = []
        self.subject = ''
        self.push_apply.clicked.connect(self.apply)
        self.push_done.clicked.connect(self.done_1)
        self.push_change.clicked.connect(self.change)
        self.push_save.clicked.connect(self.save)

    def update_combo_box(self):
        cur = self.con.cursor()
        self.combo_builds.clear()
        self.combo_subjects.clear()
        self.combo_level.clear()
        self.combo_number.clear()
        self.combo_builds.addItems([i[0] for i in cur.execute("SELECT name from builds")])
        self.combo_subjects.addItems([i[0] for i in cur.execute("SELECT name from my_subjects")])
        self.combo_level.addItems(["НОО", "ООО", "СОО"])
        self.combo_number.addItems(["Любая"])
        self.combo_number.addItems(list(set([i[0] for i in cur.execute("SELECT number from classes")])))

    def done_1(self):
        self.push_done.setEnabled(False)
        for i in self.workload:
            teacher, hours = i[-1].currentText(), int(i[-2])
            build = i[1]
            class1 = i[0]
            have = False
            for j in self.names:
                if j[0] == teacher:
                    j[1] += hours
                    have = True
            if not have:
                self.names.append([teacher, hours, build, class1])
        self.scrollArea.setEnabled(False)
        self.push_save.setEnabled(True)
        self.combo_builds.setEnabled(False)
        self.combo_subjects.setEnabled(False)
        self.combo_level.setEnabled(False)
        self.combo_number.setEnabled(False)
        self.push_apply.setEnabled(False)
        self.select_to_table()

    def change(self):
        self.scrollArea.setEnabled(True)
        self.push_save.setEnabled(False)
        self.push_done.setEnabled(True)
        self.combo_builds.setEnabled(True)
        self.combo_subjects.setEnabled(True)
        self.combo_level.setEnabled(True)
        self.combo_number.setEnabled(True)
        self.push_apply.setEnabled(True)
        self.names = []

    def save(self):
        for i in self.names:
            full_name = i[0].split()
            hours = str(i[1])
            build = i[2]
            class1 = i[3]
            surname, name, patronymic = full_name[0], full_name[1], full_name[2]
            cur = self.con.cursor()
            id_teacher = [i[0] for i in cur.execute("SELECT id_teacher from teachers "
                                     "WHERE surname = ? AND name = ? AND patronymic = ?",
                                     [surname, name, patronymic])]
            id_teacher = id_teacher[0]
            cur.execute("INSERT INTO teacher_workload(id_teacher, subject, hours, build, class) "
                        "VALUES(?, ?, ?, ?, ?)", [id_teacher, self.subject, hours, build, class1])
            self.con.commit()
        self.change()
        self.push_save.setEnabled(False)
        self.label_save.setText("Сохранено")
        for i in reversed(range(self.grid.count())):
            self.grid.itemAt(i).widget().deleteLater()

    def select_to_table(self):
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(self.names):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()

    def apply(self):
        self.label_save.setText("")
        self.widget = QWidget()
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        min1, max1 = 0, 0
        num1 = 1
        self.workload = []
        if self.combo_level.currentText() == 'НОО':
            min1, max1 = '1', '4'
        elif self.combo_level.currentText() == 'ООО':
            min1, max1 = '5', '9'
        elif self.combo_level.currentText() == 'СОО':
            min1, max1 = '10', '11'
        self.subject = self.combo_subjects.currentText()
        build = self.combo_builds.currentText()
        if self.combo_number.currentText() != "Любая":
            num = self.combo_number.currentText()
            min1, max1 = str(num), str(num)
        cur = self.con.cursor()
        classes = [list(i) for i in cur.execute("SELECT number, letter, build, plan from classes "
                                          "WHERE number IN (?, ?) AND build = ?", (min1, max1, build,))]
        col = 0
        for class1 in classes:
            cur = self.con.cursor()
            results = []
            with open(class1[3], 'r') as f:
                lines = csv.reader(f, delimiter=';', quotechar='"')
                for line in lines:
                    results.append(line)
                    if line[0] == self.combo_subjects.currentText():
                        col = line[1]
                        break
            if col != 0:
                name_class = ''.join(class1[0:2])
                load = [name_class, build, col]
                self.combo = QComboBox()
                self.combo.setStyleSheet('background-color: rgb(255,255,255);')
                cur = self.con.cursor()
                teachers = [" ".join(i) for i in cur.execute("""SELECT
                 teachers.surname, teachers.name, teachers.patronymic
                 FROM
                 teachers
                 LEFT JOIN teacher_subjects ON teachers.id_teacher = teacher_subjects.id_teacher
                 LEFT JOIN teacher_builds ON teachers.id_teacher = teacher_builds.id_teacher
                 WHERE teacher_subjects.subject = ? AND teacher_builds.build = ?
                 ORDER BY teachers.name;""", (self.subject, build,))]
                self.combo.addItems(teachers)
                positions = [(i, j) for i in range(num1 - 1, num1) for j in range(3)]
                for position, name in zip(positions, load):
                    label = QLabel(name)
                    label.setFont(QFont('Arial', 10))
                    self.grid.addWidget(label, *position)
                self.grid.addWidget(self.combo, num1 - 1, 3)
                self.combo.setFont(QFont("Arial", 10))
                self.widget.setLayout(self.grid)
                self.scrollArea.setWidget(self.widget)
                load.append(self.combo)
                self.workload.append(load)
                num1 += 1
                self.push_done.setEnabled(True)
                self.push_change.setEnabled(True)


