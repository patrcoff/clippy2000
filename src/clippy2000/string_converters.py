# this module will be responsible for providing the functions used in the editable clipboard converter system tray tool

# each function will take either a string or a list and perform some action on it

# these will be the building blocks which the GUI app will chain together using a simplified language similar to jinja

# actions to include

# remove whitespace - all
# remove linespaces
# separate to lines on x
# separate to lines by max length per line
# remove custom x from all
# extract numbers
# extract emails
# converters
#  dec to bin
#  hex to dec
#

import re

# --------------------------------------------------------------------
# STRING FUNCTIONS
def unescape_specials(x):
    return repr(x)[1:-1]  # the repr func adds quotes to the text which we don't need


def strip_whitespace(
    x,
):  # TO DECIDE IF THIS SHOULD INCLUDE LINEBREAKS OR NOT - currently it escapes all whitespace including \r and \n
    return "".join(x.split())


def extract_ints(x):  # need a float version of this...
    return ",".join([i for i in re.split(r"\D+", x) if i != ""])


def string_to_list(x, splitter):
    print(splitter)
    return x.split(splitter)


def lines_many_to_one(x, separator=","):
    remove_r = "".join(x.split("\r"))
    remove_n = separator.join(remove_r.split("\n"))
    return remove_n


def replace_string(x, y, z):
    return x.replace(y, z)


# --------------------------------------------------------------------
# LIST FUNCTIONS

# def act_on_list(lst,func):#this functionality has been moved out of the module functions and into the app logic, !!!!!!
#    #where inputs include FOREACH and ENDFOR, which will work on either list or string items
#    output = []
#    for el in lst:
#        output.append(func(el))


def lst_to_string(lst, joiner=""):
    return joiner.join(lst)


def remove_empty(x):
    return [x for x in x if x != "" and x]


def list_to_table(
    x, delim=","
):  # takes a list as input, i.e. a list of rows (separate lines) and separates lines on delim
    table = []
    for row in x:
        table.append(string_to_list(row, delim))
    return table


def reverse_table(x):  # reverse orientation of table, i.e. rows become columns
    table = []  # HERE WE'VE DONE NO ERROR CHECKNIG FOR TABLES OF INCONSISTENT SIZES
    intermediate = []
    for i in range(len(x[0])):  # column
        intermediate = [row[i] for row in x]
        table.append(intermediate)
    return table


def get_column(x, y):
    # expects a list of lists (representing a table)
    # where each sublist is a column from the table (use in conjunction with table transform function - reverse_table)
    # y is either the column number (1 indexed) or column header
    if y.isnumeric():
        # is column index
        return x[int(y) - 1]
    else:
        for col in x:
            if col[0] == y:
                # print(col)
                return col
        return x[0]  # will return first column if header not found

        # is column header


# --------------------------------------------------------------------
# COMBINED FUNCTIONS


def remove_y(x, y):
    if isinstance(x, str):
        return x.replace(y, "")
    elif isinstance(x, list):
        return [x for x in x if x != y]
