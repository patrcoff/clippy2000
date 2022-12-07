from tkinter import *
from functools import partial
from task_queue import *
from pystray import Menu, MenuItem as item
import pystray
#import json
#import re
from PIL import Image, ImageTk

commands = {'TASK1':['LINESMANYTOONE','STRINGTOLIST:,','REMOVEEMPTY','LISTTOSTRING: | '],
'TASK2':['LINESMANYTOONE','STRINGTOLIST:,','REMOVEEMPTY','LISTTOSTRING: | '],
'TASK3':['LINESMANYTOONE','STRINGTOLIST:,','REMOVEEMPTY','LISTTOSTRING: | '],
'TASK4':['LINESMANYTOONE','STRINGTOLIST:,','REMOVEEMPTY','LISTTOSTRING: | ']}

#-------------------------------------------------------------------------------
#GUI SECTION

# Create an instance of tkinter frame or window

win=Tk()

win.title("System Tray Application")
# Set the size of the window
win.geometry("700x350")

# Define a function for quit the window
def quit_window(icon, item):
    icon.stop()
    win.destroy()

# Define a function to show the window again
def show_window(icon, item):
    icon.stop()
    win.after(0,win.deiconify())

def test_func(icon,item,queue):#SO THIS WAS THE BLOODY PROBLEM, pystray item IS PASSING ITSELF AND ICON INTO THE FUNCTION, EVEN THOUGH IT'S IN A PARTIAL...?
    in_text = pyperclip.paste()
    pyperclip.copy(run_queue(parser(commands[queue.text]),in_text))#BECAUSE THE SUBMENU ITEMS ARE PASSING THE MENU OBJECTS TO THIS FUNCTION, INSTEAD OF JUST THE STRING NAME OF THE KEY FROM THE DICT, WE NEED TO USE THE .text attr OF MENU OBJ
    #print(type(queue),queue.text)
    #print(commands[queue.text])
lst = ['TASK1','TASK2','TASK3','TASK4']


#I am trying to generate a dropdown menu dynamically which contains the name of the command list and when clicked calls the function which runs said command list.

def hide_window():

    submenu = Menu(lambda: (item(x,partial(test_func,commands[x])) for x in commands))#I DON'T UNDERSTAND WHY BUT THIS IS NOT PASSING X (AS IN THE KEY FROM DICT COMMANDS) TO TEST_FUNC, BUT INSTEAD IS PASSING THE MENU OBJECT...
    win.withdraw()
    image=Image.open("favicon.ico")
    menu=(item('Quit', quit_window),
        #item('Lines: Many to one', lines_many_to_one),#some inbuilt commands do not need chaining if they directly map to a single function (but should we alloW this?)
        item('Tasks:',submenu),
        item('Quit!',quit_window))
    icon=pystray.Icon("name", image, "My System Tray Icon", menu)
    icon.run()


win.protocol('WM_DELETE_WINDOW', hide_window)

win.mainloop()
