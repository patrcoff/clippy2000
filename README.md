# clippy2000
A clipboard content processor system tray tool written in Python

Purpose: Often I find myself needing to perform some manual admin task involving a lot of copy pasting of text from various sources into various different applications.
         Sometimes however, the formatting of the copied text needs to be processed in some way for the intended purpose. For instance, I may need to copy multiple lines of text but paste them into a single line.
         A good example might be a list of email addresses provided in one format, which need to be pasted into one line, separated by commas. There are endless other examples of such inefficient tasks we all do each day.
         Often I think, I should really automate more of these repetitive tasks, but either the cost/benefit is too high, or I end up with multiple fragmented small scripts performing similar functions.
         On top of this, I often need to remind myself how exactly to perform a specific text manipulation task, making the effort to script a solution too high to bother.
         This project is intended to provide a simple general purpose tool which can be user configured to perform text manipulation on the contents of the clipboard. It will not require the user to have knowledge of programming,
         though some familiarity with the ideas of programming may help. Ultimately, the end user will be able to chain a sequence of building-block text processing functions together in a sequence, possibly containing basic for loops.
         The interface will mainly be interacted from the system tray, with a simple window for editing sequences of text processing. There will be a number of built in sequences for common or useful general text processing tools.
         User created sequences can then be saved for bespoke purposes the user may have. It will enable the user to quickly build, test and save these sequences which can then save them time in future manual admin tasks, without the need to learn more complicated code or put the upfront effort into writing an individual custom script.

Intended usage:
  -Users will have a system tray GUI tool (written in Tkinter) which will allow them process the contents of the clipboard in various, editable ways.
  -The app will consist of a system tray menu with text processing functions (a few built-in and then user editable), a window pop-up for editing processing functions, henceforth referred to as 'task queues'.
  -The user will edit the task queues via GUI, using drop down lists with brief explanations of the functions as hover-overs.
  -The custom task queues will simply be saved in a json file, which will consist of a dict of keys (task queue name) value (list of function identifiers in string format) pairs

Code:
  -The functions will simply be stored in a simple module file, no object orientation is necessary at this point.
  -The main 'app.py' file will handle both the GUI and the processing of the clipboard contents, which will be performed as follows:
    -the selected task queue (list of strings) is parsed by the parser into a parsed list of strings/sublists (used for user 'for loops' in task queue)
    -the parsed task queue is then fed into a recursive function (again, for allowing for loop functionality to end user) and functions are applied to the input text in the sequence they appear in the task queues, mapped by if statements
    -there will be some error checking at some point, probably at the point of saving a new queue, using a modified parser to test the input/output types of each step in the queue/subqueues (for loops)
    -the allowed types are string and list, some functions will take either and output one type, some will only accept a specific type - the user will need to read the function descriptions carefully to know which functions can chain together and in what order

Planned functions:

  STRINGTOLIST
  LISTTOSTRING
  EXTRACTINTS
  EXTRACTFLOATS
  EXTRACTDATES
  EXTRACTEMAILS
  STRIPWHITESPACE
  LINESMANYTOONE
  LINESONTOMANY
