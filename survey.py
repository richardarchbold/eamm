#!/usr/bin/python

# using this to determine GET or POST.
import os
import logging
import eamm.frontend.survey_webpage
import cgitb; cgitb.enable(display=1)

# setup basic logging config
logging.basicConfig(filename="/var/log/eamm.log",level=logging.INFO)

def main():
    this_webpage = eamm.frontend.survey_webpage.SurveyWebpage()
    
    if os.environ['REQUEST_METHOD'] == 'GET':
        if os.environ['QUERY_STRING']:
            query_string = os.environ['QUERY_STRING']
            this_webpage.show_survey(query_string)
        else:
            # we don't have a query string, which we should do on this page.
            # should be printing an error page here.
            this_webpage.error_table("Bad URL, no query string")
        
    elif os.environ['REQUEST_METHOD'] == 'POST':
        this_webpage.process_survey()
        
    this_webpage.render()

if __name__ == '__main__':
    main()
    