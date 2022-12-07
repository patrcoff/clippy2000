from tkinter import *
from functools import partial
#from task_queue import *
from pystray import Menu, MenuItem as item
import pystray
#import json
#import re
from PIL import Image, ImageTk


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

def test_func(icon,item,x):#SO THIS WAS THE BLOODY PROBLEM, pystray item IS PASSING ITSELF AND ICON INTO THE FUNCTION, EVEN THOUGH IT'S IN A PARTIAL...?
    print(x)

lst = ['LINESMANYTOONE','STRINGTOLIST:,','REMOVEEMPTY','LISTTOSTRING: | ']

# Hide the window and show on the system taskbar
#func_lst = [item(x,partial(test_func,x) for x in lst]
#menu2 = tuple(func_lst)


#THIS IS NOT YET WORKING AS INTENDED
#I am trying to generate a dropdown menu dynamically which contains the name of the command list and when clicked calls the function which runs said command list.
#currently trying to make a proof of concept outside of the task_queue (hence commented out import) and just get the menu items to print the sting from a list
#but it is instead printing all the items in the list, 5 times over...
#there's only 4 items in the list too so I really don't understand why, the menu dropdown labels are correctly showing only once
#documentation seems to sparse for this specific intended use case, may require to use a different library
#next thing I'm going to try and do is disregard the below and try and get a dict of key;value pairs, where value is a callable and just manually call these values by key reference to ensure I'm understanding the lambda part ok

"""
def generate_funcs_dict(lst):
    dict = {}
    for el in lst:
        print(el)
        new_lam = partial(test_func,el)
        dict[el] = new_lam
    return dict

print(dict)

functions = generate_funcs_dict(lst)


tmp = functions['LINESMANYTOONE']
input()
tmp()

print("------------------------------------\n\n\n")

for el in functions:
    functions[el]()
print("------------------------------------\n\n\n")
"""
#lst_funcs = [partial(test_func,x) for x in lst]

#print(lst_funcs)

#for el in lst_funcs:
#    el()
#items = tuple(item(x,partial(test_func,x)) for x in lst)
submenu = Menu(lambda: (item(x,partial(test_func,x)) for x in lst))
def hide_window():

    win.withdraw()
    image=Image.open("favicon.ico")
    menu=(item('Quit', quit_window),
        #item('Lines: Many to one', lines_many_to_one),#some inbuilt commands do not need chaining if they directly map to a single function (but should we allo this?)
        item('Tasks:',submenu))#WE NEED TO MAKE A DROP DOWN LIST OF COMMANDS AVAILABLE IN THE available_commands DICT  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    icon=pystray.Icon("name", image, "My System Tray Icon", menu)
    icon.run()


#disregard below! (the below does work but now we got above to work)
#I'm not really sure what got it working but I think it was setting submenu outside of the menu declaration so we passed a full (something) to the item entry for 'Tasks'
#plus the addition of passing icon and item to the function I'm calling - probably something to do with decorators inside the menu class or some shit?

"""
#the below works! it seems pystray is using a slightly different object for systray menu items as passed to icon, and submenu items as called as Menu objects
#I'm able to use a list here of the functions mapped to the command string as menu expects and iterable
#in the above, when trying to create a sub menu, it doesn't work this way though, not expecting an iterable for a Menu object... perhaps if I make a list of menu objects?
def hide_window():
    win.withdraw()
    image=Image.open("favicon.ico")
    #WE NEED TO MAKE A DROP DOWN LIST OF COMMANDS AVAILABLE IN THE available_commands DICT  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    pystray.Icon("name", image, "My System Tray Icon", menu=[item(x,partial(test_func,x)) for x in lst]).run()
    #icon.run()
"""
win.protocol('WM_DELETE_WINDOW', hide_window)

win.mainloop()
