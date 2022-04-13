# -*- coding: utf-8 -*-
import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem, QDialog


class QMyLessons(QDialog, QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('frontend\MySubjects.ui', self)
        self.con = sqlite3.connect('db_subjects.db')
        self.new_subject.clicked.connect(self.add_subject)
        self.clear_subjects.clicked.connect(self.clear_all)
        self.del_subject.clicked.connect(self.del_subject_name)
        self.subject = []
        self.select_data()
        self.update_combo_box()

    def add_subject(self):
        cur = self.con.cursor()
        yet_yes = [i[0] for i in cur.execute("SELECT name FROM my_subjects").fetchall()]
        self.name = self.lineSubject.text()
        if self.name.isalpha() and self.name not in yet_yes:
            cur.execute("INSERT INTO my_subjects(name) VALUES(?)", [self.name])
            self.con.commit()
            self.select_data()
            self.update_combo_box()
        self.lineSubject.clear()

    def select_data(self):
        res = self.con.cursor().execute('SELECT name FROM my_subjects').fetchall()
        self.tableLessons.setColumnCount(1)
        self.tableLessons.setRowCount(0)
        for i, row in enumerate(res):
            self.tableLessons.setRowCount(
                self.tableLessons.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableLessons.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        self.tableLessons.resizeColumnsToContents()

    def update_combo_box(self):
        self.combo_del_subject.clear()
        cur = self.con.cursor()
        self.combo_del_subject.addItems(
            [i[0] for i in cur.execute("SELECT name FROM my_subjects").fetchall()])

    def clear_all(self):
        cur = self.con.cursor()
        cur.execute('DELETE FROM my_subjects;',)
        self.con.commit()
        self.select_data()
        self.update_combo_box()

    def del_subject_name(self):
        del_subject_name = self.combo_del_subject.currentText()
        cur = self.con.cursor()
        sql_update_query = """DELETE from my_subjects where name = ?"""
        cur.execute(sql_update_query, (del_subject_name,))
        self.con.commit()
        self.select_data()
        self.update_combo_box()

