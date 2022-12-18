from tkinter import *
#from tkinter import ttk
from tkinter import simpledialog
from functools import partial
from task_queue import *
from pystray import Menu, MenuItem as item
import pystray
#import json
#import re
from PIL import Image, ImageTk


class App():

    def __init__(self,debug=False):
        self.debug = debug#not currently passed to functions!
        self.count = 0
        self.win=Tk()

        self.win.title("Clippy2000")
        # Set the size of the window
        self.win.geometry("700x350")
        self.commands = {'TASK1':['LINESMANYTOONE','STRINGTOLIST:,','REMOVEEMPTY','LISTTOSTRING: | '],
        'CodefromRP':['STRINGTOLIST:\n','FOREACH','REMOVE:>>> ','REMOVE:... ','ENDFOR','LISTTOSTRING:\n'],#this is for copying code from realpython where lines start with the repl >>> and ... symbols
        'TASK3':['LINESMANYTOONE','STRINGTOLIST:,','REMOVEEMPTY','LISTTOSTRING: | '],
        'TASK4':['STRINGTOLIST:\n','REMOVEEMPTY','LISTTOTABLE','REVERSETABLE','GETCOLUMN:KB','LISTTOSTRING:\n']}

    def process_queue(self,queue_ref,icon,item):#SO THIS WAS THE BLOODY PROBLEM, pystray item IS PASSING ITSELF AND ICON INTO THE FUNCTION, EVEN THOUGH IT'S IN A PARTIAL...?
        in_text = pyperclip.paste()
        #commands = self.get_commands()
        pyperclip.copy(run_queue(parser(self.commands[queue_ref]),in_text,debug=self.debug))


    def quit_window(self,icon,item):
        self.icon.stop()
        self.win.destroy()

    def show_window(self,icon,item):#the main GUI window is configured here
        self.icon.stop()
        #let's add the GUI command editor here -------------------||
        for widget in self.win.winfo_children():#clear the window
            widget.destroy()
        #then we'd add the widgets needed to edit the command queues

        #GET COMMANDS FROM FILE
        #skip for now

        #DROPDOWN LIST OF COMMANDS
        coms = list(self.commands.keys())
        clicked = StringVar()
        clicked.set(coms[0])
        label = Label(self.win,text=clicked.get())#the view below the dropdown and button
        def refresh_list(selected):
            label.config(text=self.commands[selected])
        commands_list = OptionMenu(self.win,clicked,*coms,command=refresh_list)#https://www.geeksforgeeks.org/dropdown-menus-tkinter/


        #ADD A NEW OPTION TO THE LIST OF COMMAND CHAINS
        def add_option():
            USER_INP = simpledialog.askstring(title="New command queue:",prompt="Enter unique name for command queue:")
            print(USER_INP)
            self.commands[USER_INP] = []
            #self.quit_window(icon,item)
            self.show_window(icon,item)
        add_option_btn = Button(self.win,text='New',command = add_option)

        #----------------------------------------------


        #VIEWS
        
        commands_list.pack()
        add_option_btn.pack()
        label.pack()

        self.win.after(0,self.win.deiconify())
#-----------------------------------------------------------------------

    def hide_window(self):
        print("Running hide_window")
        self.get_commands()#refresh the commands lists
        submenu = Menu(lambda: (item(x,partial(self.process_queue,x)) for x in self.commands))
        self.win.withdraw()
        image=Image.open("favicon.ico")
        menu=(item('Editor', self.show_window),
            #item('Lines: Many to one', lines_many_to_one),#some inbuilt commands do not need chaining if they directly map to a single function (but should we alloW this?)
            item('Tasks:',submenu),
            item('Quit!',self.quit_window))
        self.icon=pystray.Icon("name", image, "My System Tray Icon", menu)
        self.icon.run()

    def get_commands(self):#THIS WILL BE USED TO GET FROM USER SETTINGS FROM FILE
        #commands = self.commands

        #FOR NOW WE'RE JUST CHECKING IF IT WILL WORK TO EDIT THE SUBMENUS AFTER CLOSNING THE EDITOR EACH TIME
        if self.count == 2:
            print("We've clicking this twice!")
            self.commands['Additional!'] = ['LINESMANYTOONE','STRINGTOLIST:,','REMOVEEMPTY','LISTTOSTRING: | ']
        self.count += 1
        #return self.commands

    def run_app(self):
        #commands = self.get_commands()
        #THE ABOVE IS TO BE REPLACED WITH A USER CONFIG LOADING/SAVING MECHANISM

        self.win.protocol('WM_DELETE_WINDOW', partial(self.hide_window))#when window is closed by user, the hide_window function runs (the systray function)


        self.win.mainloop()


def main():
    app = App(debug=True)
    app.run_app()

if __name__ == '__main__':

    main()
