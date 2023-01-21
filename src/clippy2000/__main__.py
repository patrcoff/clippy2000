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


        #DEPRECATION NOTICE---------------------------------------------
        #TaskQueue module is to be pulled out into its own separate module, where it will be generalised further
        #to provide similar functionality for different applications
        #user_config will be removed from the TaskQueue module and be instead handled natively in the front end apps themselves
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
        #self.m.addAction(self.last)
        self.refreshTrayMenu()
        self.tray.setContextMenu(self.m)
        self.tray.show()

        # ------------------------------------------------------------------------
        # EDITOR WINDOW

        VLayout = QVBoxLayout()
        # HLayout = QHBoxLayout()
        centralWidget = QWidget(self)

        centralWidget.setLayout(VLayout)
        self.keys = [x for x in self.user_config.task_queue]
        self.selected = self.keys[0]#I don't know why I have done this in two steps?
        self.current_taskqueue = self.user_config.task_queue[self.selected]

        self.dropdown = QComboBox()
        self.dropdown.addItems(self.keys)
        self.dropdown.addItem("ADD NEW")
        self.dropdown.currentTextChanged.connect(self.update_selected)

        delete_btn = QPushButton('DELETE')
        delete_btn.clicked.connect(self.delete_task_queue)

        selected_taskqueue_row = QHBoxLayout()
        selected_taskqueue_row.addWidget(self.dropdown)
        selected_taskqueue_row.addWidget(delete_btn)

        VLayout.addLayout(selected_taskqueue_row)

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

    def delete_task(self,index):
        #should add a check here to see if it is the last item in the task_queue, if so, delete the task_queue instead and chastise user
        #print(index)
        self.current_taskqueue = self.current_taskqueue[:index] + self.current_taskqueue[index +1 :]
        self.save_task_queue()
        self.refresh_middle_layout()

    def delete_task_queue(self):
        name = self.selected
        print(name)
        self.user_config.task_queue.pop(name,None)
        self.save_task_queue()
        self.dropdown.removeItem(self.dropdown.findText(name))#THIS IS NOT HOW REMOVE ITEM WORKS, PROBABLY NEED TO GET THE ITEM FIRST USING REFERENCE TO NAME AND THEN CALL DELETEITEM ON IT
        self.selected = list(self.user_config.task_queue.keys())[0]
        self.dropdown.setCurrentText(self.selected)
        self.refresh_middle_layout()

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
    ):
        
        if text == "ADD NEW":
            # get user input for name of new task
            name, ok = QInputDialog.getText(self,'Input Dialog','Please name your new TaskQueue:')
            # add to user config file and save with contents of one entry
            self.user_config.task_queue[name] = ['DEFAULT']
            #above adds one default task which is a placeholder so we have at minimum 1 task dropdown
            self.user_config.save_task_queue()
            self.dropdown.addItem(name)
            # set as selected
            self.selected = name
            self.current_taskqueue = self.user_config.task_queue[self.selected]
            self.dropdown.setCurrentText(name)
            # refresh_middle_layout
            self.refresh_middle_layout()
        else:
            self.selected = text
            self.current_taskqueue = self.user_config.task_queue[self.selected]
            self.refresh_middle_layout()
            # print(text)

    def refresh_middle_layout(self):
        # self.MiddleLayout.replaceWidget()
        self.clear_layout(self.MiddleLayout)
        # taskqueue = self.user_config.task_queue[self.selected]
        # for task in taskqueue:
        #    self.MiddleLayout.addWidget(QLabel(task))

        #BUILD OUT A ROW FOR EACH TASK IN THE TASK QUEUE------------------------------------------------------|
        for i in range(len(self.current_taskqueue)):
            row = QHBoxLayout()
            task_selector = QComboBox()
            task_selector.addItems(self.taskQueue.tasks.keys())
            task_selector.setCurrentText(self.current_taskqueue[i].split(':')[0])
            task_selector.currentTextChanged.connect(partial(self.task_edited, i))
            
            var_input1 = QLineEdit()
            var_input2 = QLineEdit()
            var_input1.textEdited.connect(partial(self.vars_edited,0,i))
            var_input2.textEdited.connect(partial(self.vars_edited,1,i))

            optional_vars = [var_input1,var_input2]#count how many colons are in the task as these is optional and variable between the different available tasks
            for x in range(self.taskQueue.count_colons(self.current_taskqueue[i])):
                optional_vars[x].setText(self.current_taskqueue[i].split(':')[x+1])
            
            #ADD THE DROPDOWN TASK SELECTOR IN THE ROW
            row.addWidget(task_selector)
            
            #disable the entries which are invalid as per the current task

            if self.taskQueue.tasks[self.current_taskqueue[i].split(':')[0]]['arguments'] == 0:
                optional_vars[0].setDisabled(True)
                optional_vars[1].setDisabled(True)  
                #block out both
            elif self.taskQueue.tasks[self.current_taskqueue[i].split(':')[0]]['arguments'] == 1:
                #block out 1
                optional_vars[1].setDisabled(True)

            row.addWidget(optional_vars[0])
            row.addWidget(optional_vars[1])

            row.addWidget(QLabel("Something task description text goes here"))

            delete = QPushButton('DELETE')
            delete.clicked.connect(partial(self.delete_task,i))
            row.addWidget(delete)

            self.MiddleLayout.addLayout(row)


    def vars_edited(self, var_index, i, text):
        print(f'{i}:{text}')
        #can have 1 argument and this is it
        if self.taskQueue.tasks[self.current_taskqueue[i].split(':')[0]]['arguments'] == 1:
            self.current_taskqueue[i] = self.current_taskqueue[i].split(':')[0] + ':' + text
        #can have 2 arguments and this is the first one
        elif var_index == 0 and self.taskQueue.tasks[self.current_taskqueue[i].split(':')[0]]['arguments'] == 2:
            self.current_taskqueue[i] = self.current_taskqueue[i].split(':')[0] + ':' + text + ':' + self.current_taskqueue[i].split(':')[2]
        #can have 2 arguments and this is the second one
        else:
            self.current_taskqueue[i] = self.current_taskqueue[i].split(':')[0] + ':' + self.current_taskqueue[i].split(':')[1] + ':' + text
        #as we have disabled the var text entries for tasks with 1 or none possible vars
        #we do not need to do any error checking here for tasks with no colons in the text
        #this relies on no part of the code adding in tasks which could have a colon but don't 
        # i.e. any built-ins MUST follow this formatting rule, even if the var is blank

    def task_edited(self, i, task):
        print(f"{i}:{task}")
        if task == "ADD NEW":
            self.current_taskqueue = self.current_taskqueue[:i+1] + ["DEFAULT"] + self.current_taskqueue[i+1:]
            #add a new task of default type in the position i
            self.refresh_middle_layout()
        else:
            task = task + self.taskQueue.tasks[task]['arguments']*':'#this adds a task with the correct number of possible colons
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
        #self.m.addAction(self.last)

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
