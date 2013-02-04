#!/usr/bin/python

import sys
sys.path.append("/home/richard/workspace/eamm/")

# using this to determine GET or POST.
import os
import logging
import eamm.frontend.meeting_webpage
import cgitb; cgitb.enable(display=1)

# Import these for query string parsing.
from urlparse import parse_qs

# setup basic logging config
logging.basicConfig(filename="/var/log/eamm.log",level=logging.INFO)

def main():
    this_webpage = eamm.frontend.meeting_webpage.MeetingWebPage()
    
    if os.environ['REQUEST_METHOD'] == 'GET':
        if os.environ['QUERY_STRING']:
            qs = parse_qs(os.environ['QUERY_STRING'])
            id_meeting = int(qs['var1'][0])
            this_webpage.display_this_meeting(id_meeting)
        else:
            # we don't have a query string, which we should do on this page.
            # should be printing an error page here.
            this_webpage.error_table("Bad URL, no query string")
    elif os.environ['REQUEST_METHOD'] == 'POST':
        this_webpage.error_table("Bad URL, no POST method defined")
        
    this_webpage.render()
    
if __name__ == '__main__':
    main()