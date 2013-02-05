#!/usr/bin/python

import sys
sys.path.append("/home/richard/workspace/eamm/")

# using this to determine GET or POST.
import os
import logging
import eamm.frontend.meeting_webpage
import cgi
import cgitb; cgitb.enable(display=1)

# setup basic logging config
logging.basicConfig(filename="/var/log/eamm.log",level=logging.INFO)

def main():
    logging.info("======")
    this_webpage = eamm.frontend.meeting_webpage.MeetingWebPage()
    user = os.environ['REMOTE_USER']
    
    if os.environ['REQUEST_METHOD'] == 'GET':
        this_webpage.display(user)
    
    elif os.environ['REQUEST_METHOD'] == 'POST':
        form = cgi.FieldStorage()
        logging.info("form type: %s" % type(form))
        this_webpage.display_search_results(user, form)
        
    this_webpage.render()
    
if __name__ == '__main__':
    main()