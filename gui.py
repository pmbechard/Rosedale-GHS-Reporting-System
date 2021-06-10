from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput

from main import *

courses_dict = {}
student_grades_dict = {}
class_list = []
course_choice = []
term = ''
comment_dict = {}


class LogInWindow(Screen):
    pass


class CourseSelectionWindow(Screen):
    pass


class GradeSelectionWindow(Screen):
    pass


class CommentSelectionWindow(Screen):
    pass


class WindowManager(ScreenManager):
    pass


class CTReportsApp(App):
    def build(self):
        kv = Builder.load_file('ctreports.kv')
        return kv

    def get_credentials(self):
        username = self.root.ids.login.ids.username.text
        password = self.root.ids.login.ids.password.text
        successful_login = moodle_login(username, password)
        if successful_login:
            self.root.current = "course_select"
            self.root.ids.course_select.ids.welcome_text.text = successful_login
            self.list_available_courses()
        elif not self.root.ids.login.ids.warning_label.text:
            self.root.ids.login.ids.warning_label.color = 1, 0, 0, 1
            self.root.ids.login.ids.warning_label.text = "Invalid login..."

    def list_available_courses(self):
        global courses_dict, term
        courses_dict = course_choices()
        course_list = [x for x in courses_dict.values()]

        course_menu = Spinner(text="Select a course:", values=course_list, size_hint=(None, None), height=35, width=500,
                            pos_hint={"center_x": .5, "center_y": .8})
        self.root.ids.course_select.ids.course_select_layout.add_widget(course_menu)
        self.root.ids["course"] = course_menu

        term_menu = Spinner(text="Select the term:", values=["Midterm", "Final"], size_hint=(None, None),
                            height=35, width=500, pos_hint={"center_x": .5, "center_y": .7})
        self.root.ids.course_select.ids.course_select_layout.add_widget(term_menu)
        self.root.ids["term"] = term_menu

    def get_class_list(self, course):
        global class_list, courses_dict, student_grades_dict, term
        class_list = class_list_creation(course)
        term = self.root.ids["term"].text
        self.root.current = "grade_select"

        for student in class_list:
            student_grades_dict[class_list.index(student)] = {}
            self.root.ids.grade_select.ids.grade_select_layout.add_widget(Label(text=student, color=(0, 0, 0, 1),
                                                                                size_hint=(None, None),
                                                                                width=200, height=60))
            for i in range(6):
                student_grades_dict[class_list.index(student)][i] = {}
                grade_index = f'r{class_list.index(student)}c{i}'
                grade_field = TextInput(size_hint_y=None, height=40,
                                        pos_hint={'center_x': .5, 'center_y': .5},
                                        write_tab=False, multiline=False, halign='center')
                self.root.ids.grade_select.ids.grade_select_layout.add_widget(grade_field)
                self.root.ids[grade_index] = grade_field

    def save_grades(self):
        self.root.current = "comment_select"
        global class_list, student_grades_dict, comment_dict

        for i in range(len(student_grades_dict)):
            for field in range(6):
                student_grades_dict[i][field] = self.root.ids[f'r{i}c{field}'].text
        comments = comments_options(class_list, student_grades_dict)

        for student in class_list:
            self.root.ids.comment_select.ids.comment_select_layout.add_widget(Label(text=student, color=(0, 0, 0, 1),
                                                                                    size_hint=(None, None),
                                                                                    width=200, height=60))
            comment_1 = Spinner(text="Select a comment:", values=comments[student])
            self.root.ids.comment_select.ids.comment_select_layout.add_widget(comment_1)
            self.root.ids[f"{class_list.index(student)}-comment_1"] = comment_1

            comment_2 = Spinner(text="Select a comment:", values=comments[student])
            self.root.ids.comment_select.ids.comment_select_layout.add_widget(comment_2)
            self.root.ids[f"{class_list.index(student)}-comment_2"] = comment_2

    def submit(self):
        for student in class_list:
            comment_dict[student] = [self.root.ids[f"{class_list.index(student)}-comment_1"].text,
                                     self.root.ids[f"{class_list.index(student)}-comment_2"].text]
        doc_creation(self.root.ids.course.text, class_list, term, student_grades_dict, comment_dict)


if __name__ == '__main__':
    Window.maximize()
    Config.set('graphics', 'window_state', 'maximized')
    Config.set('graphics', 'resizable', False)
    Config.write()
    CTReportsApp().run()
