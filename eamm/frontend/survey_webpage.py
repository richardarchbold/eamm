# import necessary eamm modules.
import eamm.frontend.base_webpage 
import eamm.backend.survey

# Import modules for CGI handling , the cgitb modules gives descriptive debug errors to the browser.
import cgitb; cgitb.enable(display=1)

# Import these for query string parsing.
from urlparse import parse_qs
import re

# setup basic logging config
import logging
logging.basicConfig(filename="/var/log/eamm.log",level=logging.INFO)

class SurveyWebpage(eamm.frontend.base_webpage.WebPage):
    def __init__(self):
        super(SurveyWebpage, self).__init__()
        self.js = """<script type="text/javascript" src="http://127.0.0.1/eamm/js/eamm.js"></script>"""
        self.is_valid = True
        self.error = False
        self.query_string = False
        self.error_base = "Class: SurveyWebPage, Method: %s, Error: %s"
        
        
    def show_survey(self, query_string):
        # Flow of this method ...
        # 
        # 1. parse & validate query_string, populating self.id_meeting and self.email_addr
        #    the query string should be something like:
        #    1234&me%40amazon%2Ecom    (%40 = @ , %2E = .)
        #    
        # 2. instantiate the relevant meeting and invite objects, well need them to print the 
        #    top part of the page.
        #
        # 3. create a new survey object.
        #    populate the questions with survey.get_questions(id_template)
        #
        #    (now we have all the info we need to display the page)
        # 
        # 4. print out the HTML.
            
        self.query_string = query_string
        
        # done and 
        if not self.parse_query_string():
            self.error_table(self.error)
        
        # need to write a method to load a meeting object if it's passed an id_meeting 
        # on instantiation 
        self.meeting_obj = eamm.backend.meeting.Meeting(self.id_meeting)
        if not self.meeting_obj.is_valid:
            self.error_table(self.meeting_obj.error)
            return
        
        # need to write a method to load a meeting invite object if it's passed an id_invite
        # on instantiation (partially stubbed out at the __init__ level
        self.invite_obj = eamm.backend.meeting_invite(self.meeting_obj.id_invite)
        if not self.invite_obj.is_valid:
            self.error_table(self.invite_obj.error)
            return
        
        # need to write the function to get_questions based on id_template.
        self.survey_questions = eamm.backend.survey.get_questions(self.id_template)
        if not self.survey_questions:
            self.error_table("could not get survey questions for %s" % self.id_template)
            return
        
        self.__show_survey()
        
        
    def __show_survey(self):
        # this just prints out the HTML
        pass
        
        
    def parse_query_string(self):
        # write some code to populate self.id_meeting and self.email_addr
        # write some code to check that one is an int and that the other is an email_add
        # IF something goes wrong:
        #    return False, set is_valid to False and set error to the error log the error.
        # ELSE:
        #    return True.
        qs = parse_qs(self.query_string)

        # if we have a string in var1, the int() function will barf an exception, so we
        # catch the barf, if it happens and return false instead.    
        try:
            self.id_meeting = int(qs['var1'][0])
        except Exception:
            self.error = "survey_webpage.SurveyWebpage.__parse_query_string(): %s is not an int" % qs['var1']
            logging.info(self.error)
            self.is_valid = False
            return False

        # re.match('^[\w\-\.]+@[\w\.\-]+\.\w+$', line):
        logging.info("qs var2 = \"%s\"" % qs['var2'][0])
        if re.match('^[\w\-\.]+@[\w\.\-]+\.\w+$',qs['var2'][0]):
            self.email_addr = qs['var2'][0]
        else:
            self.error = """Class: survey_webpage, Method: __parse_query_string, Error, var2 not an 
            email_addr: %s""" % qs['var2']
            logging.info(self.error)
            self.is_valid = False
            return False
    
        return True
    
    def process_survey(self):
        pass