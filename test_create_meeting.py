#!/usr/bin/python

# using this to determine GET or POST.
import os
import logging
import cgi
import cgitb; cgitb.enable()

# setup basic logging config
logging.basicConfig(filename="/var/log/eamm.log",level=logging.INFO)

def main():
    # if GET, we are displaying the form for input
    # if POST, we are reading the form, validating it, saving it to the DB and displaying a message back to the user.
    
    if os.environ['REQUEST_METHOD'] == 'GET':
        pass    
    elif os.environ['REQUEST_METHOD'] == 'POST':
        my_forms = cgi.FieldStorage()
        my_keys = my_forms.keys()
        for item in my_keys:
            logging.info(item)
        print "Content-type:text/html\r\n\r\n"
        print "<html>"
        print "<head>"
        print "<title> test </title>"
        print "</head>"
        print "<body>"
        print "test"
        print "</body>"
        print "</html>\r\n\r\n"

if __name__ == '__main__':
    main()