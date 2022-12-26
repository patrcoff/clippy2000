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
        super().__init__()
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

    def initUI(self):#we need to modify this to create our editor window

        textEdit = QTextEdit()
        self.setCentralWidget(textEdit)

        exitAct = QAction(QIcon('exit24.png'), 'Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(self.close)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAct)

        toolbar = self.addToolBar('Exit')
        toolbar.addAction(exitAct)

        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('Main window')
        #self.show()
        #don't show on start
    
    #def show_win(self):
     #   self.show()

    #build systray outside of class - doesn't work in class for some reason...
    #https://www.pythonguis.com/tutorials/pyqt6-system-tray-mac-menu-bar-applications/



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
    action.triggered.connect(win.show)
    menu.addAction(action)

    # Add a Quit option to the menu.
    quit = QAction("Quit")
    quit.triggered.connect(app.quit)
    menu.addAction(quit)

    tray.setContextMenu(menu)
    app.exec()

if __name__ == '__main__':
    print('ismain')
    main()
