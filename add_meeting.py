#!/usr/bin/env python

"""A one line summary of the module or script, terminated by a period.

Leave one blank line. The rest of this __doc__ string should contain an
overall description of the module or script.  Optionally, it may also
contain a brief description of exported classes and functions.

    ClassFoo: One line summary.
    functionBar(): One line summary.

Source:http://github/richardarchbold/eamm.git
Created: 7 Jan 2013
"""

__authors__ = [
  # alphabetical order by last name, please
  '"Richard  Archbold" <richardarchbold@gmail.com>',
]

# using this to determine GET or POST.
import os
import logging
import eamm.meeting_webpage
import cgi
import cgitb; cgitb.enable()

# setup basic logging config
logging.basicConfig(filename="/var/log/eamm.log",level=logging.INFO)

def main():
    this_webpage = eamm.meeting_webpage.AddMeetingWebPage();
    
    # if GET, we are displaying the form for input
    # if POST, we are reading the form, validating it, saving it to the DB and displaying a message back to the user.
    if os.environ['REQUEST_METHOD'] == 'GET':
        this_webpage.display_add_meeting_initial_form()     
    elif os.environ['REQUEST_METHOD'] == 'POST':
        this_webpage.process_add_meeting_initial_form()    

if __name__ == '__main__':
    main()