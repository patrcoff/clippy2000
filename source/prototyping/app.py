#from tkinter import *
from functools import partial
from task_queue import *
import sys
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

#from pystray import Menu, MenuItem as item
#import pystray
#import json
#import re
#from PIL import Image, ImageTk


class App(QMainWindow):
    def __init__(self):
        super(App, self).__init__()
        #,config=Config(pathlib.Path(r'./'))
        self.config = Config(pathlib.Path(r'./'))#will impliment different defaults for different OS's later
        #for now is just the directory it runs from which should be source/prototyping for now

        self.initUI()

    def print_config(self):
        print(self.config.task_queue)

    def load_config():
        pass
    def save_config():
        pass
    #load config
    #save config (config will be handled in task_queue module and called here to keep sepatation between the text processing and config saving, and interface sides)

    #def add_sys_menu(self,menu,tray):

    def initUI(self):#we need to modify this to create our editor window

        icon = QIcon("favicon.ico")
        self.tray = QSystemTrayIcon(self)
        self.tray.setIcon(icon)
        self.m = QMenu()
        
        self.first = QAction('edit menu')
        self.first.triggered.connect(self.onClick)
        self.m.addAction(self.first)
        
        self.second = QAction('refresh tray')
        self.second.triggered.connect(self.refreshTrayMenu)
        self.m.addAction(self.second)
        

        self.tray.setContextMenu(self.m)
        
        self.tray.show()
        textEdit = QTextEdit()
        self.setCentralWidget(textEdit)
        #-----------------------------------------------------------------------
        p = QPushButton("Click Me", self)
        self.setCentralWidget(p)
        p.clicked.connect(self.onClick)

    def onClick(self):
        print('fuck')
        #self.m.clear()
        #use the above if we're building the full menu from scratch (we probably will, unless we can address them by index?)
        #self.m.addAction('First')
        self.m.addAction('Third')
        #self.tray.setContextMenu(self.m)
        #calling setContextMenu multiple times breaks the systray icon for some reason... just don't do it!
    
    def interim(self,var):#testing below functionality before creating intended function to call taskqueue
        print(var)

    def refreshTrayMenu(self):
        
        #firct self.m.clear()
        #then read data structure object containing the list of command queues and their names
        self.objectList = []#have figured out why QAction objects needed to be saved to an attribute of the main object
        #the addAction doesn't pass in a copy of an object, but a reference to an object, so the object (QAction) needs to 
        #keep existing - therefore we cann add these objects to a list which is itself an attribute of self - then they are
        #always available and don't get lost in the method scope
        for taskQueue in self.config.task_queue:#this is only adding the last one, not using self.com doesn't work though
            com = QAction(taskQueue)
            com.triggered.connect(partial(self.interim,taskQueue))
            self.objectList.append(com)
        for i in range(len(self.objectList)):
            self.m.addAction(self.objectList[i])

    def show_win(self):
        self.show()

    #build systray outside of class - doesn't work in class for some reason...
    #https://www.pythonguis.com/tutorials/pyqt6-system-tray-mac-menu-bar-applications/



def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    win = App()
    sys.exit(app.exec())

"""
def main():
    
    #win.print_config()
    app = QApplication([])
    app.setQuitOnLastWindowClosed(False)

    win = App()

    icon = QIcon("favicon.ico")
    tray = QSystemTrayIcon()
    tray.setIcon(icon)
    tray.setVisible(True)

    menu = QMenu()

    action = QAction("A menu item")
    func = partial(add_sys_menu,win,menu,tray)
    action.triggered.connect(func)
    menu.addAction(action)

    # Add a Quit option to the menu.
    quit = QAction("Quit")
    quit.triggered.connect(app.quit)
    menu.addAction(quit)

    tray.setContextMenu(menu)
    app.exec()
"""

if __name__ == '__main__':
    #print('ismain')
    main()
