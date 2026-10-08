import curses

from domains.classroom import Classroom
from output import UI


def main(scr):
    ui = UI(scr)
    room = Classroom()

    loaded = room.load_compressed()
    if not loaded:
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
            room.save_compressed()   # nén trước khi thoát
            break
        else:
            ui.line("Invalid choice!", 3)
            ui.wait()


curses.wrapper(main)