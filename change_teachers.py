import sys
# -*- coding: utf-8 -*-
import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QDialog, QTableWidgetItem


class MyChange_teachers(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('frontend\change_teachers.ui', self)
        self.con = sqlite3.connect('db_subjects.db')
        self.push_apply.clicked.connect(self.apply)
        self.push_add_subject.clicked.connect(self.add_subject)
        self.push_del_subject.clicked.connect(self.del_subject)
        self.push_add_build.clicked.connect(self.add_build)
        self.push_del_build.clicked.connect(self.del_build)
        self.push_done.clicked.connect(self.all_done)

    def add_subject(self):
        subject = self.combo_subjects.currentText()
        id_teacher = self.get_id()
        cur = self.con.cursor()
        cur.execute("""INSERT INTO teacher_subjects(id_teacher, subject) VALUES(?, ?)""",
                                [id_teacher, subject])
        self.con.commit()
        self.load_subjects(id_teacher)

    def del_subject(self):
        subject = self.combo_subjects.currentText()
        id_teacher = self.get_id()
        cur = self.con.cursor()
        cur.execute("""DELETE from teacher_subjects
                    WHERE id_teacher = ? AND subject = ?""", [id_teacher, subject])
        self.con.commit()
        self.load_subjects(id_teacher)

    def add_build(self):
        build = self.combo_builds.currentText()
        id_teacher = self.get_id()
        cur = self.con.cursor()
        cur.execute("""INSERT INTO teacher_builds(id_teacher, build) VALUES(?, ?)""",
                        [id_teacher, build])
        self.con.commit()
        self.load_builds(id_teacher)

    def del_build(self):
        build = self.combo_builds.currentText()
        id_teacher = self.get_id()
        cur = self.con.cursor()
        cur.execute("""DELETE from teacher_builds
                        WHERE id_teacher = ? AND build = ?""", [id_teacher, build])
        self.con.commit()
        self.load_builds(id_teacher)

    def apply(self):
        id_teacher = self.get_id()
        self.load_subjects(id_teacher)
        self.load_builds(id_teacher)
        self.push_add_subject.setEnabled(True)
        self.push_del_subject.setEnabled(True)
        self.push_add_build.setEnabled(True)
        self.push_del_build.setEnabled(True)
        self.combo_subjects.setEnabled(True)
        self.combo_builds.setEnabled(True)

    def get_id(self):
        full_name = self.combo_full_name.currentText().split()
        cur = self.con.cursor()
        id_teacher = [i[0] for i in cur.execute("SELECT id_teacher from teachers "
                                                "WHERE surname = ? AND name = ? AND patronymic = ?", full_name)]
        id_teacher = id_teacher[0]
        return id_teacher

    def load_subjects(self, id_teacher):
        cur = self.con.cursor()
        subjects = [list(i) for i in cur.execute("""SELECT subject from teacher_subjects
                                            WHERE id_teacher = ?""", [id_teacher])]
        self.tableSubjects.setColumnCount(1)
        self.tableSubjects.setRowCount(0)
        self.tableSubjects.setHorizontalHeaderLabels(["Предмет"])
        for i, row in enumerate(subjects):
            self.tableSubjects.setRowCount(
                self.tableSubjects.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableSubjects.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        self.tableSubjects.resizeColumnsToContents()

    def load_builds(self, id_teacher):
        cur = self.con.cursor()
        builds = [list(i) for i in cur.execute("""SELECT build from teacher_builds
                                            WHERE id_teacher = ?""", [id_teacher])]
        self.tableBuilds.setColumnCount(1)
        self.tableBuilds.setRowCount(0)
        self.tableBuilds.setHorizontalHeaderLabels(["Здание"])
        for i, row in enumerate(builds):
            self.tableBuilds.setRowCount(
                self.tableBuilds.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableBuilds.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        self.tableBuilds.resizeColumnsToContents()

    def update_combo_box(self):
        cur = self.con.cursor()
        self.combo_full_name.clear()
        self.combo_subjects.clear()
        self.combo_builds.clear()
        teachers = [' '.join(i) for i in cur.execute("""SELECT surname, name, patronymic from teachers""")]
        self.combo_full_name.addItems(teachers)
        subjects = [i[0] for i in cur.execute("""SELECT name from my_subjects""")]
        self.combo_subjects.addItems(subjects)
        builds = [i[0] for i in cur.execute("""SELECT name from builds""")]
        self.combo_builds.addItems(builds)

    def all_done(self):
        self.tableSubjects.setHorizontalHeaderLabels(["Предмет"])
        self.tableSubjects.setColumnCount(1)
        self.tableSubjects.setRowCount(0)

        self.tableBuilds.setHorizontalHeaderLabels(["Здание"])
        self.tableBuilds.setColumnCount(1)
        self.tableBuilds.setRowCount(0)

        self.push_add_subject.setEnabled(False)
        self.push_del_subject.setEnabled(False)
        self.push_add_build.setEnabled(False)
        self.push_del_build.setEnabled(False)
        self.combo_subjects.setEnabled(False)
        self.combo_builds.setEnabled(False)
