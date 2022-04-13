import sys
# -*- coding: utf-8 -*-
from PyQt5 import uic
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, \
    QDialog, QGridLayout, QLabel, QComboBox
import sqlite3


class MyChange_color(QDialog, QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('frontend\change_color.ui', self)
        colors = ['Бежевый', 'Бирюзовый', 'Белый', 'Серый', 'Розовый']
        self.combo_color.addItems(colors)
        self.push_apply.clicked.connect(self.apply)

    def apply(self):
        pass