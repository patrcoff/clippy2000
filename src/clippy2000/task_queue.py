from string_converters import *
import pyperclip
from functools import partial
import json
import pathlib


class UserConfig:
    def __init__(self, settings_location=None) -> None:
        self.task_queue = {
            "TASK1": [
                "LINESMANYTOONE",
                "STRINGTOLIST:,",
                "REMOVEEMPTY",
                "LISTTOSTRING: | ",
                "STRIPWHITESPACE",
            ],
            "CodefromRP": [
                "STRINGTOLIST:\n",
                "FOREACH",
                "REMOVE:>>> ",
                "REMOVE:... ",
                "ENDFOR",
                "LISTTOSTRING:\n",
            ],  # this is for copying code from realpython repl blocks where lines start with the repl >>> and ... symbols
            "TASK3": [
                "LINESMANYTOONE",
                "STRINGTOLIST:,",
                "REMOVEEMPTY",
                "LISTTOSTRING: | ",
            ],  # the other two taskqueues here are arbitrary but valid (in terms of input/output datatypes)
        }  # this is where we'll define the built-ins
        # plan is to eventually also impliment:
        # user saved (by json file)
        # app-built-ins (i.e. different UI apps may have different built-ins as per the niche use cases e.g. cli vs gui)
        if settings_location:
            try:
                path = pathlib.Path(settings_location)

                if not path.exists():
                    pathlib.Path(path).mkdir(parents=True)

                self.tq_filepath = path / "user_task_queues.json"
                if (
                    self.tq_filepath.exists()
                ):  # if the file already exists, load the settings from it instead of just using the built-ins
                    self.load_task_queue()
                    # with open(self.tq_filepath, "r") as file:
                    #    self.task_queue = json.load(file)
                else:  # set config file with default task queue hardcoded above (as we've been passed a dir but the file didn't exist yet)
                    self.save_task_queue()
                    # with open(self.tq_filepath, "w") as file:
                    #    json.dump(self.task_queue, file)
            except:
                print("FAILED TO LOAD SETTINGS JSON FILE")
        else:  # defaults to module dir
            self.tq_filepath = (
                pathlib.Path(__file__).parent.resolve() / "user_task_queues.json"
            )
            if (
                self.tq_filepath.exists()
            ):  # if the file already exists, load the settings from it instead of just using the built-ins
                self.load_task_queue()
                # with open(self.tq_filepath, "r") as file:
                #    self.task_queue = json.load(file)
            else:  # set config file with default task queue hardcoded above (as we've been passed a dir but the file didn't exist yet)
                self.save_task_queue()
                # with open(self.tq_filepath, "w") as file:
                #    json.dump(self.task_queue, file)
            # UI can use to then prompt the user for a settings location should they try and save task queues later

    # not decided if below will be kept or not, was thinking for providing method to set filepath on instances of
    # class outside the module i.e. to allow user to set in gui, though this could simply be done by directly accessing attr...
    def set_tq_filepath(self, fp):
        """Takes in a pathlib.filepath object to set tq_filepath attr"""
        self.tq_filepath = fp

    def load_task_queue(self):
        with open(self.tq_filepath, "r") as file:
            self.task_queue = json.load(file)

    def save_task_queue(self):
        with open(self.tq_filepath, "w") as file:
            json.dump(self.task_queue, file)

    # load and save config


class TaskQueue:
    """A class to define the task queue functionality and available tasks."""

    def __init__(self) -> None:
        self.tasks = {  # every task has a a name, function, no of arguments, acceptable input types and output type used for chaining validation
            "STRIPWHITESPACE": {
                "function": strip_whitespace,
                "arguments": 0,
                "input_types": ["string"],
                "output_type": "string",
            },
            "UNESCAPESPECIALS": {"function": unescape_specials, "arguments": 0},
            "EXTRACTINTS": {"function": extract_ints, "arguments": 0},
            "STRINGTOLIST": {"function": string_to_list, "arguments": 1},
            "LINESMANYTOONE": {"function": lines_many_to_one, "arguments": 1},
            "REPLACESTRING": {"function": replace_string, "arguments": 2},
            "LISTTOSTRING": {"function": lst_to_string, "arguments": 1},
            "REMOVEEMPTY": {"function": remove_empty, "arguments": 0},
            "REMOVEY": {"function": remove_y, "arguments": 1},
            "LISTTOTABLE": {"function": list_to_table, "arguments": 1},
            "REVERSETABLE": {"function": reverse_table, "arguments": 0},
            "GETCOLUMN": {"function": get_column, "arguments": 1},
            "FOREACH": {"function": None, "arguments": 0},
            "ENDFOR": {"function": None, "arguments": 0},
        }  # need to define the tasks in this dict

    def valid(self, previous):
        pass
        # function to return available next task in sequence

    def parser(self, coms):
        # the list of commands we take from the User interface  will include psudo-code-like "FOREACH/ENDFOR" commands, similar to jinja etc (but way more simplistic)
        # we  want to be able to perform the tasks between these FOREACH/ENDFOR tags, well, for each element within the input object (be that a list or a string)
        # the simplest way to handle this I could think of was to convert these sections of the command list to sublists within the main command list, rather than handle it at the input level in the UI part
        # I know this uses recursion and that's sometimes controversial but it works here, we're never going to have 1000 nested foor loops in a command list and for this purpose it just makes sense
        # I did not intend on making this eletist or unnessecarily complicated, if you can think of a nicer/simpler/easier to read way to do this with just for loops, let me know!
        out_list = []
        # fortag = False#pretty sure I don't need  this
        sublst = []
        forcount = 0
        for el in coms:
            if el == "FOREACH":
                # fortag = True#pretty sure I don't need  this
                forcount += 1  # using forcount to determine if this is a nested for loop - this is not extensively tested but I think it works
                if forcount > 1:
                    sublst.append(el)
            elif el == "ENDFOR":
                # fortag = False#pretty sure I don't need  this
                forcount -= 1  # using forcount to determine if this is a nested for loop - this is not extensively tested but I think it works
                if forcount == 0:
                    out_list.append(
                        self.parser(sublst)
                    )  # oooooh, recursion!!! (don't worry, it's not that scary, it just makes sense here)
                elif forcount > 0:
                    sublst.append(el)
            elif forcount > 0:
                sublst.append(el)
            else:
                out_list.append(el)
        return out_list

    def count_colons(self, word):
        return word.count(":")

    def call_task(self, task, working_text):
        tasks = self.tasks
        print(f"\ntask: {task} : colons : {self.count_colons(task)}")
        # count number of values passed to task (number of colons)
        if task.split(":")[0] not in tasks.keys():
            print(task, "not in keys!")

        if self.count_colons(task) == 0:
            working_text = tasks[task.split(":")[0]]["function"](working_text)
        elif self.count_colons(task) == 1:
            working_text = tasks[task.split(":")[0]]["function"](
                working_text, task.split(":")[1]
            )
        elif self.count_colons(task) == 2:
            working_text = tasks[task.split(":")[0]]["function"](
                working_text,
                task.split(":")[1],
                task.split(":")[2],
            )
            # else:
            #    print(f'\n\n{task}\n\n')

            """
            print("\nworkingtext:\n", working_text)#why am I using partial here, surely that's not needed? hangover from tkinter implementation from earlier days?
            working_text = partial(
                tasks[task.split(":")[0]]["function"], working_text
            )()
        elif self.count_colons(task) == 1:
            working_text = partial(
                tasks[task.split(":")[0]]["function"], working_text, task.split(":")[1]
            )()
        elif self.count_colons(task) == 2:
            working_text = partial(
                tasks[task.split(":")[0]]["function"],
                working_text,
                task.split(":")[1],
                task.split(":")[2],
            )()
            # need to figure out more complex logic to account for if a passed argument is itself a colon...!
"""

        return working_text
        # this function massively reduces the code needed in run_queue, and is better at DRY
        # however, it has removed the functionality of using named 'arguments' - so the code creating tasks will
        # need to carefully enforce the order of 'arguments' passed to the task
        # i.e. in TASKNAME:arg1:arg2 must match order of the called function

    def run_queue(self, queue, in_text, debug=False):
        # again, we're using recursion (see note at start of parser function)
        # so, from the parsed command list we will have a list potentially containing 'sub lists'
        # each 'sub-list' is our implementation of a FOR-LOOP (from the standpoint of how the user chains 'commands'/'tasks' together)
        # therefore, each time we meet a list (in the commands list), we need to call the commands inside this list on each element of the current state of the text, the end result of which we can then send back to the main command queue
        # (working_text is the current state of what was input and is being processed by commands in the queue - it can actually be a list itself but it helps to just generally think of it as "the clipboard text, mid process")
        # again, recursion makes sense here to me, when processing the 'sub-lists', we need to make use of some sort of stack and a loop, recursion does this by definition and I find this easier than figuring out my own stack mechanism
        # maybe I'm just lazy and should learn more about stacks
        # FYI, I recommend this podcast episode on the subject of recursion - https://open.spotify.com/episode/5iycnoUlDP4TnsUUrqnPXa?si=27bbe6a6761c400a
        # I've not yet read his book on recursion (which is a book about recursion called 'the recusive book of recursion' (which is a book...)) but I likely will at some point.
        # From the podcast I gather it is not a book hailing recursion as a wonderful tool for geniouses but really a scathing review of when not to use it, but often explaining it in more approachable ways.
        # He talks a lot in the podcast about how recursion gets a bad wrap because of the many bad uses of it in tutorials etc. I feel I am though justified for this use of recursion. Rant over.
        working_text = in_text

        # we could replace all of the below with a dict of task names to function references

        for task in queue:
            if isinstance(task, list):
                # this is a FOREACH section, recursively call again on this
                intermediary = []

                for el in working_text:  # where task is a sublist of tasks
                    intermediary.append(
                        self.run_queue(task, el)
                    )  # this is either action on each char or list element, and either outputs a list or string
                    # however, to make it possible to manage, the intermediary is always a list, so if user is not careful, they could get lists of lists
                    # some thought is needed in how to guide the user to avoid this so they don't make broken task queues
                    if debug:
                        print(task, working_text)
                working_text = intermediary
            # --------------------------------------------------------------------------------------
            elif task.split(":")[0] in self.tasks.keys():
                # task is valid, process using dictionary
                working_text = self.call_task(task, working_text)
            # so far we have one command in this new mechanism and if this works, we can start removing the below
            # --------------------------------------------------------------------------------------
            """elif task == "STRIPWHITESPACE":
                working_text = strip_whitespace(working_text)
            elif "STRINGTOLIST" in task:
                splitter = task.split(":")[
                    1
                ]  # we need to add error correction somewhere for if user doesn't supply splitter
                working_text = string_to_list(
                    working_text, splitter
                )  # there will be a separate function though for lines to list, so there will be no default splitter here
                # this will be put in the documentation so user knows they must supply splitter notation (or in GUI it will be required field just
            elif "LISTTOSTRING" in task:  # default joiner is '', :parameter is optional
                if len(task.split(":")) > 1:
                    working_text = lst_to_string(
                        working_text, joiner=task.split(":")[1]
                    )
                else:
                    working_text = lst_to_string(working_text)
            elif "LINESMANYTOONE" in task:
                if len(task.split(":")) > 1:
                    working_text = lines_many_to_one(
                        working_text, separator=task.split(":")[1]
                    )
                else:
                    working_text = lines_many_to_one(
                        working_text
                    )  # default separator is comma to provide csv like output
            elif task == "EXTRACTINTS":
                working_text = extract_ints(
                    working_text
                )  # returns string of ints separated by commas
            elif task == "REMOVEEMPTY":
                working_text = remove_empty(working_text)
            elif task == "UNESCAPESPECIALS":
                working_text = unescape_specials(working_text)
            elif task == "REVERSETABLE":
                # SHOULD ADD SOME ERROR CHECKING HERE!!!
                working_text = reverse_table(working_text)
            elif "REMOVE:" in task:
                if len(task.split(":")) > 1:
                    working_text = remove_y(working_text, task.split(":")[1])
                # should add error checking if :val not passed
            elif "LISTTOTABLE" in task:
                if len(task.split(":")) > 1:
                    working_text = list_to_table(working_text, delim=task.split(":")[1])
                else:
                    working_text = list_to_table(working_text)  # default delim is comma
            elif "GETCOLUMN" in task:
                if len(task.split(":")) > 1:
                    working_text = get_column(working_text, task.split(":")[1])
                else:
                    working_text = list_to_table(
                        working_text, "0"
                    )  # default delim is comma
            #----------------------------------------------------------------------------------------------------------"""

            if debug:
                print(task, working_text)

        return working_text
