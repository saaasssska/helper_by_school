import sys
# -*- coding: utf-8 -*-
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QDialog


class QTeachers(QDialog, QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('frontend/menu_teachers.ui', self)

