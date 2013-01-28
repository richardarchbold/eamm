#!/usr/bin/python

import sys
sys.path.append("/home/richard/workspace/eamm/")
import eamm.frontend.base_webpage

# using this to determine GET or POST.
import os
import logging

from urlparse import parse_qs

# setup basic logging config
logging.basicConfig(filename="/var/log/eamm.log",level=logging.INFO)

def main():
    this_webpage = eamm.frontend.base_webpage.WebPage()
    
    this_webpage.set_title("test")
    
    if os.environ['REQUEST_METHOD'] == 'GET':
        
        if os.environ['QUERY_STRING']:
            # REQUEST_URI
            # QUERY_STRING
            #this_qs = os.environ['QUERY_STRING']
            this_qs = "var1=12345&var2=rich%40amazon.com"
            qsl = parse_qs(this_qs)
            
            this_webpage.add_to_body("qsl %s" % qsl['var2'][0])
        else:
            this_webpage.add_to_body("error, no query string")
        
    elif os.environ['REQUEST_METHOD'] == 'POST':
        this_webpage.add_to_body("POST")
        
    this_webpage.render()

if __name__ == '__main__':
    main()