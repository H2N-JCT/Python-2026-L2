import math
import numpy as np
import os
import zipfile

from .course import Course
from .student import Student

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.join(BASE_DIR, "..")

STUDENTS_TXT = os.path.join(ROOT_DIR, "students.txt")
COURSES_TXT = os.path.join(ROOT_DIR, "courses.txt")
MARKS_TXT = os.path.join(ROOT_DIR, "marks.txt")
DAT_FILE = os.path.join(ROOT_DIR, "students.dat")

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

        with open(os.path.join(ROOT_DIR, "students.txt"), "w") as f:
            for s in self.students:
                f.write(str(s) + "\n")

    def inp_course(self, ui):
        ui.title("INPUT COURSES")
        n = int(ui.ask("number of courses: "))
        for i in range(n):
            ui.title(f"COURSE {i + 1}")
            c = Course()
            c.course_info(ui)
            self.courses.append(c)
            self.marks[c.id] = {}

        with open(os.path.join(ROOT_DIR, "courses.txt"), "w") as f:
            for c in self.courses:
                f.write(str(c) + "\n")

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

        with open(MARKS_TXT, "a") as f:
            f.write(f"--- Course: {course.name} (id={course.id}) ---\n")
            for s in self.students:
                mark = self.marks[course.id].get(s.id, "N/A")
                f.write(f"{s.name}: {mark}\n")

    
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

    def save_compressed(self):
        with zipfile.ZipFile(DAT_FILE, "w", zipfile.ZIP_DEFLATED) as z:
            for path in (STUDENTS_TXT, COURSES_TXT, MARKS_TXT):
                if os.path.exists(path):
                    z.write(path, arcname=os.path.basename(path))

    def load_compressed(self):
        if not os.path.exists(DAT_FILE):
            return False
        with zipfile.ZipFile(DAT_FILE, "r") as z:
            z.extractall(ROOT_DIR)

        self._load_students()
        self._load_courses()
        self._load_marks()
        return True
    
    def _load_students(self):
        self.students = []
        if not os.path.exists(STUDENTS_TXT):
            return
        with open(STUDENTS_TXT, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(" | ")
                s = Student()
                s.id = int(parts[0].split(": ")[1])
                s.name = parts[1].split(": ")[1]
                s.dob = parts[2].split(": ")[1]
                self.students.append(s)
    def _load_courses(self):
        self.courses = []
        self.marks = {}
        if not os.path.exists(COURSES_TXT):
            return
        with open(COURSES_TXT, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(" | ")
                c = Course()
                c.id = int(parts[0].split(": ")[1])
                c.name = parts[1].split(": ")[1]
                c.credits = int(parts[2].split(": ")[1])
                self.courses.append(c)
                self.marks[c.id] = {}

    def _load_marks(self):
        if not os.path.exists(MARKS_TXT):
            return
        name_to_id = {s.name: s.id for s in self.students}
        course_by_name = {c.name: c.id for c in self.courses}
        current_course_id = None

        with open(MARKS_TXT, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                if line.startswith("--- Course:"):
                    # "--- Course: Math (id=1) ---"
                    name = line.split("Course: ")[1].split(" (id=")[0]
                    current_course_id = course_by_name.get(name)
                elif current_course_id is not None and ":" in line:
                    stu_name, mark_str = line.split(":", 1)
                    stu_name = stu_name.strip()
                    mark_str = mark_str.strip()
                    if stu_name in name_to_id and mark_str != "N/A":
                        self.marks[current_course_id][name_to_id[stu_name]] = float(mark_str)