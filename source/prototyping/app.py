from tkinter import *
from functools import partial
from task_queue import *
from pystray import Menu, MenuItem as item
import pystray

# import json
# import re
from PIL import Image, ImageTk


def process_queue(
    icon, item, queue
):  # SO THIS WAS THE BLOODY PROBLEM, pystray item IS PASSING ITSELF AND ICON INTO THE FUNCTION, EVEN THOUGH IT'S IN A PARTIAL...?
    in_text = pyperclip.paste()
    commands = get_commands()
    pyperclip.copy(
        run_queue(parser(commands[queue.text]), in_text)
    )  # BECAUSE THE SUBMENU ITEMS ARE PASSING THE MENU OBJECTS TO THIS FUNCTION, INSTEAD OF JUST THE STRING NAME OF THE KEY FROM THE DICT, WE NEED TO USE THE .text attr OF MENU OBJ


# I am trying to generate a dropdown menu dynamically which contains the name of the command list and when clicked calls the function which runs said command list.


def hide_window(win, commands):

    submenu = Menu(
        lambda: (item(x, partial(process_queue, commands[x])) for x in commands)
    )  # I DON'T UNDERSTAND WHY BUT THIS IS NOT PASSING X (AS IN THE KEY FROM DICT COMMANDS) TO process_queue, BUT INSTEAD IS PASSING THE MENU OBJECT...
    win.withdraw()
    image = Image.open("favicon.ico")
    menu = (
        item("Editor", partial(show_window, win)),
        # item('Lines: Many to one', lines_many_to_one),#some inbuilt commands do not need chaining if they directly map to a single function (but should we alloW this?)
        item("Tasks:", submenu),
        item("Quit!", quit_window),
    )
    icon = pystray.Icon("name", image, "My System Tray Icon", menu)
    icon.run()


# ===============================================================================
# Define a function for quit the window
def quit_window(icon, item):
    icon.stop()
    win.destroy()


def show_window(icon, item, win):
    icon.stop()
    win.after(0, win.deiconify())


count = 0


def get_commands():  # THIS WILL BE USED TO GET FROM USER SETTINGS
    commands = {
        "TASK1": [
            "LINESMANYTOONE",
            "STRINGTOLIST:,",
            "REMOVEEMPTY",
            "LISTTOSTRING: | ",
        ],
        "TASK2": [
            "LINESMANYTOONE",
            "STRINGTOLIST:,",
            "REMOVEEMPTY",
            "LISTTOSTRING: | ",
        ],
        "TASK3": [
            "LINESMANYTOONE",
            "STRINGTOLIST:,",
            "REMOVEEMPTY",
            "LISTTOSTRING: | ",
        ],
        "TASK4": [
            "STRINGTOLIST:\n",
            "REMOVEEMPTY",
            "LISTTOTABLE",
            "REVERSETABLE",
            "GETCOLUMN:KB",
            "LISTTOSTRING:\n",
        ],
    }
    if count == 3:
        commands["Additional!"] = [
            "LINESMANYTOONE",
            "STRINGTOLIST:,",
            "REMOVEEMPTY",
            "LISTTOSTRING: | ",
        ]
    return commands


def main():
    commands = get_commands()
    lst = ["TASK1", "TASK2", "TASK3", "TASK4"]

    # THE ABOVE IS TO BE REPLACED WITH A USER CONFIG LOADING/SAVING MECHANISM

    win = Tk()

    win.title("Clippy2000")
    # Set the size of the window
    win.geometry("700x350")

    win.protocol(
        "WM_DELETE_WINDOW", partial(hide_window, win, commands)
    )  # when window is closed by user, the hide_window function runs (the systray function)

    win.mainloop()


if __name__ == "__main__":

    main()
