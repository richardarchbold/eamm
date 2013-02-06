#!/usr/bin/python

import sys
sys.path.append("/home/richard/workspace/eamm/")

# using this to determine GET or POST.
import os
import logging
import eamm.frontend.base_webpage
import cgi
import cgitb; cgitb.enable(display=1)

# setup basic logging config
logging.basicConfig(filename="/var/log/eamm.log",level=logging.INFO)

def main():

    this_webpage = eamm.frontend.base_webpage.WebPage()
    
    this_webpage.set_title("test POST form")
    
    if os.environ['REQUEST_METHOD'] == 'POST':
        form = cgi.FieldStorage()
        var1 = form.getvalue('var1')
        this_webpage.add_to_body("var1: %s" % var1)
        logging.info("var1: %s" % var1)
    else:
        logging.info("method was GET")
        
    this_webpage.render()
    
if __name__ == '__main__':
    main()