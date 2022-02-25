import sys
# -*- coding: utf-8 -*-
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, \
    QDialog, QWidget, QVBoxLayout, QCheckBox, QGridLayout, QPushButton, QLabel, QComboBox
import sqlite3


class MyHand_schedule(QDialog, QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('frontend\hand_schedule.ui', self)
        self.push_filters.clicked.connect(self.all_done)
        self.lenn = 0
        self.con = sqlite3.connect('db_subjects.db')
        self.update_combo_box()
        self.combo_file_lessons.setEnabled(False)
        #self.combo_day.setEnabled(False)

    def all_done(self):
        create = MyCreateChoice()
        create.move(100, 100)
        create.exec()

    def update_combo_box(self):
        global lessons, days
        cur = self.con.cursor()
        builds = [i[0] for i in cur.execute('SELECT name from builds')]
        self.combo_builds.addItems(builds)
        lessons = [i[0] for i in cur.execute('SELECT name from my_subjects')]
        self.combo_subject.addItems(lessons)
        days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']
        self.combo_day.addItems(days)


class MyCreateChoice(MyHand_schedule):
    def __init__(self):
        super().__init__()
        uic.loadUi('frontend\create_choice.ui', self)
        self.names = []
        self.con = sqlite3.connect('db_subjects.db')
        self.make_shablon()

    def make_shablon(self):
        cur = self.con.cursor()
        subject = self.combo_subject.currentText()
        print(subject)
        id = [i[0] for i in cur.execute('SELECT id_teacher from teacher_subjects WHERE subject = ?', [subject])]
        print(id)
        for i in id:
            teacher = [' '.join(j) for j in cur.execute('SELECT surname, name, patronymic from teachers '
                                  'WHERE id_teacher = ?', [i])]
            if teacher:
                self.names.append(teacher[0])
                for i in range(8):
                    self.names.append(' ')
                self.lenn += 1
        self.draw_pictures()


    def draw_pictures(self):
        grid = QGridLayout()
        self.setLayout(grid)

        positions = [(i, j) for i in range(self.lenn) for j in range(9)]
        for position, name in zip(positions, self.names):
            if name == '':
                continue
            if position[1] == 0:
                label = QLabel(name)
                grid.addWidget(label, *position)
            else:
                box = QComboBox()
                grid.addWidget(box, *position)

        self.move(300, 150)
        self.setWindowTitle('Макет сетки')
