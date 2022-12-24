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

"""
class Window(QDialog):
    def __init__(self):
        super().__init__(parent=None)
        self.setWindowTitle("Task Queue Editor")
        dialogLayout = QVBoxLayout()
        self.formLayout = QFormLayout()

class App():
    pass
    #required functionality:

    #load config
    #save config (config will be handled in task_queue module and called here to keep sepatation between the text processing and config saving, and interface sides)

    #build systray and editor window in qt
    #https://www.pythonguis.com/tutorials/pyqt6-system-tray-mac-menu-bar-applications/
    
    #I am planning to also fork a banch of this project for a CLI tool as well so focus only on GUI interactions
    #loading and saving should only be implemented as a wrapper of the load/save functions from the module

def main():
    print('at least it starts?')
    app = QApplication([])
    app.setQuitOnLastWindowClosed(False)

    # Create the icon
    icon = QIcon("icon.png")

    # Create the tray
    tray = QSystemTrayIcon()
    tray.setIcon(icon)
    tray.setVisible(True)

    # Create the menu
    menu = QMenu()
    action = QAction("A menu item")
    menu.addAction(action)

    # Add a Quit option to the menu.
    quit = QAction("Quit")
    quit.triggered.connect(app.quit)
    menu.addAction(quit)

    # Add the menu to the tray
    tray.setContextMenu(menu)

    sys.exit(app.exec())

if __name__ == '__main__':
    main()
"""
print('at least it starts?')
app = QApplication([])
app.setQuitOnLastWindowClosed(False)

# Create the icon
icon = QIcon("favicon.ico")

# Create the tray
tray = QSystemTrayIcon()
tray.setIcon(icon)
tray.setVisible(True)

# Create the menu
menu = QMenu()
action = QAction("A menu item")
menu.addAction(action)

# Add a Quit option to the menu.
quit = QAction("Quit")
quit.triggered.connect(app.quit)
menu.addAction(quit)

# Add the menu to the tray
tray.setContextMenu(menu)

app.exec()