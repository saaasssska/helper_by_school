import sys
# -*- coding: utf-8 -*-
import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QDialog, QTableWidgetItem


class MyDefiniteTeacher(QDialog):
    def __init__(self):
        super().__init__()
        self.con = sqlite3.connect('db_subjects.db')
        uic.loadUi('frontend\definite_teacher.ui', self)
        self.workload = []
        self.push_choice_teacher.clicked.connect(self.choice_teacher)
        self.push_del_load.clicked.connect(self.del_load)

    def choice_teacher(self):
        cur = self.con.cursor()
        full_name = self.combo_teacher_full_name.currentText().split()
        id_teacher = [i[0] for i in cur.execute("""SELECT id_teacher from teachers
                                WHERE surname = ? AND name = ? AND patronymic = ?""", full_name)]
        id_teacher = id_teacher[0]
        self.workload = [list(i) for i in cur.execute("""SELECT class, build, subject, hours FROM teacher_workload
                                WHERE id_teacher = ?""", [id_teacher])]
        all_hours = 0
        for i in self.workload:
            all_hours += int(i[-1])
        self.load_to_table(all_hours)
        self.update_classes_and_subjects(id_teacher)

    def update_classes_and_subjects(self, id_teacher):
        cur = self.con.cursor()
        self.combo_class.clear()
        self.combo_subject.clear()
        classes = [i[0] for i in cur.execute("""SELECT class from teacher_workload
                                WHERE id_teacher = ?""", [id_teacher])]
        self.combo_class.addItems(classes)
        subjects = [i[0] for i in cur.execute("""SELECT subject from teacher_workload
                                WHERE id_teacher = ?""", [id_teacher])]
        self.combo_subject.addItems(subjects)


    def del_load(self):
        cur = self.con.cursor()
        class1 = self.combo_class.currentText()
        subject = self.combo_subject.currentText()
        full_name = self.combo_teacher_full_name.currentText().split()
        id_teacher = [i[0] for i in cur.execute("""SELECT id_teacher from teachers
                                        WHERE surname = ? AND name = ? AND patronymic = ?""", full_name)]
        id_teacher = id_teacher[0]
        cur.execute("""DELETE from teacher_workload 
                        WHERE id_teacher = ? AND class = ? AND subject = ?""", [id_teacher, class1, subject])
        self.con.commit()
        self.choice_teacher()

    def load_to_table(self, all_hours):
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(self.workload):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()
        self.label_hours.setText("Общее количество часов: " + str(all_hours))

    def update_combo_box(self):
        self.combo_teacher_full_name.clear()
        cur = self.con.cursor()
        teachers = [" ".join(i) for i in cur.execute("""SELECT 
                                    teachers.surname,
                                    teachers.name,
                                    teachers.patronymic
                                    FROM
                                    teachers
                                    INNER JOIN teacher_workload
                                    ON teachers.id_teacher = teacher_workload.id_teacher;""")]
        self.combo_teacher_full_name.addItems(teachers)


