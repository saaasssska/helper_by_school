import sys
# -*- coding: utf-8 -*-
import sqlite3
from PyQt5 import uic
import csv
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem, QDialog


class QMy_school_plan(QDialog, QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('frontend\School_plan.ui', self)
        self.con = sqlite3.connect('db_subjects.db')
        self.hours = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15']
        self.plan = []
        self.combo_col_lessons.addItems(self.hours)
        self.push_add_lesson.clicked.connect(self.add_lesson)
        self.push_del_lesson.clicked.connect(self.del_lesson)
        self.push_save_plan.clicked.connect(self.save_plan)

    def add_lesson(self):
        lesson = {}
        name = self.comboLessons.currentText()
        col = self.combo_col_lessons.currentText()
        lesson['Наименование'] = name
        lesson['Количество'] = col
        self.combo_del_lesson.setEnabled(True)
        self.plan.append(lesson)
        self.write_lessons()
        self.update_combo_del()

    def del_lesson(self):
        name_lesson = self.combo_del_lesson.currentText()
        for j in self.plan:
            name = j['Наименование']
            if name == name_lesson:
                self.plan.remove(j)

        self.update_combo_del()
        self.write_lessons()

    def update_combo_del(self):
        self.combo_del_lesson.clear()
        lessons = []
        for i in self.plan:
            lessons.append(i['Наименование'])
        self.combo_del_lesson.addItems(lessons)

    def write_lessons(self):
        try:
            row_count = (len(self.plan))
            column_count = (len(self.plan[0]))
            self.tableWidget.setColumnCount(column_count)
            self.tableWidget.setRowCount(row_count)
            self.tableWidget.setHorizontalHeaderLabels((list(self.plan[0].keys())))
            for row in range(row_count):
                for column in range(column_count):
                    item = (list(self.plan[row].values())[column])
                    self.tableWidget.setItem(row, column, QTableWidgetItem(item))
            self.tableWidget.resizeColumnsToContents()
        except Exception:
            self.tableWidget.setHorizontalHeaderLabels(["Предмет", "Количество"])
            self.tableWidget.setColumnCount(2)
            self.tableWidget.setRowCount(0)
            self.tableWidget.resizeColumnsToContents()

    def save_plan(self):
        file_name = self.line_filename.text() + '.csv'
        with open(file_name, 'w', newline='') as csvfile:
            writer = csv.DictWriter(
                csvfile, fieldnames=list(self.plan[0].keys()),
                delimiter=';', quoting=csv.QUOTE_NONNUMERIC)
            writer.writeheader()
            for d in self.plan:
                writer.writerow(d)
        self.line_filename.setText('Файл успешно сохранен')
        self.tableWidget.clear()
        csvfile.close()
        cur = self.con.cursor()
        cur.execute("INSERT INTO files(name) VALUES(?)", [file_name])
        self.con.commit()
        self.plan = []
        self.tableWidget.setHorizontalHeaderLabels(["Предмет", "Количество"])
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(0)
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
