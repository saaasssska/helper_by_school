import sys
# -*- coding: utf-8 -*-
import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QDialog, QVBoxLayout, QPushButton
from PyQt5.QtWidgets import QWidget, QLabel, QCheckBox, QTableWidgetItem


class QNew_teachers(QDialog, QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('frontend/add_teacher.ui', self)
        self.con = sqlite3.connect('db_subjects.db')
        self.update_combo_box()
        self.push_add_subject.clicked.connect(self.add_subject)
        self.push_del_subject.clicked.connect(self.del_subject)
        self.widget = QWidget()
        self.btn_group = []
        self.vbox = QVBoxLayout()
        self.builds = []
        self.subject = []
        self.push_done.clicked.connect(self.all_done)

    def my_builds(self):
        for i in range(len(self.builds)):
            object = QCheckBox(self.builds[i])
            self.btn_group.append(object)
            self.vbox.addWidget(object)
        self.widget.setLayout(self.vbox)
        self.scrollArea.setWidget(self.widget)

    def get_builds(self):
        cur = self.con.cursor()
        self.builds = [i[0] for i in cur.execute("SELECT name FROM builds").fetchall()]
        self.con.commit()
        self.my_builds()

    def update_combo_box(self):
        self.combo_subjects.clear()
        cur = self.con.cursor()
        self.combo_subjects.addItems(
            [i[0] for i in cur.execute("SELECT name FROM my_subjects").fetchall()])

    def add_subject(self):
        sub = self.combo_subjects.currentText()
        self.subject.append([sub])
        self.set_to_file()

    def del_subject(self):
        del_sub = self.combo_subjects.currentText()
        for i in self.subject:
            if i == [del_sub]:
                self.subject.remove(i)
        self.set_to_file()

    def all_done(self):
        name = self.line_name.text()
        surname = self.line_surname.text()
        patronymic = self.line_patronymic.text()
        build = []
        for i in self.btn_group:
            if i.isChecked():
                build.append(i.text())
        if not name.isalnum() or not surname.isalnum() or not patronymic.isalnum():
            self.label_error.setText("Заполните ФИО преподавателя")
        elif len(build) == 0:
            self.label_error.setText("Выберите здание")
        elif len(self.subject) == 0:
            self.label_error.setText("Выберите предмет")
        else:
            cur = self.con.cursor()
            cur.execute('INSERT INTO teachers(surname, name, patronymic) VALUES(?, ?, ?)', [surname, name, patronymic])
            id_teacher = [i[0] for i in cur.execute("SELECT id_teacher FROM teachers WHERE name = ?"
                                                    "AND surname = ? AND patronymic = ?", (name, surname, patronymic,)).fetchall()]
            id_teacher = id_teacher[0]
            self.con.commit()
            for i in build:
                cur.execute('INSERT INTO teacher_builds(id_teacher, build) VALUES(?, ?)', [id_teacher, i])
            self.con.commit()
            for j in self.subject:
                j = j[0]
                cur.execute('INSERT INTO teacher_subjects(id_teacher, subject) VALUES(?, ?)', [id_teacher, j])
            self.con.commit()
            self.label_error.setText("Учитель успешно сохранен")
            self.tableWidget.setColumnCount(0)
            self.tableWidget.setRowCount(0)
            self.line_name.clear()
            self.line_surname.clear()
            self.line_patronymic.clear()
            self.subject = []
            for i in self.btn_group:
                i.setChecked(False)

    def set_to_file(self):
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setHorizontalHeaderLabels(["Предмет"])
        for i, row in enumerate(self.subject):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))

