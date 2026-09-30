import curses


class UI:
    def __init__(self, scr):
        self.scr = scr
        curses.curs_set(0)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLUE)
        curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)
        self.row = 0

    def title(self, text):
        self.scr.clear()
        _, w = self.scr.getmaxyx()
        self.scr.addstr(0, 0, text.center(w - 1), curses.color_pair(1) | curses.A_BOLD)
        self.row = 2

    def line(self, text="", color=0):
        h, w = self.scr.getmaxyx()
        if self.row >= h - 1:
            return
        self.scr.addstr(self.row, 2, text[:w - 4], curses.color_pair(color))
        self.row += 1

    def ask(self, prompt):
        h, w = self.scr.getmaxyx()
        if self.row >= h - 1:
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