from functools import partial
from task_queue import *
import sys
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

# from platform import platform

# from pystray import Menu, MenuItem as item
# import pystray
# import json
# import re
# from PIL import Image, ImageTk


class App(QMainWindow):
    """
    The main window class for the QT based GUI app of \'clipp2000\' - inherits from QMainWindow

    ...
    Attributes
    ----------
    config : task_queue.Config
        config object of task_queue module which contains saved task queues
    taskQueue : task_queue.TaskQueue
        TaskQueue object which holds the available tasks as well as methods to parse and run task queues
    debug : bool
        Used to determine whether user debug mode is used by TaskQueue object methods
    tray : QSystemTrayIcon
        System tray object from PyQt
    first : QAction
        The first entry in the system tray menu
    last : QAction
        The last entry in the system tray menu
    m : QMenu
        The menu object of the system tray icon
    objectList : list
        A dynamically populated list of QAction menu objects populated from user saved task queues in self.user_config

    Methods
    -------
    load_config()
    """

    def __init__(self):
        super(App, self).__init__()

        self.user_config = UserConfig(pathlib.Path.home() / "Clippy2000")

        self.taskQueue = TaskQueue()
        self.initUI()
        self.debug = True

    def print_config(self):
        print(self.user_config.task_queue)

    def load_config(self):
        self.user_config.load_task_queue()

    def save_config(self):
        self.user_config.save_task_queue()

    def initUI(self):
        # SYSTEM TRAY ------------------------------------------------------------
        icon_path = (
            pathlib.Path(__file__).parent.resolve() / "favicon.ico"
        )  # when we migrate this code out of 'prototyping dir' we will maybe add a module subdir for images etc
        icon = QIcon(f"{icon_path}")
        self.tray = QSystemTrayIcon(self)
        self.tray.setIcon(icon)
        self.m = QMenu()

        self.first = QAction("edit menu")
        self.first.triggered.connect(self.show)
        self.m.addAction(self.first)

        self.last = QAction("refresh tray")
        self.last.triggered.connect(self.refreshTrayMenu)
        self.m.addAction(self.last)

        self.tray.setContextMenu(self.m)
        self.tray.show()

        # ------------------------------------------------------------------------
        # EDITOR WINDOW

        VLayout = QVBoxLayout()
        # HLayout = QHBoxLayout()
        centralWidget = QWidget(self)

        centralWidget.setLayout(VLayout)
        self.keys = [x for x in self.user_config.task_queue]
        self.selected = self.keys[0]
        self.current_taskqueue = [
            x.split(":")[0] for x in self.user_config.task_queue[self.selected]
        ]

        self.dropdown = QComboBox()
        self.dropdown.addItems(self.keys)
        self.dropdown.addItem("ADD NEW")
        self.dropdown.currentTextChanged.connect(self.update_selected)

        VLayout.addWidget(self.dropdown)

        self.MiddleLayout = QVBoxLayout()
        # self.MiddleLayout.addWidget(QLabel(str(self.user_config.task_queue[self.selected])))
        self.refresh_middle_layout()
        VLayout.addLayout(self.MiddleLayout)

        bottomLayout = QHBoxLayout()
        save = QPushButton("SAVE")
        close = QPushButton("EXIT")
        close.clicked.connect(self.close)
        save.clicked.connect(self.save_task_queue)
        bottomLayout.addWidget(save)
        bottomLayout.addWidget(close)

        VLayout.addLayout(bottomLayout)

        self.setCentralWidget(centralWidget)

        # -----------------------------------------------------------------------

    def save_task_queue(self):
        self.user_config.task_queue[self.selected] = self.current_taskqueue
        self.user_config.save_task_queue()

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget() is not None:
                child.widget().deleteLater()
            elif child.layout() is not None:
                self.clear_layout(child.layout())

    def update_selected(
        self, text
    ):  # let's maybe rename this after we add the full window refreshing functionality to reflect changing selected taskqueue in the editor
        self.selected = text
        if text == "ADD NEW":
            pass
            # get user input for name of new task
            # add to user config file and save with contents of one entry
            # set as selected
            # refresh_middle_layout
        else:
            self.current_taskqueue = [
                x.split(":")[0] for x in self.user_config.task_queue[self.selected]
            ]
            self.refresh_middle_layout()
            # print(text)

    def refresh_middle_layout(self):
        # self.MiddleLayout.replaceWidget()
        self.clear_layout(self.MiddleLayout)
        # taskqueue = self.user_config.task_queue[self.selected]
        # for task in taskqueue:
        #    self.MiddleLayout.addWidget(QLabel(task))

        for i in range(len(self.current_taskqueue)):
            row = QHBoxLayout()
            task_selector = QComboBox()
            task_selector.addItems(self.taskQueue.tasks.keys())
            task_selector.setCurrentText(self.current_taskqueue[i])
            task_selector.currentTextChanged.connect(partial(self.task_edited, i))
            row.addWidget(task_selector)
            row.addWidget(QLabel(self.current_taskqueue[i]))
            row.addWidget(QLabel("Something task description text goes here"))
            self.MiddleLayout.addLayout(row)
        # REPLACE ABOVE WITH THE EDITOR VIEW
        # FOR TASK IN TASKQUEUE: ADD ROW WITH TASK SELECTED IN DROPDOWN, 2X VAR ENTRY BOXES
        # TASK DROPDOWN SHOULD HAVE OPTIONS TO ADD A NEW TASK IN THE QUEUE, DELETE THE SELECTED TASK

    def task_edited(self, i, task):
        print(f"{i}:{task}")
        if task == "ADD NEW":
            pass
        else:
            self.current_taskqueue = (
                self.current_taskqueue[:i] + [task] + self.current_taskqueue[i + 1 :]
            )
            self.refresh_middle_layout()

    def refreshMainWindow(self, focus):
        pass

    def run_task_queue(
        self, var
    ):  # testing below functionality before creating intended function to call taskqueue
        # print(var)
        in_text = pyperclip.paste()
        pyperclip.copy(
            self.taskQueue.run_queue(
                self.taskQueue.parser(self.user_config.task_queue[var]),
                in_text,
                debug=self.debug,
            )
        )

    def refreshTrayMenu(self):

        self.m.clear()
        self.m.addAction(self.first)

        # then read data structure object containing the list of command queues and their names
        self.load_config()

        self.objectList = (
            []
        )  # have figured out why QAction objects needed to be saved to an attribute of the main object
        # the addAction doesn't pass in a copy of an object, but a reference to an object, so the object (QAction) needs to
        # keep existing - therefore we cann add these objects to a list which is itself an attribute of self - then they are
        # always available and don't get lost in the method scope
        for (
            taskQueue
        ) in (
            self.user_config.task_queue
        ):  # this is only adding the last one, not using self.com doesn't work though
            com = QAction(taskQueue)
            com.triggered.connect(partial(self.run_task_queue, taskQueue))
            self.objectList.append(com)
        for i in range(len(self.objectList)):
            self.m.addAction(self.objectList[i])
        self.m.addAction(self.last)

    def show_win(self):
        self.show()

    # build systray outside of class - doesn't work in class for some reason...
    # https://www.pythonguis.com/tutorials/pyqt6-system-tray-mac-menu-bar-applications/


def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    win = App()
    sys.exit(app.exec())


if __name__ == "__main__":
    # print('ismain')
    main()
