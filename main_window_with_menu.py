import sys
# -*- coding: utf-8 -*-
import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QMenuBar, QAction
from MyBuildings import QMyBuildings
from MyLessons import QMyLessons
from Classes import MyClasses
from School_plan import QMy_school_plan
from change_plans import QChange_plan
from del_classes import My_del_classes
from new_teachers import QNew_teachers
from del_teachers import MyDelTeachers
from create_workload import MyCreate_workload
from definite_teacher import MyDefiniteTeacher
from class_teachers import MyClassTeachers
from workload_problems import MyWorkloadProblems
from export_workload import MyExport_workload
from change_teachers import MyChange_teachers
from hand_schedule import MyHand_schedule
from auto_schedule import MyAuto_schedule
from change_schedule import MyChange_schedule
from del_schedule import MyDel_schedule
from create_choice import MyCreateChoice


class QMainWindow_1(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('frontend\main_window_with_menu.ui', self)
        self.actions()
        self.menus()

    def menus(self):
        menus = QMenuBar(self)
        self.setMenuBar(menus)
        self.build = menus.addMenu('Здания')
        self.build.addAction(self.builds)
        self.school_plan = menus.addMenu('Учебный план')
        self.school_plan.addAction(self.lessons)
        self.school_plan.addAction(self.add_school_plan)
        self.school_plan.addAction(self.change_school_plan)
        self.teachers = menus.addMenu('Учителя')
        self.teachers.addAction(self.add_teachers)
        self.teachers.addAction(self.change_teachers)
        self.teachers.addAction(self.del_teachers)
        self.classes = menus.addMenu('Классы')
        self.classes.addAction(self.add_class)
        self.classes.addAction(self.del_class)
        self.workload = menus.addMenu('Нагрузка учителей')
        self.workload.addAction(self.add_workload)
        self.workload.addAction(self.teacher_workload)
        self.workload.addAction(self.teacher_classes)
        self.workload.addAction(self.problems)
        self.workload.addAction(self.export)
        self.schedule = menus.addMenu('Составить расписание')
        self.schedule.setEnabled(False)
        self.schedule.addAction(self.hand_schedule)
        self.schedule.addAction(self.auto_schedule)
        self.schedule.addAction(self.change_schedule)
        self.schedule.addAction(self.del_schedule)

    def actions(self):
        self.builds = QAction('Здания', self)
        self.builds.triggered.connect(self.my_builds)

        self.lessons = QAction('Предметы', self)
        self.lessons.triggered.connect(self.my_lesson)
        self.add_school_plan = QAction('Создать учебный план', self)
        self.add_school_plan.triggered.connect(self.school_plan)
        self.change_school_plan = QAction('Изменение и удаление учебного плана')
        self.change_school_plan.triggered.connect(self.change_plans)

        self.add_class = QAction('Добавить класс')
        self.add_class.triggered.connect(self.add_classes)
        self.del_class = QAction('Просмотр и удаление классов')
        self.del_class.triggered.connect(self.del_my_classes)

        self.add_teachers = QAction('Добавить учителя')
        self.add_teachers.triggered.connect(self.add_new_teachers)
        self.change_teachers = QAction('Изменение учителей')
        self.change_teachers.triggered.connect(self.change_my_teacher)
        self.del_teachers = QAction('Просмотр и удаление учителей')
        self.del_teachers.triggered.connect(self.del_my_teacher)

        self.add_workload = QAction('Добавить/Рудактировать нагрузку по предмету')
        self.add_workload.triggered.connect(self.new_workload)
        self.teacher_workload = QAction('Нагрузка конкретного учителя')
        self.teacher_workload.triggered.connect(self.load_definite_teacher)
        self.teacher_classes = QAction('Просмотр учителей класса')
        self.teacher_classes.triggered.connect(self.my_classroom_teachers)
        self.problems = QAction('Поиск проблем')
        self.problems.triggered.connect(self.find_workload_problems)
        self.export = QAction('Экспорт нагрузки учителей в word')
        self.export.triggered.connect(self.export_workload_in_word)

        self.hand_schedule = QAction('Ручное составление расписания')
        self.hand_schedule.triggered.connect(self.my_hand_schedule)
        self.auto_schedule = QAction('Автоматическое составление расписания')
        self.auto_schedule.triggered.connect(self.my_auto_schedule)
        self.change_schedule = QAction('Изменение расписания')
        self.change_schedule.triggered.connect(self.my_change_schedule)
        self.del_schedule = QAction('Просмотр и удаление расписания')
        self.del_schedule.triggered.connect(self.my_del_schedule)

    def my_builds(self):
        Buildings = QMyBuildings()
        Buildings.setFixedSize(821, 600)
        Buildings.update_combo_box()
        Buildings.loadTable()
        menu.hide()
        Buildings.exec()
        menu.show()

    def my_lesson(self):
        lessons = QMyLessons()
        menu.hide()
        lessons.exec()
        menu.show()

    def school_plan(self):
        my_school_plan = QMy_school_plan()
        my_school_plan.setFixedSize(821, 600)
        menu.hide()
        con = sqlite3.connect('db_subjects.db')
        my_school_plan.comboLessons.clear()
        cur = con.cursor()
        my_school_plan.comboLessons.addItems(
            [i[0] for i in cur.execute("SELECT name FROM my_subjects").fetchall()])
        my_school_plan.exec()
        menu.show()

    def change_plans(self):
        my_change_plans = QChange_plan()
        my_change_plans.setFixedSize(821, 600)
        menu.hide()
        my_change_plans.tableWidget.setHorizontalHeaderLabels(["Наименование", "Количество"])
        my_change_plans.tableWidget.setColumnCount(2)
        my_change_plans.tableWidget.setRowCount(0)
        my_change_plans.line_new_file.clear()
        con = sqlite3.connect('db_subjects.db')
        my_change_plans.combo_file_name.clear()
        cur = con.cursor()
        my_change_plans.combo_file_name.addItems(
            [i[0] for i in cur.execute("SELECT name FROM files").fetchall()])
        my_change_plans.combo_add_subject.clear()
        my_change_plans.combo_add_subject.addItems(
            [i[0] for i in cur.execute("SELECT name FROM my_subjects").fetchall()])
        my_change_plans.exec()
        menu.show()

    def add_classes(self):
        classes_plans = MyClasses()
        classes_plans.setFixedSize(821, 600)
        menu.hide()
        classes_plans.select_data()
        classes_plans.table_plan.setHorizontalHeaderLabels(["Предмет", "Количество"])
        classes_plans.table_plan.setColumnCount(2)
        classes_plans.table_plan.setRowCount(0)
        classes_plans.update_builds()
        classes_plans.update_school_plans()
        classes_plans.exec()
        menu.show()

    def del_my_classes(self):
        del_class = My_del_classes()
        menu.hide()
        del_class.setFixedSize(821, 600)
        del_class.select_data()
        del_class.update_combo_box()
        del_class.exec()
        menu.show()

    def add_new_teachers(self):
        new_teachers = QNew_teachers()
        new_teachers.setFixedSize(821, 600)
        new_teachers.tableWidget.setColumnCount(0)
        new_teachers.tableWidget.setRowCount(0)
        new_teachers.update_combo_box()
        new_teachers.get_builds()
        menu.hide()
        new_teachers.exec()
        menu.show()

    def change_my_teacher(self):
        change_teacher = MyChange_teachers()
        change_teacher.setFixedSize(821, 600)
        change_teacher.update_combo_box()
        menu.hide()
        change_teacher.exec()
        menu.show()

    def del_my_teacher(self):
        delete_teacher = MyDelTeachers()
        delete_teacher.setFixedSize(821, 600)
        delete_teacher.loadTable()
        delete_teacher.update_combo_box()
        menu.hide()
        delete_teacher.exec()
        menu.show()

    def new_workload(self):
        create_work = MyCreate_workload()
        create_work.setFixedSize(821, 600)
        create_work.update_combo_box()
        create_work.label_save.setText("")
        create_work.tableWidget.setHorizontalHeaderLabels(["Учитель", "Часы"])
        create_work.tableWidget.setColumnCount(2)
        create_work.tableWidget.setRowCount(0)
        menu.hide()
        create_work.exec()
        menu.show()

    def load_definite_teacher(self):
        def_teacher = MyDefiniteTeacher()
        def_teacher.setFixedSize(821, 600)
        def_teacher.update_combo_box()
        menu.hide()
        def_teacher.exec()
        menu.show()

    def my_classroom_teachers(self):
        classroom_teachers = MyClassTeachers()
        classroom_teachers.setFixedSize(821, 600)
        classroom_teachers.label_build.setText("Здание: ")
        classroom_teachers.update_combo_box()
        classroom_teachers.tableWidget.setHorizontalHeaderLabels(["Предмет", "Часы", "Учитель"])
        classroom_teachers.tableWidget.setColumnCount(3)
        classroom_teachers.tableWidget.setRowCount(0)
        menu.hide()
        classroom_teachers.exec()
        menu.show()

    def find_workload_problems(self):
        problems = MyWorkloadProblems()
        problems.setFixedSize(821, 600)
        menu.hide()
        problems.tableWidget.setHorizontalHeaderLabels(["Класс", "Здание", "Предмет", "Статус"])
        problems.tableWidget.setColumnCount(4)
        problems.tableWidget.setRowCount(0)
        problems.exec()
        menu.show()

    def export_workload_in_word(self):
        export = MyExport_workload()
        export.setFixedSize(821, 600)
        export.label_save.setText("")
        menu.hide()
        export.exec()
        menu.show()

    def my_hand_schedule(self):
        hand_sched = MyHand_schedule()
        hand_sched.setFixedSize(821, 600)
        menu.hide()
        hand_sched.exec()
        menu.show()

    def my_auto_schedule(self):
        auto_sched = MyAuto_schedule()
        auto_sched.setFixedSize(821, 600)
        menu.hide()
        auto_sched.exec()
        menu.show()

    def my_change_schedule(self):
        change_sched = MyChange_schedule()
        change_sched.setFixedSize(821, 600)
        menu.hide()
        change_sched.exec()
        menu.show()

    def my_del_schedule(self):
        del_sched = MyDel_schedule()
        del_sched.setFixedSize(821, 600)
        menu.hide()
        del_sched.exec()
        menu.show()

    def closeEvent(self, event):
        reply = QMessageBox.question(
            self, 'Вопрос', 'Точно хотите закрыть?',
            QMessageBox.Yes, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    menu = QMainWindow_1()
    menu.show()
    sys.exit(app.exec())