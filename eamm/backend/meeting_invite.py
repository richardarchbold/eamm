import logging
import eamm.backend.database
import eamm.backend.meeting

# Import modules for CGI handling , the cgitb modules gives descriptive debug errors to the browser.
import cgitb; cgitb.enable(display=1)

import re

# setup basic logging config
logging.basicConfig(filename='/var/log/eamm.log',level=logging.INFO)

class MeetingInvite(object):
    """
    * MeetingInvite(form), create a new MeetingInvite object, initialize values from a form
        * MeetingInvite.__init__(form)
            * MeetingInvite.__load_form(form), sets self.XXX values
                * MeetingInvite.__validate(), validates self.XXX values.
    
     if MeetingInvite.is_valid:     (is_valid is a bool set by __validate()
            if MeetingInvite.add():
                check if MeetingInvite.__already_exists, check if it already exists.
                MeetingInvite.__add_to_invite_tbl, use auto_increment to set self.id_invite.
                Meeting(), create a new meeting object
                Meeting.add(id_invite, start_datetime, end_datetime, meeting_chair)
    """
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
            # 1. add to invite tbl
            logging.info("start __add_to_invite_tbl")
            self.__add_to_invite_tbl()
            logging.info("finish __add_to_invite_tbl, is_valid=%s" % self.is_valid)
            # if the __add_to_invite_tbl failed, it will set the is_valid bool to false and stick the
            # error message is self.error
            if self.is_valid == False:
                return
                
            # 2. add to the invitees tbl
            logging.info("start __add_to_inviteeeeeee_tbl")
            self.__add_to_invitee_tbl()
            logging.info("finish __add_to_inviteeeeeeee_tbl, is_valid=%s" % self.is_valid)
            if self.is_valid == False:
                return
            
            # 3. add to meeting tbl, a la Meeting.add()
            # 
            # if it's a recurring meeting, we'll need to iterate through and add several
            # meeting instances.
            # if it's a non-recurring meeting, we only need to add a single meeting instance.
            #
            # we re-use the same db_connection for all of these, so we can do a single commit
            # at the end.
            if (self.recurring == "none"):
                my_meeting = eamm.backend.meeting.Meeting()
                if self.db_connection:
                    my_meeting.db_connection = self.db_connection
                    my_meeting.add(self.id_invite, self.start_datetime, self.end_datetime, self.requester)
                else:
                    self.is_valid = False
                    self.error = "meeting_invite.add() self.db_connection is dead and can't be passed \
                    to my_meeting.db_connection"
                    logging.info(self.error)
                    return
            else:
                # TODO: we'll deal with recurring meetings later
                pass
                  
            # if the my_meeting.add() method failed, it will set the is_valid bool to false and stick the
            # error message is self.error
            if my_meeting.is_valid == False:
                self.is_valid = False
                self.error = my_meeting.error
                    
                #roll back all the inserts
                try:
                    self.db_connection.db.rollback()
                except:
                    raise
                
                return
            else:
                # we made it, everything added!
                try:
                    self.db_connection.db.commit()
                except:
                    raise
                
                return True
            
    def __add_to_invitee_tbl(self):
        # row format:
        #    idInvite, invitee_email_addr
        # local attribute = self.invitees_list
        
        for this_addr in self.invitees_list:
            sql = """INSERT INTO Invitee (idInvite, invitee_email_addr) VALUES (%s, %s)"""
            sql_vars= [self.id_invite, this_addr]
            
            my_db_connection = self.db_connection
            my_db_connection.insert2(sql, sql_vars)
            
            if self.is_valid == False:
                self.error = "Class:MeetingInvite, Method: __add_to_invitee_tbl, error"
                logging.info(self.error)
                return
        
        return True
                
    def __add_to_invite_tbl(self):
        # row format:
        #   idInvite, start_date, duration, end_date, recurring, invite_status, title, purpose, 
        #   background_reading, agenda, requester_email_addr, venue, idMeetingTemplate  

        # set up the insert sql stmt
        #sql = '''
        #INSERT into Invite (start_date, duration, end_date, recurring, invite_status, title, 
        #                    purpose, background_reading, agenda, requester_email_addr, venue, 
        #                    idMeetingTemplate) 
        #VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")
        #''' % (self.start_datetime, self.duration, self.end_datetime, self.recurring, "ACTIVE", 
        #             self.title, self.purpose, "NONE", self.agenda, self.requester, self.venue, 
        #             self.id_template)
        
        sql = """
        INSERT into Invite (start_date, duration, end_date, recurring, invite_status, title, 
                            purpose, background_reading, agenda, requester_email_addr, venue, 
                            idMeetingTemplate) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """ 
        sql_vars= [self.start_datetime, self.duration, self.end_datetime, self.recurring, "ACTIVE", 
                   self.title, self.purpose, "NONE", self.agenda, self.requester, self.venue,
                   self.id_template]
        
        # Specify that this is an insert with an auto-incrementing PK.
        auto_increment = True       

        # check to see if db_connection is set
        if self.db_connection:
            my_db_connection = self.db_connection
        else:
            # open up a connection to the DB, check to make sure it worked
            my_db_connection = eamm.backend.database.MyDatabase()
            if not my_db_connection:
                self.is_valid = False
                self.error = "Class:MeetingInvite, Method: __add_to_invite_tbl, ERROR: Couldn't create \
                              MyDatabase object"
                return False
                
        # execute the insert2, if it worked, the returned value will be the auto-incremented 
        # PK value for the fresh insert
        my_last_insert_id = my_db_connection.insert2(sql, sql_vars, auto_increment)
        if not my_last_insert_id:      
            self.is_valid = False
            self.error = "Class:MeetingInvite, Method: __add_to_invite_tbl, Error: Couldn't \
            insert row, Message: %s" % my_db_connection.error
            return False
        else:
            logging.info("Class:MeetingInvite, Method: __add_to_invite_tbl, my_last_insert_id: \
            type(%s), value %s" % (type(my_last_insert_id), my_last_insert_id))
            # check that the return code is indeed good, and use it to set self.id_invite
            if my_last_insert_id > 0:  
                self.id_invite = my_last_insert_id
                logging.info("Class:MeetingInvite, Method: __add_to_invite_tbl, self.id_invite has \
                been set to %s", self.id_invite)
                return True
            else:
                self.is_valid = False
                self.error = "Class:MeetingInvite, Method: __add_to_invite_tbl, error: self.id_invite \
                could not be set, last_insert_id is %s" % my_last_insert_id
                logging.info(self.error)
                return False

    
    def __already_exists(self):    
        sql = """
        SELECT count(*) from Invite 
        WHERE (start_date=%s AND duration=%s AND invite_status='ACTIVE' AND title=%s AND
               purpose=%s AND agenda=%s AND requester_email_addr=%s)
        """
        
        sql_vars = [self.start_datetime, self.duration, self.title, self.purpose, self.agenda, 
                    self.requester]
        
        # open a DB connection and check it.
        my_db_connection = eamm.backend.database.MyDatabase()
        if not my_db_connection:
            self.is_valid = False
            self.error = "Class:MeetingInvite, Method: __add_to_invite_tbl, ERROR: Couldn't create \
                          MyDatabase object"
            return False
        
        # execute the select and check to make sure it worked.
        my_query_results = my_db_connection.select2(sql, sql_vars)
        if not my_query_results:
            self.is_valid = False
            self.error = "Class:MeetingInvite, Method: __already_exists, Error: Couldn't \
                          select row, Message: %s" % my_db_connection.error
            return False
        else:
            if my_query_results[0][0] == 0:
                # this means the select got back nothing.
                logging.info("Invite for %s does NOT already exist in DB" % self.title)
                return 0
            else:
                logging.info("Invite for %s DOES already exist in DB" % self.title)
                self.error = "Invite for meeting with Title \"%s\" DOES already exist in DB" % self.title
                self.is_valid = False
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
            self.error = "Class:MeetingInvite, Method: __load_form, Error:Not all form fields \
            contain data"
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
        
        # TODO, remove once testing complete.
        logging.info("Show me the invitee list from form: %s" % self.invitees)
        
        if not self.__validate():
            self.is_valid = False
            self.error = "Class:MeetingInvite, Method: __load_form, ERROR: Couldn't validate \
            form" 
            logging.info(self.error)
            return False
        else:
            return True
    
    
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
            logging.info("Class:MeetingInvite, Method: __validate, ERROR: %s" % self.error)
        #else:
            #logging.info("good start_date: %s" % self.start_date)
        
        result2 = re.search(regex_date, self.end_date)
        if result2 == None:
            self.is_valid = False
            self.error = "bad end_date: %r" % self.end_date
            logging.info("Class:MeetingInvite, Method: __validate, ERROR: %s" % self.error)
        #else:
        #    logging.info("good end_date: %s" % self.end_date)

        result3 = re.search(regex_time, self.start_time)
        if result3 == None:
            self.is_valid = False
            self.error = "bad start_time: %r" % self.start_time
            logging.info("Class:MeetingInvite, Method: __validate, ERROR: %s" % self.error)
        #else:
        #    logging.info("good start_time: %s" % self.start_time)

        result4 = re.search(regex_duration, self.duration)
        if result4 == None:
            self.is_valid = False
            self.error = "bad duration: %r" % self.duration
            logging.info("Class:MeetingInvite, Method: __validate, ERROR: %s" % self.error)
        #else:
        #    logging.info("good duration: %s" % self.duration)
        
        ####
        # validate invitees list, save the good email_addrs in a new list
        invitee_list = list()
        lines = self.invitees.split('\n')
        i=0
    
        for line in lines:
            # get rid of bracketing white spaces and print the line
            line = line.strip()
            logging.info("Class:MeetingInvite, Method: __validate, invitees line: %s" % line)
            
            # get rid of HTML tags with a non-greedy search and replace.
            line = re.sub("<.*?>", "", line)
            logging.info("Class:MeetingInvite, Method: __validate, invitees line stripped %s" % line)
        
            if re.match('^[\w\-\.]+@[\w\.\-]+\.\w+$', line):
                # the above is a crude regex for an email address.
                logging.info("Class:MeetingInvite, Method: __validate, invitees, line is an email address: %s\n\n" % line)
                invitee_list.append(line)
            elif re.match('\W+$', line):
                # it's a pure white space line, so skip it.
                logging.info("Class:MeetingInvite, Method: __validate, invitees, line is non-word chars, skipping")
                pass
            else:
                # bugs crud
                logging.info("Class:MeetingInvite, Method: __validate, invitees, line is NOT an email address: %s\n\n" % line)
                self.error = "Class:MeetingInvite, Method: __validate, invitees, line is NOT an email address: %s\n\n" % line
                self.is_valid = False
            i+=1
        
        # if there are no email's then it's false.
        if len(invitee_list) <= 0:
            self.is_valid = False
            self.error = "Class:MeetingInvite, Method: __validate, no valid email addrs for invitees"
            logging.info(self.error)
            
        # initialize a new object attribute for the santized invitee email_addr list        
        self.invitees_list = invitee_list
        logging.info("emails: %s", tuple(self.invitees_list))
        
        return self.is_valid

        
def __cleanup_crud(self):
    # delete any leftover crud from DB, pitty we're not using transactions here :-(
    sql = """
    DELETE FROM Invite WHERE idInvite='%s' LIMIT 1
    """
    
    # open up a connection to the DB
    my_db_connection = eamm.backend.database.MyDatabase()
        
    # execute the cleanup delete stmt.
    logging.info("Cleaning up and deleting Meeting Invite \"%s\" from the Invite tbl" % self.id_invite)
    my_db_connection.delete(sql)