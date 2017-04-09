import curses
from curses import wrapper
from curses.textpad import Textbox, rectangle


def init_screen():
    stdscr = curses.initscr()
    stdscr.keypad(True)
    curses.noecho()
    curses.cbreak()


def fini_screen(stdscr):
    stdscr.keypad(False)
    curses.nocbreak()
    curses.echo()
    curses.endwin()


def screen_size():
    return (curses.LINES, curses.COLS)


def create_win(size):
    x, y, w, h = size
    return curses.newwin(h, w, y, x)


def main(screen):
    screen.clear()
    h, w = screen_size()
    win = create_win((1, 1, int(w/2-1), int(h/2-1)))
    rectangle(screen, 0, 0, int(h/2), int(w/2))
    screen.refresh()
    box = Textbox(win)
    box.edit()
    # win.addstr("asdf")
    # win.getch()


wrapper(main)
