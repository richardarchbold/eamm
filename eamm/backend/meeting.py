import logging
import eamm.backend.database
import cgitb; cgitb.enable(display=1)   # the cgitb modules gives descriptive debug errors to the browser.

# setup basic logging config
logging.basicConfig(filename='/var/log/eamm.log',level=logging.INFO)

class Meeting(object):
    """Summary of class here.

    """
    def __init__(self):
        """ init
        """
        self.id_Meeting = False
        self.is_valid = True
        self.error = None
    
    def add(self, id_invite, start_datetime, end_datetime, meeting_chair):
        self.id_invite = id_invite
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime
        self.meeting_chair = meeting_chair
        
        # idMeeting idInvite meeting_status start_time end_time meeting_chair meeting_minute_notes
        sql = """
        INSERT INTO Meeting (idInvite, meeting_status, start_time, end_time, meeting_chair) VALUES 
        ('%s', 'SCHEDULED', '%s', '%s', '%s')
        """ % (self.id_invite, self.start_datetime, self.end_datetime, self.meeting_chair)
        
        # Specify that this is an insert with an auto-incrementing PK.
        auto_increment = True       

        # open up a connection to the DB
        my_db_connection = eamm.backend.database.MyDatabase()
        
        # execute the insert, if it worked, the returned value will be the auto-incremented pk value
        # for the fresh insert.
        logging.info("Adding Meeting with id_invite of \"%s\" to the Meeting tbl DB" % self.id_invite)
        my_last_insert_id = my_db_connection.insert(sql, auto_increment)

        # check that the return code is indeed good, and use it to set self.id_invite
        if my_last_insert_id > 0:  
            self.id_meeting = my_last_insert_id
            logging.info("self.id_meeting has been set to %s", self.id_meeting)
            return True
        else:
            self.is_valid = False
            self.error = "self.id_meeting could not be set"
            logging.info("self.id_meeting could not be set")
            return False

        
         
    
            
        