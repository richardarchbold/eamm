#!/usr/bin/python

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
import eamm.frontend.meeting_invite_webpage.py
import cgi
import cgitb; cgitb.enable()

# setup basic logging config
logging.basicConfig(filename="/var/log/eamm.log",level=logging.INFO)

def main():
    this_webpage = eamm.frontend.meeting_invite_webpage.AddMeetingWebPage();
    
    if os.environ['REQUEST_METHOD'] == 'GET':
        this_webpage.add_meeting_invite_step_1_form()
             
    elif os.environ['REQUEST_METHOD'] == 'POST':
        form = cgi.FieldStorage()
        form_method = form.getvalue('method')
        
        if form_method == 'add_meeting_invite_step_1_form':
            this_webpage.add_meeting_invite_step_2_form()
        elif form_method == 'add_meeting_invite_step_2_form':
            this_webpage.add_meeting_invite_step_3_form()
        elif form_method == 'add_meeting_invite_step_3_form':
            this_webpage.add_meeting_invite_step_4_form()
        else
            logging.info('unknown post method: %s' % form_method)   

if __name__ == '__main__':
    main()