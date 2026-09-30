import math
import numpy as np

from .course import Course
from .student import Student


class Classroom:
    def __init__(self):
        self.students = []
        self.courses = []
        self.marks = {}

    def inp_stu(self, ui):
        ui.title("INPUT STUDENTS")
        n = int(ui.ask("number of students: "))
        for i in range(n):
            ui.title(f"STUDENT {i + 1}")
            s = Student()
            s.stu_info(ui)
            self.students.append(s)

    def inp_course(self, ui):
        ui.title("INPUT COURSES")
        n = int(ui.ask("number of courses: "))
        for i in range(n):
            ui.title(f"COURSE {i + 1}")
            c = Course()
            c.course_info(ui)
            self.courses.append(c)
            self.marks[c.id] = {}

    def find_course(self, course_id):
        for c in self.courses:
            if c.id == course_id:
                return c
        return None

    def inp_marks(self, ui):
        self.list_courses(ui, wait=False)
        course = self.find_course(int(ui.ask("Select course id: ")))
        if course is None:
            ui.line("Course not found!", 3)
            ui.wait()
            return
        for s in self.students:
            mark = float(ui.ask(f"mark of {s.name}: "))
            self.marks[course.id][s.id] = math.floor(mark * 10) / 10
        ui.line("Marks saved!", 4)
        ui.wait()

    def list_courses(self, ui, wait=True):
        ui.title("COURSES")
        for c in self.courses:
            ui.line(str(c))
        if wait:
            ui.wait()

    def list_students(self, ui):
        ui.title("STUDENTS")
        for s in self.students:
            ui.line(f"{s} | GPA: {self.gpa(s):.1f}")
        ui.wait()

    def show_marks(self, ui):
        ui.title("SHOW MARKS")
        course = self.find_course(int(ui.ask("Course id: ")))
        if course is None:
            ui.line("Course not found!", 3)
            ui.wait()
            return
        ui.title(f"MARKS FOR COURSE {course.name}")
        for s in self.students:
            ui.line(f"{s.name}: {self.marks[course.id].get(s.id, 'N/A')}")
        ui.wait()

    def gpa(self, student):
        marks, credits = [], []
        for c in self.courses:
            if student.id in self.marks[c.id]:
                marks.append(self.marks[c.id][student.id])
                credits.append(c.credits)
        if not credits:
            return 0.0
        marks = np.array(marks)
        credits = np.array(credits)
        return float(np.sum(marks * credits) / np.sum(credits))

    def sort_by_gpa(self, ui):
        gpas = np.array([self.gpa(s) for s in self.students])
        self.students = [self.students[i] for i in np.argsort(-gpas)]
        ui.title("STUDENTS SORTED BY GPA (DESC)")
        for s in self.students:
            ui.line(f"{s.name}: {self.gpa(s):.1f}")
        ui.wait()