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
        self.combo_day.addItems(['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота'])

    def all_done(self):
        create = MyCreateChoice(self.combo_subject.currentText(), self.combo_day.currentText(), self.combo_builds.currentText())
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
    def __init__(self, subject, day, build):
        self.day = day
        self.subject = subject
        self.build = build
        super().__init__()
        uic.loadUi('frontend\create_choice.ui', self)
        self.names = []
        self.lenn = 0
        teacher = []
        self.setFixedSize(1200, 900)
        self.push_done.clicked.connect(self.all_done)
        self.con = sqlite3.connect('db_subjects.db')
        self.lessons = []
        self.make_shablon()

    def make_shablon(self):
        cur = self.con.cursor()
        id = [i[0] for i in cur.execute('SELECT id_teacher from teacher_subjects WHERE subject = ?', [self.subject])]
        for i in id:
            teacher = [' '.join(j) for j in cur.execute('SELECT surname, name, patronymic from teachers '
                                  'WHERE id_teacher = ?', [i])]
            if teacher:
                self.names.append(teacher[0])
                for i in range(7):
                    self.names.append(' ')
                self.lenn += 1
        self.draw_pictures()


    def draw_pictures(self):
        grid = QGridLayout()
        self.setLayout(grid)

        positions = [(i, j) for i in range(self.lenn + 1) for j in range(8)]
        for position, name in zip(positions, self.names):
            if name == '':
                continue
            if position[1] == 0:
                try:
                    self.lessons.append(elem)
                except:
                    elem = []
                elem = [name]
                cur = self.con.cursor()
                teacher_name = name.split()
                id = list(cur.execute('SELECT id_teacher from teachers WHERE surname = ? AND name = ? AND patronymic = ?',
                                 [teacher_name[0], teacher_name[1], teacher_name[2]]))[0][0]
                label = QLabel(name)
                grid.addWidget(label, *position)

            else:
                box = QComboBox()
                cur = self.con.cursor()
                classes = [' '.join(j) for j in cur.execute('SELECT class from teacher_workload WHERE subject = ? AND id_teacher = ?',
                                                            [self.subject, id])]
                box.addItem('')
                box.addItems(classes)
                grid.addWidget(box, *position)
                elem.append(box)
        self.lessons.append(elem)

    def all_done(self):
        for elem in self.lessons:
            name1 = elem[0]
            for lesson in range(1, len(elem)):
                class1 = elem[lesson].currentText()
                print(class1)
                cur = self.con.cursor()
                if class1:
                    print(name1, self.day, self.subject, lesson, class1)
                    cur.execute('INSERT INTO shedule(teacher, day, subject, lesson, class, build) VALUES (?,?,?,?,?,?)',
                            [name1, self.day, self.subject, lesson, class1, self.build])
                    self.con.commit()





