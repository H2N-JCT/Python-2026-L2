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