#!/usr/bin/python

import sys
sys.path.append("/home/richard/workspace/eamm/")

'''
Created on 3 Jan 2013
@author: richard
'''

# using this to determine GET or POST.
import os
import logging
import eamm.frontend.user_webpage

# setup basic logging config
logging.basicConfig(filename="/var/log/eamm.log",level=logging.INFO)

def main():

    this_webpage = eamm.frontend.user_webpage.AddUserWebPage();
    
    # if GET, we are displaying the form for input
    # if POST, we are reading the form, validating it, saving it to the DB and displaying a message back to the user.
    if os.environ['REQUEST_METHOD'] == 'GET':
        this_webpage.display_add_user_form()     
    elif os.environ['REQUEST_METHOD'] == 'POST':
        this_webpage.process_add_user_form()    
        
if __name__ == "__main__":
    main()
