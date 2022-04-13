import sys
# -*- coding: utf-8 -*-
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QDialog
import sqlite3


class MyDel_schedule(QDialog, QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('frontend/del_schedule.ui', self)
        self.con = sqlite3.connect('db_subjects.db')
        self.push_done.clicked.connect(self.apply)

    def update_combo_box(self):
        cur = self.con.cursor()
        classes = [i[0] for i in cur.execute('SELECT DISTINCT class FROM shedule')]
        self.combo_class.addItems(classes)
        self.con.commit()

    def apply(self):
        global class1
        class1 = self.combo_class.currentText()
        view_shedule = MyViewShedule()
        view_shedule.setWindowTitle('Просмотр расписания')
        view_shedule.exec()


class MyViewShedule(QDialog, QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('frontend/view_shedule.ui', self)
        self.days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']
        self.con = sqlite3.connect('db_subjects.db')
        self.generate()

    def generate(self):
        cur = self.con.cursor()
        for day in self.days:
            for time in range(1, 9):
                lesson = 'Не указан'
                cur = self.con.cursor()
                s = [i[0] for i in cur.execute('SELECT subject from shedule '
                                'WHERE class = ? AND day = ? AND lesson = ?', [class1, day, time])]
                if s:
                    lesson = s[0]
                if day == 'Понедельник':
                    self.list_monday.addItem(str(time) + ' ' + lesson)
                elif day == 'Вторник':
                    self.list_tuesday.addItem(str(time) + ' ' + lesson)
                elif day == 'Среда':
                    self.list_wednesday.addItem(str(time) + ' ' + lesson)
                elif day == 'Четверг':
                    self.list_thursday.addItem(str(time) + ' ' + lesson)
                elif day == 'Пятница':
                    self.list_friday.addItem(str(time) + ' ' + lesson)
                elif day == 'Суббота':
                    self.list_saturday.addItem(str(time) + ' ' + lesson)





class1 = ''
