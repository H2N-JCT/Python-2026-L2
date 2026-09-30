import curses
import math
import numpy as np


class UI:
    def __init__(self, scr):
        self.scr = scr
        curses.curs_set(0)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLUE)   # tiêu đề
        curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)    # câu hỏi
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)     # lỗi
        curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)   # thành công
        self.row = 0

    def title(self, text):
        self.scr.clear()
        _, w = self.scr.getmaxyx()
        self.scr.addstr(0, 0, text.center(w - 1), curses.color_pair(1) | curses.A_BOLD)
        self.row = 2

    def line(self, text="", color=0):
        h, w = self.scr.getmaxyx()
        if self.row >= h - 1:  # hết chỗ thì không in nữa
            return
        self.scr.addstr(self.row, 2, text[:w - 4], curses.color_pair(color))
        self.row += 1

    def ask(self, prompt):
        h, w = self.scr.getmaxyx()
        if self.row >= h - 1:  # hết chỗ thì xoá màn hình, in từ đầu
            self.title("")
        self.scr.addstr(self.row, 2, prompt, curses.color_pair(2))
        curses.echo()
        curses.curs_set(1)
        s = self.scr.getstr(self.row, 2 + len(prompt), 40).decode("utf-8").strip()
        curses.noecho()
        curses.curs_set(0)
        self.row += 1
        return s

    def wait(self):
        self.line("")
        self.line("Press any key to continue...")
        self.scr.refresh()
        self.scr.getch()


class Course:
    def __init__(self):
        self.id = 0
        self.name = ""
        self.credits = 0

    def course_info(self, ui):
        self.id = int(ui.ask("course id: "))
        self.name = ui.ask("course name: ")
        self.credits = int(ui.ask("credits: "))

    def __str__(self):
        return f"ID: {self.id} | Name: {self.name} | Credits: {self.credits}"


class Student:
    def __init__(self):
        self.id = 0
        self.name = ""
        self.dob = ""

    def stu_info(self, ui):
        self.id = int(ui.ask("student id: "))
        self.name = ui.ask("student name: ")
        self.dob = ui.ask("dob: ")

    def __str__(self):
        return f"ID: {self.id} | Name: {self.name} | DoB: {self.dob}"


class Classroom:
    def __init__(self):
        self.students = []
        self.courses = []
        self.marks = {}          # marks[course_id][student_id] = mark

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
            self.marks[course.id][s.id] = math.floor(mark * 10) / 10   # round-down 1 chữ số lẻ
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

    # ---------- GPA + sort (numpy) ----------
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
        self.students = [self.students[i] for i in np.argsort(-gpas)]   # giảm dần
        ui.title("STUDENTS SORTED BY GPA (DESC)")
        for s in self.students:
            ui.line(f"{s.name}: {self.gpa(s):.1f}")
        ui.wait()


def main(scr):
    ui = UI(scr)
    room = Classroom()
    room.inp_stu(ui)
    room.inp_course(ui)

    while True:
        ui.title("STUDENT MARK MANAGEMENT")
        ui.line("1. Input marks")
        ui.line("2. List courses")
        ui.line("3. List students")
        ui.line("4. Show marks")
        ui.line("5. Sort students by GPA")
        ui.line("0. Exit")
        choice = ui.ask("Choose: ")
        if choice == "1":
            room.inp_marks(ui)
        elif choice == "2":
            room.list_courses(ui)
        elif choice == "3":
            room.list_students(ui)
        elif choice == "4":
            room.show_marks(ui)
        elif choice == "5":
            room.sort_by_gpa(ui)
        elif choice == "0":
            break
        else:
            ui.line("Invalid choice!", 3)
            ui.wait()


curses.wrapper(main)