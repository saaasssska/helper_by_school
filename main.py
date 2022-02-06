import sys
# -*- coding: utf-8 -*-
import sqlite3
from PyQt5.QtWidgets import QApplication
from MainWindow import QMainWindow_1
from MyBuildings import QMyBuildings
from ClassesAndLessons import MyClassesAndLessons
from MyLessons import QMyLessons
from Classes import MyClasses
from School_plan import QMy_school_plan
from change_plans import QChange_plan
from del_classes import My_del_classes
from teachers import QTeachers
from new_teachers import QNew_teachers
from teacher_workload import MyTeacher_workload
from classes_menu import MyClasses_menu
from del_teachers import MyDelTeachers
from create_workload import MyCreate_workload
from definite_teacher import MyDefiniteTeacher
from class_teachers import MyClassTeachers
from workload_problems import MyWorkloadProblems
from export_workload import MyExport_workload
from change_teachers import MyChange_teachers
from make_schedule import MyMake_schedule
from hand_schedule import MyHand_schedule
from auto_schedule import MyAuto_schedule
from change_schedule import MyChange_schedule
from del_schedule import MyDel_schedule


app = QApplication(sys.argv)
menu = QMainWindow_1()
menu.setFixedSize(821, 600)
menu.show()
Mylesson = MyClassesAndLessons()
Buildings = QMyBuildings()
lessons = QMyLessons()
classes_plans = MyClasses()
my_school_plan = QMy_school_plan()
my_change_plans = QChange_plan()
del_class = My_del_classes()
teachers = QTeachers()
new_teachers = QNew_teachers()
workload = MyTeacher_workload()
class_menu = MyClasses_menu()
delete_teacher = MyDelTeachers()

create_work = MyCreate_workload()
def_teacher = MyDefiniteTeacher()
classroom_teachers = MyClassTeachers()
problems = MyWorkloadProblems()
export = MyExport_workload()

change_teacher = MyChange_teachers()

schedule = MyMake_schedule()

hand_sched = MyHand_schedule()
auto_sched = MyAuto_schedule()
change_sched = MyChange_schedule()
del_sched = MyDel_schedule()


def MyBuild():
    Buildings.setFixedSize(821, 600)
    Buildings.update_combo_box()
    Buildings.loadTable()
    menu.hide()
    Buildings.exec()
    menu.show()


def MyLessonsAndClasses():
    Mylesson.setFixedSize(821, 600)
    menu.hide()
    Mylesson.exec()
    menu.show()


def MyLesson():
    lessons.setFixedSize(821, 600)
    Mylesson.setEnabled(False)
    lessons.exec()
    Mylesson.setEnabled(True)


def change_school_plans():
    my_change_plans.setFixedSize(821, 600)
    Mylesson.setEnabled(False)
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
    Mylesson.setEnabled(True)


def add_classes():
    classes_plans.setFixedSize(821, 600)
    Mylesson.setEnabled(False)
    classes_plans.select_data()
    classes_plans.table_plan.setHorizontalHeaderLabels(["Предмет", "Количество"])
    classes_plans.table_plan.setColumnCount(2)
    classes_plans.table_plan.setRowCount(0)
    classes_plans.update_builds()
    classes_plans.update_school_plans()
    classes_plans.exec()
    Mylesson.setEnabled(True)


def school_plans():
    my_school_plan.setFixedSize(821, 600)
    Mylesson.setEnabled(False)
    con = sqlite3.connect('db_subjects.db')
    my_school_plan.comboLessons.clear()
    cur = con.cursor()
    my_school_plan.comboLessons.addItems(
        [i[0] for i in cur.execute("SELECT name FROM my_subjects").fetchall()])
    my_school_plan.exec()
    Mylesson.setEnabled(True)


def del_my_classes():
    Mylesson.setEnabled(False)
    del_class.setFixedSize(821, 600)
    del_class.select_data()
    del_class.update_combo_box()
    del_class.exec()
    Mylesson.setEnabled(True)


def MyTeachers():
    teachers.setFixedSize(821, 600)
    menu.hide()
    teachers.exec()
    menu.show()


def add_teachers():
    new_teachers.setFixedSize(821, 600)
    new_teachers.tableWidget.setColumnCount(0)
    new_teachers.tableWidget.setRowCount(0)
    new_teachers.update_combo_box()
    new_teachers.get_builds()
    teachers.setEnabled(False)
    new_teachers.exec()
    teachers.setEnabled(True)


def Workloads():
    workload.setFixedSize(821, 600)
    menu.hide()
    workload.exec()
    menu.show()


def Classes():
    class_menu.setFixedSize(821, 600)
    menu.hide()
    class_menu.exec()
    menu.show()


def del_my_teacher():
    delete_teacher.setFixedSize(821, 600)
    delete_teacher.loadTable()
    delete_teacher.update_combo_box()
    teachers.setEnabled(False)
    delete_teacher.exec()
    teachers.setEnabled(True)


def new_workload():
    create_work.setFixedSize(821, 600)
    create_work.update_combo_box()
    create_work.label_save.setText("")
    create_work.tableWidget.setHorizontalHeaderLabels(["Учитель", "Часы"])
    create_work.tableWidget.setColumnCount(2)
    create_work.tableWidget.setRowCount(0)
    workload.setEnabled(False)
    create_work.exec()
    workload.setEnabled(True)


def load_definite_teacher():
    def_teacher.setFixedSize(821, 600)
    def_teacher.update_combo_box()
    workload.setEnabled(False)
    def_teacher.exec()
    workload.setEnabled(True)


def my_classroom_teachers():
    classroom_teachers.setFixedSize(821, 600)
    classroom_teachers.label_build.setText("Здание: ")
    classroom_teachers.update_combo_box()
    classroom_teachers.tableWidget.setHorizontalHeaderLabels(["Предмет", "Часы", "Учитель"])
    classroom_teachers.tableWidget.setColumnCount(3)
    classroom_teachers.tableWidget.setRowCount(0)
    workload.setEnabled(False)
    classroom_teachers.exec()
    workload.setEnabled(True)


def find_workload_problems():
    problems.setFixedSize(821, 600)
    workload.setEnabled(False)
    problems.tableWidget.setHorizontalHeaderLabels(["Класс", "Здание", "Предмет", "Статус"])
    problems.tableWidget.setColumnCount(4)
    problems.tableWidget.setRowCount(0)
    problems.exec()
    workload.setEnabled(True)


def export_workload_in_word():
    export.setFixedSize(821, 600)
    export.label_save.setText("")
    workload.setEnabled(False)
    export.exec()
    workload.setEnabled(True)


def change_my_teacher():
    change_teacher.setFixedSize(821, 600)
    change_teacher.update_combo_box()
    teachers.setEnabled(False)
    change_teacher.exec()
    teachers.setEnabled(True)


def make_schedule():
    schedule.setFixedSize(821, 600)
    menu.hide()
    schedule.exec()
    menu.show()


def hand_schedule():
    hand_sched.setFixedSize(821, 600)
    schedule.setEnabled(False)
    hand_sched.exec()
    schedule.setEnabled(True)


def auto_schedule():
    auto_sched.setFixedSize(821, 600)
    schedule.setEnabled(False)
    auto_sched.exec()
    schedule.setEnabled(True)


def change_schedule():
    change_sched.setFixedSize(821, 600)
    schedule.setEnabled(False)
    change_sched.exec()
    schedule.setEnabled(True)


def del_schedule():
    del_sched.setFixedSize(821, 600)
    schedule.setEnabled(False)
    del_sched.exec()
    schedule.setEnabled(True)


menu.push_lessons.clicked.connect(MyLessonsAndClasses)
menu.pushBuild.clicked.connect(MyBuild)
menu.push_teachers.clicked.connect(MyTeachers)
menu.push_teacher_workload.clicked.connect(Workloads)
menu.push_classes.clicked.connect(Classes)
menu.push_make_schedule.clicked.connect(make_schedule)
Mylesson.push_lesson.clicked.connect(MyLesson)
class_menu.push_add_Classes.clicked.connect(add_classes)
Mylesson.create_school_plan.clicked.connect(school_plans)
Mylesson.push_change_plan.clicked.connect(change_school_plans)
class_menu.push_del_classes.clicked.connect(del_my_classes)
teachers.push_add_teacher.clicked.connect(add_teachers)
teachers.push_change_teachers.clicked.connect(change_my_teacher)
teachers.push_del_teacher.clicked.connect(del_my_teacher)
workload.push_create_workload.clicked.connect(new_workload)
workload.push_definite_teacher.clicked.connect(load_definite_teacher)
workload.push_class_teachers.clicked.connect(my_classroom_teachers)
workload.push_find_problems.clicked.connect(find_workload_problems)
workload.push_export_workload.clicked.connect(export_workload_in_word)
schedule.push_hand_schedule.clicked.connect(hand_schedule)
schedule.push_auto_schedule.clicked.connect(hand_schedule)
schedule.push_change_schedule.clicked.connect(change_schedule)
schedule.push_del_schedule.clicked.connect(del_schedule)


sys.exit(app.exec_())

