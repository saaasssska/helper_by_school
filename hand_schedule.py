import sys
# -*- coding: utf-8 -*-
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QDialog, QWidget, QVBoxLayout
from create_choice import MyCreateChoice
import sqlite3


class MyHand_schedule(QDialog, QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('frontend\hand_schedule.ui', self)
        self.push_filters.clicked.connect(self.all_done)
        self.con = sqlite3.connect('db_subjects.db')
        self.update_combo_box()
        self.combo_file_lessons.setEnabled(False)
        self.combo_day.setEnabled(False)
        self.widget = QWidget()
        self.btn_group = []
        self.vbox = QVBoxLayout()

    def all_done(self):
        create = MyCreateChoice()
        create.move(100, 100)
        create.exec()

    def update_combo_box(self):
        cur = self.con.cursor()
        builds = [i[0] for i in cur.execute('SELECT name from builds')]
        self.combo_builds.addItems(builds)
        lessons = [i[0] for i in cur.execute('SELECT name from my_subjects')]
        self.combo_subject.addItems(lessons)
        #days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']
        #self.combo_day.addItems(days)
        teachers = [' '.join(i) for i in cur.execute('SELECT surname, name, patronymic from teachers')]
        self.combo_teachers.addItems(teachers)
