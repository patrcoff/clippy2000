from string_converters import *
import pyperclip
#NEED TO CHECK I NEED ALL OF THESE, THEY'VE BEEN COPIED FROM THE PREVIOUS ITERATION OF THIS PROJECT, WHICH ITSELF WAS BASED ON A GUIDE FOR CREATING SYSTEM TRAY TOOLS
#https://www.tutorialspoint.com/how-to-make-a-system-tray-application-in-tkinter


def parser(coms):
    #the list of commands we take from the User interface  will include psudo-code-like "FOREACH/ENDFOR" commands, similar to jinja etc (but way more simplistic)
    #we  want to be able to perform the tasks between these FOREACH/ENDFOR tags, well, for each element within the input object (be that a list or a string)
    #the simplest way to handle this I could think of was to convert these sections of the command list to sublists within the main command list, rather than handle it at the input level in the UI part
    #I know this uses recursion and that's sometimes controversial but it works here, we're never going to have 1000 nested foor loops in a command list and for this purpose it just makes sense
    #I did not intend on making this eletist or unnessecarily complicated, if you can think of a nicer/simpler/easier to read way to do this with just for loops, let me know!
    out_list = []
    #fortag = False#pretty sure I don't need  this
    sublst = []
    forcount = 0
    for el in coms:
        if el == 'FOREACH':
            #fortag = True#pretty sure I don't need  this
            forcount += 1#using forcount to determine if this is a nested for loop - this is not extensively tested but I think it works
            if forcount > 1:
                sublst.append(el)
        elif el == 'ENDFOR':
            #fortag = False#pretty sure I don't need  this
            forcount -= 1#using forcount to determine if this is a nested for loop - this is not extensively tested but I think it works
            if forcount == 0:
                out_list.append(parser(sublst))#oooooh, recursion!!! (don't worry, it's not that scary, it just makes sense here)
            elif forcount > 0:
                sublst.append(el)
        elif forcount > 0:
            sublst.append(el)
        else:
            out_list.append(el)
    return out_list

def run_queue(queue,in_text):
    #again, we're using recursion (see note at start of parser function)
    #so, from the parsed command list we will have a list potentially containing 'sub lists'
    #each 'sub-list' is our implementation of a FOR-LOOP (from the standpoint of how the user chains 'commands'/'tasks' together)
    #therefore, each time we meet a list (in the commands list), we need to call the commands inside this list on each element of the current state of the text, the end result of which we can then send back to the main command queue
    #(working_text is the current state of what was input and is being processed by commands in the queue - it can actually be a list itself but it helps to just generally think of it as "the clipboard text, mid process")
    #again, recursion makes sense here to me, when processing the 'sub-lists', we need to make use of some sort of stack and a loop, recursion does this by definition and I find this easier than figuring out my own stack mechanism
    #maybe I'm just lazy and should learn more about stacks
    #FYI, I recommend this podcast episode on the subject of recursion - https://open.spotify.com/episode/5iycnoUlDP4TnsUUrqnPXa?si=27bbe6a6761c400a
    #I've not yet read his book on recursion (which is a book about recursion called 'the recusive book of recursion' (which is a book...)) but I likely will at some point.
    #From the podcast I gather it is not a book hailing recursion as a wonderful tool for geniouses but really a scathing review of when not to use it, but often explaining it in more approachable ways.
    #He talks a lot in the podcast about how recursion gets a bad wrap because of the many bad uses of it in tutorials etc. I feel I am though justified for this use of recursion. Rant over.
    working_text = in_text
    for task in queue:
        if isinstance(task, list):
            #this is a FOREACH section, recursively call again on this
            intermediary = []
            '''
            if isinstance(working_text,list):
                for each el in working_text:
                    intermediary_lst.append(run_queue(task,el))
            elif isinstance(working_text,str):
                for each el in working_text):
                    intermediary_lst += run_queue(task,el)'''
            for el in working_text:#where task is a sublist of tasks
                intermediary.append(run_queue(task,el))#this is either action on each char or list element, and either outputs a list or string
                #however, to make it possible to manage, the intermediary is always a list, so if user is not careful, they could get lists of lists
                #some thought is needed in how to guide the user to avoid this so they don't make broken task queues
            working_text = intermediary
        elif task == 'STRIPWHITESPACE':
            working_text = strip_whitespace(working_text)
        elif 'STRINGTOLIST' in task:
            splitter = task.split(':')[1]#we need to add error correction somewhere for if user doesn't supply splitter
            working_text = string_to_list(working_text,splitter)#there will be a separate function though for lines to list, so there will be no default splitter here
            #this will be put in the documentation so user knows they must supply splitter notation (or in GUI it will be required field just
        elif 'LISTTOSTRING' in task:#default joiner is '', :parameter is optional
            if len(task.split(':')) > 1:
                working_text = lst_to_string(working_text,joiner=task.split(':')[1])
            else:
                working_text = lst_to_string(working_text)
        elif 'LINESMANYTOONE' in task:
            if len(task.split(':')) > 1:
                working_text = lines_many_to_one(working_text,separator=task.split(':')[1])
            else:
                working_text = lines_many_to_one(working_text)#default separator is comma to provide csv like output
        elif task == 'EXTRACTINTS':
            working_text = extract_ints(working_text)#returns string of ints separated by commas
        elif task == 'REMOVEEMPTY':
            working_text = remove_empty(working_text)
        elif task == 'UNESCAPESPECIALS':
            working_text = unescape_specials(working_text)
    return working_text




#command sequences will be saved in a json file and loaded at runtime
#we will have an import function to import commands from a json file x into the system settings file (basically the json file in 'install' location) to allow for user sharing of command lists.
available_commands = {''}

def command_lists_from_file(filepath):
    pass

def export_command_lists_to_file(list_of_command_lists):
    pass

def load_settings(filepath='./app_settings.json'):
    pass








#BASIC TESTING
#here we shall perform some testing of the functions and the command queue mechanism, outside of GUI operation.

"""
commands = ['LINESMANYTOONE','STRINGTOLIST:,','REMOVEEMPTY','LISTTOSTRING: | ']
parsed_commands = parser(commands)

print(run_queue(parsed_commands,text))

print(" ----------- ")
input("Copy text now")
print(run_queue(parser(['STRIPWHITESPACE']),pyperclip.paste()))
"""