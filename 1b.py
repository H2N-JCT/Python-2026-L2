class Course:
    def __init__(self):
        self.id = 0
        self.name = ""

    def course_info(self):
        self.id = int(input("course id: "))
        self.name = input("course name: ")

    def __str__(self):
        return f"ID: {self.id} | Name: {self.name}"


class Student:
    def __init__(self):
        self.id = 0
        self.name = ""
        self.dob = ""

    def stu_info(self):
        self.id = int(input("student id: "))
        self.name = input("student name: ")
        self.dob = input("dob: ")

    def __str__(self):
        return f"ID: {self.id} | Name: {self.name} | DoB: {self.dob}"


class Classroom:
    def __init__(self):
        self.students = []
        self.courses = []
        self.marks = {}          # marks[course_id][student_id] = mark

    def inp_stu(self):
        n = int(input("number of students: "))
        for i in range(n):
            print(f"Student {i + 1}:")
            s = Student()
            s.stu_info()
            self.students.append(s)

    def inp_course(self):
        n = int(input("number of courses: "))
        for i in range(n):
            print(f"Course {i + 1}:")
            c = Course()
            c.course_info()
            self.courses.append(c)
            self.marks[c.id] = {}

    def find_course(self, course_id):
        for c in self.courses:
            if c.id == course_id:
                return c
        return None

    def inp_marks(self):
        self.list_courses()
        course = self.find_course(int(input("Select course id: ")))
        if course is None:
            print("Course not found!")
            return
        for s in self.students:
            self.marks[course.id][s.id] = float(input(f"mark of {s.name}: "))

    def list_courses(self):
        print("--- Courses ---")
        for c in self.courses:
            print(c)

    def list_students(self):
        print("--- Students ---")
        for s in self.students:
            print(s)

    def show_marks(self):
        course = self.find_course(int(input("Course id: ")))
        if course is None:
            print("Course not found!")
            return
        print(f"--- Marks for course {course.name} ---")
        for s in self.students:
            print(f"{s.name}: {self.marks[course.id].get(s.id, 'N/A')}")


def main():
    room = Classroom()
    room.inp_stu()
    room.inp_course()

    while True:
        print("\n1. Input marks  2. List courses  3. List students")
        print("4. Show marks   0. Exit")
        choice = input("Choose: ")
        if choice == "1":
            room.inp_marks()
        elif choice == "2":
            room.list_courses()
        elif choice == "3":
            room.list_students()
        elif choice == "4":
            room.show_marks()
        elif choice == "0":
            break
        else:
            print("Invalid choice!")

main()