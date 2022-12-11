from tkinter import *
from functools import partial
from task_queue import *
from pystray import Menu, MenuItem as item
import pystray
#import json
#import re
from PIL import Image, ImageTk


class App():

    def __init__(self,debug=False):
        self.debug = debug
        self.count = 0
        self.win=Tk()

        self.win.title("Clippy2000")
        # Set the size of the window
        self.win.geometry("700x350")
        self.commands = {'TASK1':['LINESMANYTOONE','STRINGTOLIST:,','REMOVEEMPTY','LISTTOSTRING: | '],
        'TASK2':['LINESMANYTOONE','STRINGTOLIST:,','REMOVEEMPTY','LISTTOSTRING: | '],
        'TASK3':['LINESMANYTOONE','STRINGTOLIST:,','REMOVEEMPTY','LISTTOSTRING: | '],
        'TASK4':['STRINGTOLIST:\n','REMOVEEMPTY','LISTTOTABLE','REVERSETABLE','GETCOLUMN:KB','LISTTOSTRING:\n']}

    def process_queue(self,queue_ref,icon,item):#SO THIS WAS THE BLOODY PROBLEM, pystray item IS PASSING ITSELF AND ICON INTO THE FUNCTION, EVEN THOUGH IT'S IN A PARTIAL...?
        in_text = pyperclip.paste()
        commands = self.get_commands()
        pyperclip.copy(run_queue(parser(commands[queue_ref]),in_text))#BECAUSE THE SUBMENU ITEMS ARE PASSING THE MENU OBJECTS TO THIS FUNCTION, INSTEAD OF JUST THE STRING NAME OF THE KEY FROM THE DICT, WE NEED TO USE THE .text attr OF MENU OBJ


    def quit_window(self,icon,item):
        self.icon.stop()
        self.win.destroy()

    def show_window(self,icon,item):
        self.icon.stop()
        self.win.after(0,self.win.deiconify())

    def hide_window(self,commands):

        submenu = Menu(lambda: (item(x,partial(self.process_queue,x)) for x in commands))#I DON'T UNDERSTAND WHY BUT THIS IS NOT PASSING X (AS IN THE KEY FROM DICT COMMANDS) TO process_queue, BUT INSTEAD IS PASSING THE MENU OBJECT...
        self.win.withdraw()
        image=Image.open("favicon.ico")
        menu=(item('Editor', self.show_window),
            #item('Lines: Many to one', lines_many_to_one),#some inbuilt commands do not need chaining if they directly map to a single function (but should we alloW this?)
            item('Tasks:',submenu),
            item('Quit!',self.quit_window))
        self.icon=pystray.Icon("name", image, "My System Tray Icon", menu)
        self.icon.run()

    def get_commands(self):#THIS WILL BE USED TO GET FROM USER SETTINGS
        #commands = self.commands
        if self.count == 2:
            self.commands['Additional!'] = ['LINESMANYTOONE','STRINGTOLIST:,','REMOVEEMPTY','LISTTOSTRING: | ']
        self.count += 1
        return self.commands

    def run_app(self):
        commands = self.get_commands()
        #THE ABOVE IS TO BE REPLACED WITH A USER CONFIG LOADING/SAVING MECHANISM

        self.win.protocol('WM_DELETE_WINDOW', partial(self.hide_window,commands))#when window is closed by user, the hide_window function runs (the systray function)

        self.win.mainloop()


def main():
    app = App()
    app.run_app()

if __name__ == '__main__':

    main()
