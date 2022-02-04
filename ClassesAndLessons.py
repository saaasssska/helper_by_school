import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QDialog


class MyClassesAndLessons(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('frontend\ClasseAndLessons.ui', self)

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self, 'Вопрос', 'Точно хотите закрыть?',
            QMessageBox.Yes, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
