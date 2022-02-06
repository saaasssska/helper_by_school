import sys
# -*- coding: utf-8 -*-
from PyQt5 import uic
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QDialog, QTableWidgetItem


class MyClassTeachers(QDialog):
    def __init__(self):
        super().__init__()
        self.con = sqlite3.connect('db_subjects.db')
        uic.loadUi('frontend\class_teachers.ui', self)
        self.push_change.clicked.connect(self.change)
        self.push_del_subject.clicked.connect(self.del_subject)

    def update_combo_box(self):
        cur = self.con.cursor()
        self.combo_classes.clear()
        classes = list(set([i[0] for i in cur.execute("""SELECT class from teacher_workload""")]))
        self.combo_classes.addItems(classes)

    def del_subject(self):
        class1 = self.combo_classes.currentText()
        subject = self.combo_subjects.currentText()
        cur = self.con.cursor()
        cur.execute("""DELETE from teacher_workload
                    WHERE class = ? AND subject = ?""", [class1, subject])
        self.con.commit()
        self.change()

    def change(self):
        cur = self.con.cursor()
        class1 = self.combo_classes.currentText()
        teachers = [list(i) for i in cur.execute("""SELECT subject, hours, id_teacher from teacher_workload
                    WHERE class = ?""", [class1])]
        build = [i[0] for i in cur.execute("""SELECT build from teacher_workload
                    WHERE class = ?""", [class1])]
        try:
            build = build[0]
            self.label_build.setText("Здание: " + build)
        except Exception:
            build = build
            self.label_build.setText("Здание: ")
        for i in teachers:
            id_teacher = i[-1]
            name = [' '.join(i) for i in cur.execute("""SELECT surname, name, patronymic from teachers 
                        WHERE id_teacher = ?""", [id_teacher])]
            i[-1] = name[0]
        self.load_to_table(teachers)
        self.combo_subjects.clear()
        subjects = [i[0] for i in cur.execute("""SELECT subject from teacher_workload
                        WHERE class = ?""", [class1])]
        self.combo_subjects.addItems(subjects)

    def load_to_table(self, teachers):
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(teachers):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()
