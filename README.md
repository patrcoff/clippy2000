# clippy2000
A clipboard content processor system tray tool written in Python

Purpose: Often I find myself needing to perform some manual admin task involving a lot of copy/pasting of text from various sources into various different applications.
         Sometimes however, the formatting of the copied text needs to be processed in some way for the intended purpose. For instance, I may need to copy multiple lines of text but paste them into a single line.
         An example might be a list of email addresses provided in a given format, which need to be pasted into one line, separated by commas. There are endless other examples of such inefficient tasks we all do each day, often performed manually using basic tools like a text editor as an intermediary between applications. This is of course fine for one off tasks, but once you start to need to repeat such manual tasks over and over, the pain of doing even small repetitions grows more and more unbearable.
         Often I think, I should really automate more of these repetitive tasks, but either the cost/benefit is too high, or I end up with multiple fragmented small scripts performing similar functions.
         On top of this, I often need to remind myself how exactly to perform a specific text manipulation task, making the effort to script a solution too high to bother.
         Initially, I had the idea to hardcode several specific workflows I need for my own personal and professional life, into one system tray tool, coded in Python. I made a quick demo in a couple of hours and very quickly realised that the scope could be significantly improved if I implemented a mechanism allowing for custom workflows to be created by the user without the needing for hardcoding. I also saw how often I was repeating the same code, or basically reordering the use of functions in my initial prototype.
         This project is intended to provide a simple, general purpose tool which can be user configured to perform text manipulation on the contents of the clipboard. It will not require the user to have knowledge of programming,
         though some familiarity with the ideas of programming may help. Ultimately, the end user will be able to chain a sequence of 'building-block' text processing functions together, with the option of some more advanced sequencing such as 'for loops'.
         The interface will mainly be interacted with via the system tray, with a simple window for editing sequences of text processing. There will be a number of built in sequences for common or useful general text processing tools.
         User created sequences can then be saved for bespoke purposes the user may have. It will enable the user to quickly build, test and save these sequences which can then save them time in repetitive manual copy/paste type admin tasks, without the need to learn more complicated code or put the upfront effort into writing an individual custom script for each task. It also provides a central resource for such repetitive tasks.
         Additionally, beyond the scope of simply reformatting copied text, more advanced functionality can be achieved with the use of 'extractor' and 'conversion' functions, which will allow the program to be used for some forms of text analysis, calculations etc. A simple example might be to take the average of a list of numbers embedded within a text, with just one click; or count the number words/characters in copied text. I may at some point include a mechanism to provide simple if-then logic to the end user but it has not currently been included at this stage of the project. This expands the scope beyond the initial intended use case of being a tool used in the middle of a copy/paste workflow (bypassing the need for manual text editing in say, notepad++), but provides further utilities which can be used in other such workflows where previously, you may have needed to perform a manual calculation, open a temporary spreadsheet or write an individual script. Instead, this can be seen as a more general purpose text based tool, where there user interacts with the tool via copy/paste, instead of a CLI or more complicated GUI (than the system tray list of available task sequences). The intention is to provide a reasonably high level of flexibility whilst maintaining a fairly simple to use interface with a small learning curve for creating custom task sequences. My current goal is for the tool to provide the functionality to allow for the processing of the following real world example.

         Example: In my day job I use a Salesforce instance of a case management system, where I spend a lot of time looking at a list of open/closed cases, with fields showing several pieces of information about each case.
         The salesforce instance, being a web app, does not handle being copy/pasted, where the result of pasting is that each 'cell' of data is pasted onto a separate line, starting with the first row of 'cells'. You thereofore end up with a 1-dimensional list of cells with no reference to where one row starts and another ends - this is virtually impossible to work with in another program such as excel and is not feasible to manually process. Thankfully, there is a 'printable view' which pastes somewhat acceptably into excel, however, to view in this mode opens a new tab (within the salesforce instance, as opposed to in the browser), adding to the overheads, and requires switching back to normal viewing mode to perform any regular casework. This is not an impossible problem, but it is very frustratingly clunky, and as I have no control over the salesforce instance, I cannot remove the source of the problem. Instead, my goal is to be able to use this project to be able to parse this text into properly formatted csv lines, without hardcoding a bespoke routine for just this one scenario (i.e. built from core functions/commands provided to the user).

         As I do not have to perform analysis of my historical cases, it needs to be simple enough to write the sequence of tasks to be considered a valuable use case. This is the initial benchmark of this project.

Intended usage:
  -Users will have a system tray GUI tool (written in Tkinter) which will allow them process the contents of the clipboard in various, editable ways.
  -The app will consist of a system tray menu with text processing functions (a few built-in and then user editable), a window pop-up for editing processing functions, henceforth referred to as 'task queues'.
  -The user will edit the task queues via GUI, using drop down lists with brief explanations of the functions as hover-overs.
  -The custom task queues will simply be saved in a json file, which will consist of a dict of keys (task queue name) value (list of function identifiers in string format) pairs

Code:
  -The functions will simply be stored in a simple module file, no object orientation is necessary at this point.
  -The main 'app.py' file will handle both the GUI and the processing of the clipboard contents, which will be performed as follows:
    -the selected task queue (list of strings) is parsed by the parser into a parsed list of strings/sub-lists (used for user 'for loops' in task queue)
    -the parsed task queue is then fed into a recursive function (again, for allowing for loop functionality to end user) and functions are applied to the input text in the sequence they appear in the task queues, mapped by if statements
    -there will be some error checking at some point, probably at the point of saving a new queue, using a modified parser to test the input/output types of each step in the queue/subqueues (for loops)
    -the allowed types are string and list, some functions will take either and output one type, some will only accept a specific type - the user will need to read the function descriptions carefully to know which functions can chain together and in what order

Although the user will not have to type the names of the commands to chain together (this will all be done via drop down lists in GUI), they will still see to them referred to by the internal nomenclature -  capitalised strings with no spaces, sometimes with options parameters appended after a colon i.e. TASKDESCRIPTION:parameter

An example of this which uses the full extended nomenclature including parameters, would be 'STRINGTOLIST:,' where 'STRINGTOLIST' maps to a function which takes text input, and separates it based on the substring immediately following the colon symbol - in this example using the comma symbol, and outputs it to a list of strings. This is analogous to the Python code 'output = str.split(',')' which is in fact how this is handled internally. (there is currently very little error checking at this stage and it is immediately apparent to me as I write this that I will need to edit the parser to handle the case where a colon is the separator itself.) Again, the user doesn't have to write these commands, but they will at least see the first part of them (before the colon) as they will be used for the 'function' names in the user context. They will have access to a library of these commands which will explain their usage, including the input and output types. All commands will either take a string or list type as input, and likewise output one or the other of these two types. Therefore, not all possible combinations of commands will be valid, the input and output of chained commands must match to be compatible. *Actually, excel seems to manage to perform some of this desired functionality itself, where it manages to put the content into the correct rows, though it gets the columns out of sync by inconsistently including html elements in the data -  there is clearly metadata not being kept in the clipboard text when pasted into python, a generic text editor, or even using repr() function in python to show special characters. More research is needed here but the way I imagined performing this was by translating lists based on a known column or row length, after initially cleaning the text (there are unwanted elements in this example which do come through to the text-only clipboard content, for example 'Select item 5' - this is text attributed to a checkbox in the webpage (which we do not want as copy does not get the first instance of this, therefore putting the columns out of sync so we want to first remove instances of this text) - the text is not shown on the webpage but in excel it is displayed beside an actual check-box, it is likely an html or javascript component, perhaps a variable name. This is a good outline of how the user will need to initially inspect the contents of the returned clipboard text in order to know all required processing steps.

Planned functions:

  UNESCAPESPECIALS
  Takes a string a un-escapes it's special characters in order to show the user what special characters are in the text - used for prototyping new workflows.

  STRINGTOLIST
  Takes text input and splits it into a list based on the required parameter passed in.

  LISTTOSTRING
  Takes a list of strings and joins them together based on the optional joiner parameter: a substring (default: comma). E.g ['This','text','joins','together'] --> 'LISTTOSTRING: & ' --> This & text & joins & together

  LISTTOMULTILIST
  Takes a list of strings, and converts them to a different list of lists, where every parameter x elements of the input list, become a 'row' or a 'column' in the output list. You can consider x to be the number of columns/rows depending on the orientation of the input list. This can be then fed into LISTTOTABLE where parameter orientation is 'row' or 'col'

  LISTTOTABLE
  Takes a list of lists and outputs them as *csv data based on parameter 'orientation', which can take values of 'row' or 'col' indicating whether each sub-list represents a row or a column of data
  * I need to figure out how we will handle 'csv' data, for different output purposes - what do we do about commas within the text, what about quotations etc - needs some testing. *

  REMOVEEMPTY
  Takes a list and removes any empty elements, returns list

  REMOVEELEMENTEQUALS
  Takes a list and removes any elements which equal the string parameter

  REMOVEELEMENTCONTAINS
  Takes a list and removes any elements which contain the string parameter

  REMOVEELEMENTSTARTSWITH
  Takes a list and removes any elements which starts with the string parameter

  REMOVEELEMENTENDSWITH
  Takes a list and removes any elements which ends with the string parameter

  EXTRACTINTS
  Extracts all of the integers within the input text and passes them out in a list.

  EXTRACTFLOATS
  Extracts all of the floating point numbers within the input text and passes them out in a list.

  EXTRACTDATES
  Extracts numerous date formats and outputs them to a list. Takes optional parameter of regional date formatting Global vs US, defaults to assuming DD/MM/YY order is used in input. Output dates will be YYYY-MM-DD

  EXTRACTEMAILS
  Extracts email addresses from text and outputs them to a list.

  STRIPWHITESPACE
  Removes whitespace from text, outputs as string type.   

  LINESMANYTOONE
  Removes linebreaks from input text and outputs to one line, separating input lines by optional separator parameter.

  LINESOENTOMANY
  Separates text input to multiple lines based on separator parameter, outputs multiline string.

  FOREACH
  The start of a for-loop, where all commands between this and the ENDFOR command are performed on each element within the input variable. This will perform actions most commonly on the elements of a list, or chars of a string.

  ENDFOR
