from string_converters import *

#print(extract_nums('3qrg45g45h45'))




def parser(coms):
    #print(coms)
    out_list = []
    fortag = False
    sublst = []
    forcount = 0
    for el in coms:
        if el == 'FOREACH':
            fortag = True
            forcount += 1
            if forcount > 1:
                sublst.append(el)
        elif el == 'ENDFOR':
            #sublst.append(el)
            
            fortag = False
            forcount -= 1
            if forcount == 0:
                out_list.append(parser(sublst))
                #something
                #sublst = []
            elif forcount > 0:
                sublst.append(el)
        elif forcount > 0:
            sublst.append(el)
        else:
            out_list.append(el)
    return out_list

def run_queue(queue,in_text):
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
    return working_text

text = """11 individual sweets

7 masks

10 masks + cloth

6 candles

1 foot spa

35 individual items"""

commands = ['LINESMANYTOONE','STRINGTOLIST:,','REMOVEEMPTY','LISTTOSTRING: | ']
parsed_commands = parser(commands)

print(run_queue(parsed_commands,text))
    