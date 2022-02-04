import sys
# -*- coding: utf-8 -*-
from PyQt5 import uic
import sqlite3
import csv
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem, QDialog


class QChange_plan(QDialog, QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('frontend\change_plan.ui', self)
        self.con = sqlite3.connect('db_subjects.db')
        self.combo_col_lessons.addItems(['1', '2', '3', '4', '5', '6', '7', '8',
                                         '9', '10', '11', '12', '13', '14', '15'])
        self.combo_col_2.addItems(['1', '2', '3', '4', '5', '6', '7', '8',
                                        '9', '10', '11', '12', '13', '14', '15'])
        self.push_open_file.clicked.connect(self.new_file)
        self.push_open_file.clicked.connect(self.open_file)
        self.push_modify.clicked.connect(self.modify_subject)
        self.push_done.clicked.connect(self.done_1)
        self.push_del_subject.clicked.connect(self.del_subject)
        self.push_add_subject.clicked.connect(self.add_subject)
        self.push_done_2.clicked.connect(self.all_done)

    def update_combo_choice(self, name):
        self.combo_choice_subject.clear()
        subjects = []
        with open(name, encoding='windows-1251') as csvfile:
            file_reader = csv.DictReader(csvfile, delimiter=";")
            for row in file_reader:
                subjects.append(row["Наименование"])
        self.combo_choice_subject.addItems(subjects)
        csvfile.close()

    def update_combo_files(self):
        self.combo_file_name.clear()
        cur = self.con.cursor()
        self.combo_file_name.addItems(
            [i[0] for i in cur.execute("SELECT name FROM database").fetchall()])
        self.con.commit()
        self.combo_add_subject.clear()

    def modify_subject(self):
        self.combo_file_name.setEnabled(False)
        self.combo_choice_subject.setEnabled(False)
        self.combo_col_lessons.setEnabled(True)
        self.push_done.setEnabled(True)

    def add_subject(self):
        name = "writer.csv"
        name_subject = self.combo_add_subject.currentText()
        col = self.combo_col_2.currentText()
        r = csv.reader(open(name), delimiter=';', quotechar='"')
        lines = list(r)
        lines.append([name_subject, col])
        self.write_into_file(name, lines)

    def del_subject(self):
        name = "writer.csv"
        name_subject = self.combo_choice_subject.currentText()
        r = csv.reader(open(name), delimiter=';', quotechar='"')
        lines = list(r)
        for i in lines:
            if i[0] == name_subject:
                lines.remove(i)
        self.write_into_file(name, lines)

    def new_file(self):
        name = self.combo_file_name.currentText()
        r = csv.reader(open(name), delimiter=';', quotechar='"')
        lines = list(r)
        with open("writer.csv", "w", newline="") as f:
            writer = csv.writer(f,  delimiter=';', quotechar='"')
            writer.writerows(lines)
        self.combo_col_lessons.setEnabled(False)
        self.push_done.setEnabled(False)
        self.combo_choice_subject.setEnabled(True)
        f.close()

    def open_file(self):
        self.combo_choice_subject.setEnabled(True)
        name = "writer.csv"
        with open("writer.csv", encoding="windows-1251") as csvfile:
            reader = csv.reader(csvfile,
                                delimiter=';', quotechar='"')
            title = next(reader)
            self.tableWidget.setColumnCount(len(title))
            self.tableWidget.setHorizontalHeaderLabels(title)
            self.tableWidget.setRowCount(0)
            for i, row in enumerate(reader):
                self.tableWidget.setRowCount(
                    self.tableWidget.rowCount() + 1)
                for j, elem in enumerate(row):
                    self.tableWidget.setItem(
                        i, j, QTableWidgetItem(elem))
        self.tableWidget.resizeColumnsToContents()
        self.update_combo_choice(name)
        csvfile.close()

    def done_1(self):
        name = "writer.csv"
        name_subject = self.combo_choice_subject.currentText()
        col = self.combo_col_lessons.currentText()
        r = csv.reader(open(name), delimiter=';', quotechar='"')
        lines = list(r)
        for i in range(len(lines)):
            if lines[i][0] == name_subject:
                lines[i][1] = col
        self.combo_file_name.setEnabled(True)
        self.write_into_file(name, lines)

    def write_into_file(self, name, lines):
        with open(name, "w", newline="") as f:
            writer = csv.writer(f, delimiter=';', quotechar='"')
            writer.writerows(lines)
        f.close()
        self.combo_col_lessons.setEnabled(False)
        self.push_done.setEnabled(False)
        self.combo_choice_subject.setEnabled(True)
        self.open_file()

    def all_done(self):
        name = "writer.csv"
        r = csv.reader(open(name), delimiter=';', quotechar='"')
        lines = list(r)
        new_file = self.line_new_file.text()
        if self.radio_this_file.isChecked():
            new_file = self.combo_file_name.currentText()
            name_subject = self.combo_choice_subject.currentText()
            self.write_into_file(new_file, lines)
            self.tableWidget.setHorizontalHeaderLabels(["Наименование", "Количество"])
            self.tableWidget.setColumnCount(2)
            self.tableWidget.setRowCount(0)
            self.tableWidget.resizeColumnsToContents()
            self.line_new_file.setText("Файл успешно сохранен")
        elif ' ' not in new_file:
            new_file = self.line_new_file.text() + '.csv'
            self.write_into_file(new_file, lines)
            self.tableWidget.setHorizontalHeaderLabels(["Наименование", "Количество"])
            self.tableWidget.setColumnCount(2)
            self.tableWidget.setRowCount(0)
            self.tableWidget.resizeColumnsToContents()
            cur = self.con.cursor()
            cur.execute("INSERT INTO files(name) VALUES(?)", [new_file])
            self.con.commit()
            self.update_combo_files()
            self.line_new_file.setText("Файл успешно сохранен")

    def closeEvent(self, event):
        self.con.close()
        reply = QMessageBox.question(
            self, 'Вопрос', 'Точно хотите закрыть?',
            QMessageBox.Yes, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
