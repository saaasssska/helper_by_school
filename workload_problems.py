import sys
# -*- coding: utf-8 -*-
import csv
import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QDialog, QTableWidgetItem


class MyWorkloadProblems(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('frontend\workload_problems.ui', self)
        self.class_problems = []
        self.con = sqlite3.connect('db_subjects.db')
        self.push_find_problems.clicked.connect(self.problems)

    def problems(self):
        self.class_problems = []
        cur = self.con.cursor()
        classes = [list(i) for i in cur.execute("""SELECT * from classes""")]
        for i in classes:
            name_class = ''.join(i[0:2])
            filename = i[2]
            build = i[3]
            results = []
            with open(filename, 'r') as f:
                lines = csv.reader(f, delimiter=';')
                for line in lines:
                    results.append(line)
            del results[0]
            for j in results:
                subject = j[0]
                teacher = [i[0] for i in cur.execute("""SELECT id_teacher from teacher_workload
                        WHERE class = ? AND subject = ?""", [name_class, subject])]
                if len(teacher) == 0:
                    self.class_problems.append([name_class, build, subject, "Учитель не выбран"])
        self.load_to_table()

    def load_to_table(self):
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(self.class_problems):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self, 'Вопрос', 'Точно хотите закрыть?',
            QMessageBox.Yes, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
