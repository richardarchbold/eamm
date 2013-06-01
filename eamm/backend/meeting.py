import logging
import eamm.backend.database
import cgitb; cgitb.enable(display=1)   # the cgitb modules gives descriptive debug errors to the browser.

# setup basic logging config
logging.basicConfig(filename='/var/log/eamm.log',level=logging.INFO)

class Meeting(object):
    """Summary of class here.

    """
    def __init__(self, id_meeting=None):
        """ init
        """
        self.is_valid = True
        self.error = None
    
        if (isinstance(id_meeting, (int, long))):
            # we were passed a meeting invite to load
            #
            # 1. craft the SQL, be explict
            # 2. execute the query
            # 3. check the rows returned, should be one.
            #    if 1 row returned:
            #        populate the right vales are return.
            #    else:
            #        log the error, set the flags
            #        return False
            sql = """
            SELECT idMeeting, idInvite, meeting_status, start_time, end_time, meeting_chair,
                   meeting_minute_notes
            FROM EAMM.Meeting
            WHERE idMeeting=%s
            """
            sql_vars = [id_meeting]
            my_db_conn = eamm.backend.database.MyDatabase()
            my_query_results = my_db_conn.select2(sql, sql_vars)
            
            if not my_query_results:
                self.is_valid = False
                self.error = my_db_conn.error
                logging.info("No query results")
            elif len(my_query_results) == 0:
                self.is_valid = False
                self.error = "id_meeting %s does not exist"
                logging.info(self.error)
            else:
                self.id_meeting = id_meeting
                self.id_invite = my_query_results[0][1]
                self.meeting_status = my_query_results[0][2]
                self.start_datetime = my_query_results[0][3]
                self.end_datetime = my_query_results[0][4]
                self.meeting_chair = my_query_results[0][5]
                self.meeting_minutes_notes = my_query_results[0][6]
        else:
            logging.info("bad id_meeting passed to init %s:%s" \
                         % (type(id_meeting), id_meeting))
        
    
    def add(self, id_invite, start_datetime, end_datetime, meeting_chair):
        self.id_invite = id_invite
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime
        self.meeting_chair = meeting_chair
        
        # idMeeting idInvite meeting_status start_time end_time meeting_chair 
        # meeting_minute_notes
        sql = """
        INSERT INTO Meeting (idInvite, meeting_status, start_time, end_time, 
                             meeting_chair) VALUES 
        ('%s', 'SCHEDULED', '%s', '%s', '%s')
        """ % (self.id_invite, self.start_datetime, self.end_datetime, 
               self.meeting_chair)
        
        # Specify that this is an insert with an auto-incrementing PK.
        auto_increment = True       

        if self.db_connection:
            my_db_connection = self.db_connection
            logging.info("yo")
        else:
            # open up a connection to the DB
            my_db_connection = eamm.backend.database.MyDatabase()
            logging.info("noo")
        
        # execute the insert, if it worked, the returned value will be the 
        # auto-incremented pk value for the fresh insert.
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

class Search(object):
    def __init__(self):
        pass
    
    def search(self, **kwargs):
        pass
        
         
    
            
        