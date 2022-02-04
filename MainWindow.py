import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox


class QMainWindow_1(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('frontend\MainWindow.ui', self)

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self, 'Вопрос', 'Точно хотите закрыть?',
            QMessageBox.Yes, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()