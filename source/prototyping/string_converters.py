#this module will be responsible for providing the functions used in the editable clipboard converter system tray tool

#each function will take either a string or a list and perform some action on it

#these will be the building blocks which the GUI app will chain together using a simplified language similar to jinja

#actions to include

#remove whitespace - all
#remove linespaces
#separate to lines on x
#separate to lines by length per line
#remove custom x from all
#extract numbers
#extract emails
#converters
#  dec to bin
#  hex to dec
#

import re

#--------------------------------------------------------------------
#STRING FUNCTIONS
def strip_whitespace(x):
    return "".join(x.split())

def extract_ints(x):#need a float version of this...
    return ",".join([i for i in re.split(r'\D+',x) if i != ''])

def string_to_list(x,splitter):
    return x.split(splitter)

def lines_many_to_one(x,separator=','):
    remove_r = "".join(x.split('\r'))
    remove_n =  separator.join(remove_r.split('\n'))
    return remove_n

#--------------------------------------------------------------------
#LIST FUNCTIONS

def act_on_list(lst,func):#this functionality has been moved out of the module functions and into the app logic,
    #where inputs include FOREACH and ENDFOR, which will work on either list or string items
    output = []
    for el in lst:
        output.append(func(el))

def lst_to_string(lst,joiner=''):
    return joiner.join(lst)

def remove_empty(x):
    return [x for x in x if x != '' and x]