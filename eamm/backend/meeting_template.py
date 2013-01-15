import eamm.backend.database
import logging

# Import modules for CGI handling , the cgitb modules gives descriptive debug errors to the browser.
import cgitb; cgitb.enable(display=1)

# setup basic logging config
logging.basicConfig(filename='/var/log/eamm.log',level=logging.INFO)

class MeetingTemplate(object):
    
    def __init__(self, arg1=None):
        sql = ""

    def get_all(self):
        
        sql = '''
        SELECT idMeetingTemplate, title, description, purpose, agenda FROM EAMM.Template 
            ORDER BY idMeetingTemplate;
        '''   
        
        my_db_connection = eamm.backend.database.MyDatabase()
        my_query_results = my_db_connection.select(sql)        # my_query_results is a dict (tuple of tuples).
    
        if my_query_results[0][0] == 0:
            # this means the select got back nothing.
            return False
        else:
            return my_query_results
        
    def get(self, id_template):
        
        sql = '''
        SELECT idMeetingTemplate, title, description, purpose, agenda FROM EAMM.Template
            WHERE idMeetingTemplate='%s'
        ''' % id_template
        
        my_db_connection = eamm.backend.database.MyDatabase()
        my_query_results = my_db_connection.select(sql)        # my_query_results is a dict (tuple of tuples).
    
        if my_query_results[0][0] == 0:
            # this means the select got back nothing.
            return False
        else:
            self.id_template = my_query_results[0][0]
            self.title = my_query_results[0][1]
            self.description = my_query_results[0][2]
            self.purpose = my_query_results[0][3]
            self.agenda = my_query_results[0][4]
        