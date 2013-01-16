import logging
import eamm.backend.database
import eamm.backend.meeting

# Import modules for CGI handling , the cgitb modules gives descriptive debug errors to the browser.
import cgitb; cgitb.enable(display=1)

import re

# setup basic logging config
logging.basicConfig(filename='/var/log/eamm.log',level=logging.INFO)

class MeetingInvite(object):
    
    def __init__(self, arg1=None):    
        # by default, a new object is True, self.__validate() will update the status.
        self.is_valid = True
        self.error = False
        
        if arg1 == None:
            # no arguments passed
            pass
        elif type(arg1) is int:
            # arg1 is an int, likely an existing id_meeting_invite
            pass
        elif arg1.getvalue('purpose'):
            # arg1 is a form object instance.
            #logging.info("MeetingTemplate() was passed a form as an object")
            form = arg1
            
            # error back to the calling class if we can't load the form.
            self.__load_form(form)
       
       
    def add(self):
        """add needs to do a few things:
        
        1. add a single row to the invite table.
        2. add a row for every meeting instance of the invite to the meeting table.
           --> time to create meeting.add()?
        3. add all relevant rows for each invitee email for each meeting instance to the 
           participants table. 
           --> time to create participant.add()?
           1. add a single row to the invite table.
        """
        
        # MySQL retrieves and displays DATETIME values in 'YYYY-MM-DD HH:MM:SS' format. 
        self.start_datetime = self.start_date + " " + self.start_time + ":00"
        self.end_datetime = self.end_date + " " + self.start_time + ":00"
        
        if not self.__already_exists():
            self.__add_to_invite_tbl()
            # add to meeting table
            # add to participant table
            
            if (self.recurring == "none"):
                my_meeting = eamm.backend.meeting.Meeting()
                # meeting.add(id_invite, start_datetime, end_datetime, meeting_chair)
                my_meeting.add(self.id_invite, self.start_datetime, self.end_datetime, self.requester)
                
                # if it worked, my_meeting.id_meeting will be an int, if it failed, it will be False
                if type(my_meeting.id_meeting) is int:
                    return True
                else:
                    return False
            # TODO: this is where we flesh out the recurring shit.
            
    def __add_to_invite_tbl(self):
        # row format:
        #   idInvite, start_date, duration, end_date, recurring, invite_status, title, purpose, 
        #   background_reading, agenda, requester_email_addr, venue, idMeetingTemplate  

        # set up the insert sql stmt
        sql = """
        INSERT into Invite (start_date, duration, end_date, recurring, invite_status, title, 
                            purpose, background_reading, agenda, requester_email_addr, venue, 
                            idMeetingTemplate) 
        VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')
        """ % (self.start_datetime, self.duration, self.end_datetime, self.recurring, "ACTIVE", \
                     self.title, self.purpose, "NONE", self.agenda, self.requester, self.venue, \
                     self.id_template)
        # Specify that this is an insert with an auto-incrementing PK.
        auto_increment = True       

        # open up a connection to the DB
        my_db_connection = eamm.backend.database.MyDatabase()
        
        # execute the insert, if it worked, the returned value will be the auto-incremented pk value
        # for the fresh insert.
        my_last_insert_id = my_db_connection.insert(sql, auto_increment)

        
        # check that the return code is indeed good, and use it to set self.id_invite
        if type(my_last_insert_id) is int:  
            self.id_invite = my_last_insert_id
            return True
        else:
            return False

    
    def __already_exists(self):
        sql = """
        SELECT count(*) from Invite 
        WHERE (start_date='%s' AND duration='%s' AND invite_status='ACTIVE' AND title='%s' AND
               purpose='%s' AND agenda='%s' AND requester_email_addr='%s')
        """ % (self.start_datetime, self.duration, self.title, self.purpose, self.agenda, self.requester)
        
        logging.info("__already_exists sql: %s" % sql)
        
        my_db_connection = eamm.backend.database.MyDatabase()
        my_query_results = my_db_connection.select(sql)
        if my_query_results[0][0] == 0:
            # this means the select got back nothing.
            return False
        else:
            return True

    
    def __load_form(self, form):
    # initialize all key class attributes from form data.            
        # check to make sure all fields have stuff in them.
        if not all((form.getvalue('purpose'), form.getvalue('justification'), 
                    form.getvalue('template'), form.getvalue('agenda'), 
                    form.getvalue('title'), form.getvalue('start_date'),
                    form.getvalue('start_time'), form.getvalue('recurring'),
                    form.getvalue('end_date'), form.getvalue('venue'),
                    form.getvalue('requester'), form.getvalue('invitees'))):
            self.is_valid = False
            self.error = "Not all form fields contain data"
            return False
        
        self.purpose = form.getvalue('purpose')              # wysiwyg html string
        self.justification = form.getvalue('justification')  # wysiwyg html string
        self.id_template = form.getvalue('template')         # integer
        self.agenda = form.getvalue('agenda')                # wysiwyg html string
        self.title = form.getvalue('title')                  # string
        self.start_date = form.getvalue('start_date')        # yyyy-mm-dd string
        self.start_time = form.getvalue('start_time')        # hh:mm 24 hr string 
        self.duration = form.getvalue('duration')            # mm string
        self.recurring = form.getvalue('recurring')          # string
        self.end_date = form.getvalue('end_date')            # yyyy-mm-dd string
        self.venue = form.getvalue('venue')                  # string
        self.requester = form.getvalue('requester')          # you@example.com string
        self.invitees = form.getvalue('invitees')            # wysiwyg html string    
        
        self.__validate()
        return
    
    
    def __validate(self):
    # just check to make sure dates and times are in the correct format to be parsed for
    # mysql datetimes, etc.
    # The DATETIME type is used for values that contain both date and time parts. 
    # MySQL retrieves and displays DATETIME values in 'YYYY-MM-DD HH:MM:SS' format. 
    # The supported range is '1000-01-01 00:00:00' to '9999-12-31 23:59:59'.
    #
    #   self.start_date     # yyyy-mm-dd string
    #   self.start_time     # hh:mm 24 hr string
    #   self.end_date       # yyyy-mm-dd string
        regex_date = "^20\d\d-([01]\d)-([0-3]\d$)"
        regex_time = "^[0-2]\d:[0-6]\d$"
        regex_duration = "^\d\d$"
        
        result = re.search(regex_date, self.start_date)
        if result == None:
            self.is_valid = False
            self.error = "bad start date: %r" % self.start_date
        else:
            logging.info("good start_date: %s" % self.start_date)
        
        result2 = re.search(regex_date, self.end_date)
        if result2 == None:
            self.is_valid = False
            self.error = "bad end_date: %r" % self.end_date
        else:
            logging.info("good end_date: %s" % self.end_date)

        result3 = re.search(regex_time, self.start_time)
        if result3 == None:
            self.is_valid = False
            self.error = "bad start_time: %r" % self.start_time
        else:
            logging.info("good start_time: %s" % self.start_time)

        result4 = re.search(regex_duration, self.duration)
        if result4 == None:
            self.is_valid = False
            self.error = "bad duration: %r" % self.duration
        else:
            logging.info("good duration: %s" % self.duration)