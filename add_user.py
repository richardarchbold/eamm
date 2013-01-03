#!/usr/bin/env python



# using this to determine GET or POST.
import os

# does the heavy lifting
from eamm.add_user_webpage import *

def main():

    this_webpage = AddUserWebPage();
    
    # if GET, we are displaying the form for input
    # if POST, we are reading the form, validating it, saving it to the DB and displaying a message back to the user.
    if os.environ['REQUEST_METHOD'] == 'GET':
        this_webpage.display_add_user_form()
                
    elif os.environ['REQUEST_METHOD'] == 'POST':
        this_webpage.process_add_user_form()    
        
if __name__ == "__main__":
    main()

