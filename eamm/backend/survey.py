import eamm.backend.database
import logging

# setup basic logging config
logging.basicConfig(filename='/var/log/eamm.log',level=logging.INFO)

def get_questions(id_template):

    # 1. get all initial generic questions.
    # 2. get template specific question.
    # 3. get all ending generic questions.
    # 4. return a dict, tupe of tuples with results ordered by idSurveyQuestion
    sql = """
    SELECT idSurveyQuestion, survey_question_text, idMeetingTemplate, ask_to_all 
    FROM EAMM.SurveyQuestion
    WHERE ask_to_all=1 or idMeetingTemplate=%s
    ORDER BY idSurveyQuestion
    """ 
    sql_vars=[id_template]
    
    db_conn = eamm.backend.database.MyDatabase()
    my_query_results = db_conn.select2(sql, sql_vars)
    if not my_query_results:
        logging.info(db_conn.error)
        return False
    elif len(my_query_results) == 0:
        logging.info("bad sql, not exist")
        return False
    else:
        # looks like were good.
        return my_query_results

class SurveyResponse(object):
    """
    1. Survey.__init__(form) is called to start up a new SurveyResponse object with
       the contents of the form being submittied.
       
       1.1 Survey.__load_form() pulls all the data from the form and into the self. 
           variables.
           
           1.1.1 Survey.__validate() checks to make sure everything is of the right 
                 format
                 
    2.0 Survey.add() is called to insert the data into the Survey Table.
    
        2.1 Survey.__already_exists() is run and checks to see if a form has already
            been filled out by someone with this email address.
            
        2.2 Survey.__add_to_survey_tbl() inserts the data into mysql.
    """
    def __init__(self, arg1=None):
        self.is_valid = True
        self.error = None
        if arg1 == None:
            # no arguments passed
            pass
        elif isinstance(arg1, (int, long)):
            # id_survey_response is an int, likely an existing id_survey_response
            # 1. craft the SQL, be explict
            # 2. execute the query
            # 3. check the rows returned, should be more than 1.
            
            sql = """
            """
            sql_vars = [arg1]
            my_db_conn = eamm.backend.database.MyDatabase()
            my_query_results = my_db_conn.select2(sql, sql_vars)
            
            if not my_query_results:
                self.is_valid = False
                self.error = my_db_conn.error
                logging.info("db connection failed")
            elif len(my_query_results) == 0:
                self.is_valid = False
                self.error = "id_survey_response %s does not exist"
                logging.info(self.error)
            else:
                # looks like were good.
                # better populate the data structure.
                pass
            
        elif arg1.getvalue('id_invite'):
            # arg1 is a form object instance, we know this because id_invite is 
            # one of the hidden form vals always passed through.
            form = arg1
            # error back to the calling class if we can't load the form.
            try:
                self.__load_form(form)
            except:
                raise
            
            try:
                self.__validate()
            except:
                raise
           
            
    def __load_form(self, form):
        
        if not all((form.getvalue('id_invite'), form.getvalue('id_meeting'),
                    form.getvalue('email_addr'), form.getvalue('responder_email_addr'))):
            self.error = "Class:SurveyResponse, Method: __load_form, Error: Not all form \
            fields contain data"
            logging.info(self.error)
            raise Exception(self.error)
        else:
            self.id_invite = form.getvalue('id_invite')
            self.id_meeting = form.getvalue('id_meeting')
            self.invitee_email_addr = form.getvalue('email_addr')
            self.responder_email_addr = form.getvalue('responder_email_addr')
            
            self.q_and_a = dict()
            for i in form.keys():
                if (isinstance(i, (int,long)) and 
                    isinstance(form.getvalue(i), (int,long))):
                    # looks like we have a q&a pair.
                    self.q_and_a[i]=form.getvalue(i)
        
    def __validate(self):
        pass
    
    
    def add(self):
        return True
    
    
    def __already_exists(self):
        pass
    
    
    def __add_to_survey_tbl(self):
        pass
    
    
        