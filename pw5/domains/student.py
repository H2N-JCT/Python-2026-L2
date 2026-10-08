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