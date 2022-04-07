import sys
# -*- coding: utf-8 -*-
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, \
    QDialog, QWidget, QVBoxLayout, QCheckBox, QGridLayout, QPushButton, QLabel, QComboBox, QLineEdit, QTextEdit
import sqlite3


class MyHand_schedule(QDialog, QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('frontend\hand_schedule.ui', self)
        self.push_filters.clicked.connect(self.all_done)
        self.con = sqlite3.connect('db_subjects.db')
        self.update_combo_box()
        #self.combo_day.setEnabled(False)

    def all_done(self):
        create = MyCreateChoice(self.combo_subject.currentText())
        create.move(100, 100)
        create.exec()

    def update_combo_box(self):
        global lessons, days
        cur = self.con.cursor()
        builds = [i[0] for i in cur.execute('SELECT name from builds')]
        self.combo_builds.addItems(builds)
        lessons = [i[0] for i in cur.execute('SELECT name from my_subjects')]
        self.combo_subject.addItems(lessons)


class MyCreateChoice(MyHand_schedule):
    def __init__(self, subject):
        self.subject = subject
        super().__init__()
        uic.loadUi('frontend\create_choice.ui', self)
        self.names = []
        self.lenn = 0
        teacher = []
        self.setFixedSize(1200, 900)
        self.con = sqlite3.connect('db_subjects.db')
        self.make_shablon()

    def make_shablon(self):
        cur = self.con.cursor()
        id = [i[0] for i in cur.execute('SELECT id_teacher from teacher_subjects WHERE subject = ?', [self.subject])]
        for i in id:
            teacher = [' '.join(j) for j in cur.execute('SELECT surname, name, patronymic from teachers '
                                  'WHERE id_teacher = ?', [i])]
            if teacher:
                self.names.append(teacher[0])
                for i in range(6):
                    self.names.append(' ')
                self.lenn += 1
        print(teacher)
        self.draw_pictures()


    def draw_pictures(self):
        grid = QGridLayout()
        self.setLayout(grid)

        positions = [(i, j) for i in range(self.lenn + 1) for j in range(7)]
        for position, name in zip(positions, self.names):
            if name == '':
                continue
            if position[1] == 0:
                label = QLabel(name)
                grid.addWidget(label, *position)
            else:
                box = QComboBox()
                cur = self.con.cursor()
                classes = [' '.join(j) for j in cur.execute('SELECT class from teacher_workload WHERE subject = ?', [self.subject])]
                box.addItems(classes)
                grid.addWidget(box, *position)


