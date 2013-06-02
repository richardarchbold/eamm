"""This module is the meeting invite backend abstraction layer

This module contains the MeetingInvite Class, the backend class which models
meeting invite behavior and performs storage actions for meeting invites.

"""

import logging
import eamm.backend.database
import eamm.backend.meeting
import eamm.backend.email_invite
from datetime import datetime, timedelta
from dateutil.rrule import *

# Import modules for CGI handling , the cgitb modules gives descriptive debug 
# errors to the browser.
import cgitb; cgitb.enable(display=1)

import re
from random import randint

# setup basic logging config
logging.basicConfig(filename='/var/log/eamm.log',level=logging.INFO)

class MeetingInvite(object):
    """
    * MeetingInvite(form), create a new MeetingInvite object, initialize 
      values from a form
        * MeetingInvite.__init__(form)
            * MeetingInvite.__load_form(form), sets self.XXX values
                * MeetingInvite.__validate(), validates self.XXX values.
    
     if MeetingInvite.is_valid:     (is_valid is a bool set by __validate()
            if MeetingInvite.add():
                check if MeetingInvite.__already_exists, check if it already 
                exists.
                MeetingInvite.__add_to_invite_tbl, use auto_increment to set 
                self.id_invite.
                Meeting(), create a new meeting object
                Meeting.add(id_invite, start_datetime, end_datetime, 
                            meeting_chair)
    """
    def __init__(self, arg1=None):    
        # by default, a new object is True, self.__validate() will update 
        # the status.
        self.is_valid = True
        self.error = None
        
        if arg1 == None:
            # no arguments passed
            pass
        elif isinstance(arg1, (int, long)):
            # id_invite is an int, likely an existing id_meeting_invite
            # 1. craft the SQL, be explict
            # 2. execute the query
            # 3. check the rows returned, should be one.
            #    if 1 row returned:
            #        populate the right vales are return.
            #    else:
            #        log the error, set the flags
            #        return False
            sql = """
            SELECT idInvite, start_date, duration, end_date, recurring, 
                   invite_status, title, purpose, background_reading, agenda, 
                   requester_email_addr, venue, idMeetingTemplate, 
                   justification
            FROM Invite
            Where idInvite=%s
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
                self.error = "id_invite %s does not exist"
                logging.info(self.error)
            else:
                # looks like were good.
                self.id_invite = my_query_results[0][0]
                self.start_date = my_query_results[0][1]
                self.duration = my_query_results[0][2]
                self.end_date = my_query_results[0][3]
                self.recurring = my_query_results[0][4]
                self.invite_status = my_query_results[0][5]
                self.title = my_query_results[0][6]
                self.purpose = my_query_results[0][7]
                self.background_reading = my_query_results[0][8]
                self.agenda = my_query_results[0][9]
                self.requester = my_query_results[0][10]
                self.venue = my_query_results[0][11]
                self.id_template = my_query_results[0][12]
                self.justification = my_query_results[0][13]
                self.invitees_list = self.__get_invitees()
                
        elif arg1.getvalue('purpose'):
            # arg1 is a form object instance.
            #logging.info("MeetingTemplate() was passed a form as an object")
            form = arg1
            # error back to the calling class if we can't load the form.
            self.__load_form(form)
            
    def add(self):
        """add needs to do a few things:
        
        1. add a single row to the invite table.
        2. add a row for every meeting instance of the invite to the meeting 
           table.
           --> time to create meeting.add()?
        3. add all relevant rows for each invitee email for each meeting 
           instance to the participants table. 
           --> time to create participant.add()?
           1. add a single row to the invite table.
        """
        
        # MySQL retrieves and displays DATETIME values 
        # in 'YYYY-MM-DD HH:MM:SS' format. 
        self.start_datetime = self.start_date + " " + self.start_time + ":00"
        
        st = re.search('^(\d{2}):(\d{2})$', self.start_time)
        hh   = int(st.group(1))
        mm   = int(st.group(2)) 
        
        if self.end_date:
            # end_date:(start_time + duration) 
            ed = re.search('^(\d{4})-(\d{2})-(\d{2})$', self.end_date)
            YYYY = int(ed.group(1))
            MM   = int(ed.group(2))
            DD   = int(ed.group(3))
            self.end_datetime = datetime(YYYY, MM, DD, hh, mm) \
                                + timedelta(minutes=int(self.duration))
        else:
            # start_date:(start_time + duration)
            sd = re.search('^(\d{4})-(\d{2})-(\d{2})$', self.start_date)
            YYYY = int(sd.group(1))
            MM   = int(sd.group(2))
            DD   = int(sd.group(3))
            self.end_datetime = datetime(YYYY, MM, DD, hh, mm) \
                                + timedelta(minutes=int(self.duration))
        
        if not self.__already_exists():
            # 1. add to invite tbl
            logging.info("start __add_to_invite_tbl")
            self.__add_to_invite_tbl()
            logging.info("finish __add_to_invite_tbl, is_valid=%s" 
                         % self.is_valid)
            # if the __add_to_invite_tbl failed, it will set the is_valid 
            # bool to false  and stick the error message is self.error
            if self.is_valid == False:
                return
                
            # 2. add to the invitees tbl
            logging.info("start __add_to_inviteeeeeee_tbl")
            self.__add_to_invitee_tbl()
            logging.info("finish __add_to_inviteeeeeeee_tbl, is_valid=%s" 
                         % self.is_valid)
            if self.is_valid == False:
                return
            
            # set up the datetime variables for the very start and very 
            # end of the dates provided by the requester.
            dt_start   = datetime.strptime(self.start_datetime, 
                                               "%Y-%m-%d %H:%M:%S")
            dt_end     = self.end_datetime
    
            # 3. add to meeting tbl, a la Meeting.add()
            # 
            # if it's a recurring meeting, we'll need to iterate through and 
            # add several meeting instances.
            # if it's a non-recurring meeting, we only need to add a single 
            # meeting instance.
            #
            # we re-use the same db_connection for all of these, so we can do 
            # a single commit at the end.
            if self.recurring == "none":
                my_meeting = eamm.backend.meeting.Meeting()
                if self.db_connection:
                    my_meeting.db_connection = self.db_connection
                    my_meeting.add(self.id_invite, self.start_datetime, 
                                   self.end_datetime, 
                                   self.requester)
                else:
                    self.is_valid = False
                    self.error = "meeting_invite.add() self.db_connection is \
                    dead and can't be passed to my_meeting.db_connection"
                    logging.info(self.error)
                    return
            elif self.recurring == "weekly":
                # ok, weekly recurring meetings, can't be to hard to figure 
                # out dates.
                # we have a start_datetime and end_datetime from form.
                # we also have start_date and end_date from the form.
                #
                # while (start_date <= end_date):
                #    meeting.add(foo, bar, etc)
                #    start_date += 7 days
                #
                
                # check to make sure that the latest start date is still before 
                # the series end date
                while (dt_start <= dt_end):
                    # define the dates of the instance in the series.
                    mt_start = dt_start
                    mt_end   = dt_start + timedelta(minutes=int(self.duration))
                    logging.info("start: %s" % mt_start)
                    logging.info("end:   %s" % mt_end)
                        
                    # add the meeting to the Meeting table.
                    my_meeting = eamm.backend.meeting.Meeting()
                    if self.db_connection:
                        my_meeting.db_connection = self.db_connection
                        my_meeting.add(self.id_invite, mt_start, 
                                       mt_end, self.requester)
                    else:
                        self.is_valid = False
                        self.error = "meeting_invite.add() self.db_connection \
                        is dead and can't be passed to my_meeting.db_connection"
                        logging.info(self.error)
                    
                    # skip the start date forward 7 days.
                    dt_start += timedelta(days=7)
            elif self.recurring == 'monthly':
                my_dates = self.__recurr_every_X_months(dt_start, dt_end, 1)
                for d in my_dates:
                    mt_start = d
                    mt_end   = d + timedelta(minutes=int(self.duration))
                    logging.info("start: %s" % mt_start)
                    logging.info("end:   %s" % mt_end)
                        
                    # add the meeting to the Meeting table.
                    my_meeting = eamm.backend.meeting.Meeting()
                    if self.db_connection:
                        my_meeting.db_connection = self.db_connection
                        my_meeting.add(self.id_invite, mt_start, 
                                       mt_end, self.requester)
                    else:
                        self.is_valid = False
                        self.error = "meeting_invite.add() db_connection \
                        is dead and can't be passed to my_meeting"
                        logging.info(self.error)
            elif self.recurring == 'quarterly':
                my_dates = self.__recurr_every_X_months(dt_start, dt_end, 3)
                for d in my_dates:
                    mt_start = d
                    mt_end   = d + timedelta(minutes=int(self.duration))
                    logging.info("start: %s" % mt_start)
                    logging.info("end:   %s" % mt_end)
                        
                    # add the meeting to the Meeting table.
                    my_meeting = eamm.backend.meeting.Meeting()
                    if self.db_connection:
                        my_meeting.db_connection = self.db_connection
                        my_meeting.add(self.id_invite, mt_start, 
                                       mt_end, self.requester)
                    else:
                        self.is_valid = False
                        self.error = "meeting_invite.add() db_connection \
                        is dead and can't be passed to my_meeting"
                        logging.info(self.error)
            elif self.recurring == 'daily':
                my_dates = self.__recurr_daily(dt_start, dt_end)
                for d in my_dates:
                    mt_start = d
                    mt_end   = d + timedelta(minutes=int(self.duration))
                    logging.info("start: %s" % mt_start)
                    logging.info("end:   %s" % mt_end)
                        
                    # add the meeting to the Meeting table.
                    my_meeting = eamm.backend.meeting.Meeting()
                    if self.db_connection:
                        my_meeting.db_connection = self.db_connection
                        my_meeting.add(self.id_invite, mt_start, 
                                       mt_end, self.requester)
                    else:
                        self.is_valid = False
                        self.error = "meeting_invite.add() db_connection \
                        is dead and can't be passed to my_meeting"
                        logging.info(self.error)
                  
            # if the my_meeting.add() method failed, it will set the is_valid 
            # bool to false and stick the error message is self.error
            if self.is_valid == False:
                    
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
                    return
                
            eml_inv = eamm.backend.email_invite.EmailInvite(self.id_invite) 
            eml_inv.send()
             
            return True
            
    def __add_to_invitee_tbl(self):
        # row format:
        #    idInvite, invitee_email_addr
        # local attribute = self.invitees_list
        
        for this_addr in self.invitees_list:
            sql = """INSERT INTO Invitee (idInvite, invitee_email_addr) 
            VALUES (%s, %s)"""
            sql_vars= [self.id_invite, this_addr]
            
            my_db_connection = self.db_connection
            my_db_connection.insert2(sql, sql_vars)
            
            if self.is_valid == False:
                self.error = "Error at MeetingInvite.__add_to_invitee_tbl()"
                logging.info(self.error)
                return
        
        return True
                
    def __add_to_invite_tbl(self):
        # row format:
        #   idInvite, start_date, duration, end_date, recurring, invite_status, 
        # title, purpose, background_reading, agenda, requester_email_addr, 
        # venue, idMeetingTemplate  

        sql = """
        INSERT into Invite (start_date, duration, end_date, recurring, 
                            invite_status, title, purpose, background_reading, 
                            agenda, requester_email_addr, venue, 
                            idMeetingTemplate, justification) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """ 
        sql_vars= [self.start_datetime, self.duration, self.end_datetime, 
                   self.recurring, "ACTIVE", self.title, self.purpose, 
                   "NONE", self.agenda, self.requester, self.venue,
                   self.id_template, self.justification]
        
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
                self.error = "Error at MeetingInvite.__add_to_invite_tbl() " \
                           + "Couldn't create MyDatabase object"
                return False
                
        # execute the insert2, if it worked, the returned value will be the 
        # auto-incremented PK value for the fresh insert
        my_last_insert_id = my_db_connection.insert2(sql, sql_vars, 
                                                     auto_increment)
        if not my_last_insert_id:      
            self.is_valid = False
            self.error = "Error at MeetingInvite.__add_to_invite_tbl() " \
                       + "Couldn't insert row(%s)" % my_db_connection.error
            return False
        else:
            logging.info("MeetingInvite.__add_to_invite_tbl() " \
                       + "my_last_insert_id: type(%s), value %s" \
                       % (type(my_last_insert_id), my_last_insert_id))
            # check that the return code is indeed good, and use it to set 
            # self.id_invite
            if my_last_insert_id > 0:  
                self.id_invite = my_last_insert_id
                logging.info("MeetingInvite.__add_to_invite_tbl() " \
                           + "self.id_invite set to %s", self.id_invite)
                return True
            else:
                self.is_valid = False
                self.error = "Error at MeetingInvite.__add_to_invite_tbl() " \
                           + "self.id_invite could not be set, "             \
                           + "last_insert_id is %s" % my_last_insert_id
                logging.info(self.error)
                return False

    
    def __already_exists(self):    
        sql = """
        SELECT count(*) from Invite 
        WHERE (start_date=%s AND 
               duration=%s AND 
               invite_status='ACTIVE' AND 
               title=%s AND
               purpose=%s AND 
               agenda=%s AND 
               requester_email_addr=%s
              )
        """
        
        sql_vars = [self.start_datetime, self.duration, self.title, 
                    self.purpose, self.agenda, self.requester]
        
        # open a DB connection and check it.
        my_db_connection = eamm.backend.database.MyDatabase()
        if not my_db_connection:
            self.is_valid = False
            self.error = "Error at MeetingInvite.__add_to_invite_tbl: " \
                       + "Couldn't create MyDatabase object"
            return False
        
        # execute the select and check to make sure it worked.
        my_query_results = my_db_connection.select2(sql, sql_vars)
        if not my_query_results:
            self.is_valid = False
            self.error = "Error at MeetingInvite.__already_exists: Couldn't " \
                       + "select row, Message: %s" % my_db_connection.error
            return False
        else:
            if my_query_results[0][0] == 0:
                # this means the select got back nothing.
                logging.info("Invite for %s does NOT already exist in DB" 
                             % self.title)
                return 0
            else:
                logging.info("Invite for %s DOES already exist in DB" 
                             % self.title)
                self.error = "An identical meeting for \"%s\" " % self.title \
                           + "is already scheduled!"
                self.is_valid = False
                return True

    
    def __load_form(self, form):
        # initialize all key class attributes from form data.            
        # check to make sure all fields have stuff in them.
        if not all((form.getvalue('purpose'), form.getvalue('justification'), 
                    form.getvalue('template'), form.getvalue('agenda'), 
                    form.getvalue('title'), form.getvalue('start_date'),
                    form.getvalue('start_time'), form.getvalue('recurring'),
                    form.getvalue('venue'),
                    form.getvalue('requester'), form.getvalue('invitees'))):
            self.is_valid = False
            self.error = "Error at MeetingInvite.__load_form: Not all form " \
                       + "fields contain data"
            return False
        
        self.purpose = form.getvalue('purpose')             # wysiwyg html
        self.justification = form.getvalue('justification') # wysiwyg html
        self.id_template = form.getvalue('template')        # integer
        self.agenda = form.getvalue('agenda')               # wysiwyg html
        self.title = form.getvalue('title')                 # string
        self.start_date = form.getvalue('start_date')       # yyyy-mm-dd str
        self.start_time = form.getvalue('start_time')       # hh:mm 24 hr str 
        self.duration = form.getvalue('duration')           # mm str
        self.recurring = form.getvalue('recurring')         # str
        if form.getvalue('end_date'):                       # optional 
            self.end_date = form.getvalue('end_date')       # yyyy-mm-dd str
        else:
            self.end_date = None
        self.venue = form.getvalue('venue')                 # str
        self.requester = form.getvalue('requester')         # email_addr str
        self.invitees = form.getvalue('invitees')           # wysiwyg html     
        
        # TODO, remove once testing complete.
        logging.info("Show me the invitee list from form: %s" % self.invitees)
        
        if not self.__validate():
            self.is_valid = False
            self.error = "Error at MeetingInvite.__load_form: Couldn't " \
                       + "validate form" 
            logging.info(self.error)
            return False
        else:
            return True
    
    
    def __validate(self):
    # just check to make sure dates and times are in the correct format to be 
    # parsed for mysql datetimes, etc.
    # The DATETIME type is used for values that contain both date and time 
    # parts MySQL retrieves and displays DATETIME values in 
    # 'YYYY-MM-DD HH:MM:SS' format. The supported range is 
    # '1000-01-01 00:00:00' to '9999-12-31 23:59:59'.
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
            self.error = "bad start date: %s" % self.start_date
            logging.info("Error at MeetingInvite.__validate: %s" % self.error)
        #else:
            #logging.info("good start_date: %s" % self.start_date)
        
        if self.end_date:
            result2 = re.search(regex_date, self.end_date)
            if result2 == None:
                self.is_valid = False
                self.error = "bad end_date: %s" % self.end_date
                logging.info("Error at MeetingInvite.__validate: %s" \
                             % self.error)
            #else:
            #    logging.info("good end_date: %s" % self.end_date)

        result3 = re.search(regex_time, self.start_time)
        if result3 == None:
            self.is_valid = False
            self.error = "bad start_time: %s" % self.start_time
            logging.info("Error at MeetingInvite.__validate: %s" % self.error)
        #else:
        #    logging.info("good start_time: %s" % self.start_time)

        result4 = re.search(regex_duration, self.duration)
        if result4 == None:
            self.is_valid = False
            self.error = "bad duration: %s" % self.duration
            logging.info("Error at MeetingInvite.__validate: %s" % self.error)
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
            logging.info("MeetingInvite.__validate, invitees line: %s" \
                         % line)
            
            # get rid of HTML tags with a non-greedy search and replace.
            line = re.sub("<.*?>", "", line)
            logging.info("MeetingInvite.__validate, invitees stripped %s" \
                         % line)
        
            if re.match('^[\w\-\.]+@[\w\.\-]+\.\w+$', line):
                # the above is a crude regex for an email address.
                logging.info("MeetingInvite.__validate, invitees, is an " \
                           + "email address: %s" % line)
                invitee_list.append(line)
            elif re.match('\W+$', line):
                # it's a pure white space line, so skip it.
                logging.info("MeetingInvite.__validate, invitees, is " \
                           + "non-word chars, skipping")
                pass
            else:
                # bugs crud
                logging.info("MeetingInvite.__validate, invitees, is " \
                           + "NOT an email address: %s" % line)
                self.error = "MeetingInvite.__validate, invitees, is " \
                           + "NOT an email address: %s" % line
                self.is_valid = False
            i+=1
        
        # if there are no email's then it's false.
        if len(invitee_list) <= 0:
            self.is_valid = False
            self.error = "Error at MeetingInvite.__validate, no valid email " \
                       + "addrs for invitees"
            logging.info(self.error)
            
        # initialize a new object attribute for the sanitized 
        # invitee email_addr list        
        self.invitees_list = invitee_list
        logging.info("emails: %s", tuple(self.invitees_list))
        
        return self.is_valid
    
    
    def test(self, start_date, requester):
        """
        self.purpose = form.getvalue('purpose')             # wysiwyg html 
        self.justification = form.getvalue('justification') # wysiwyg html 
        self.id_template = form.getvalue('template')        # integer
        self.agenda = form.getvalue('agenda')               # wysiwyg html 
        self.title = form.getvalue('title')                 # string
        self.start_date = form.getvalue('start_date')       # yyyy-mm-dd str
        self.start_time = form.getvalue('start_time')       # hh:mm 24 hr str 
        self.duration = form.getvalue('duration')           # mm str
        self.recurring = form.getvalue('recurring')         # str
        self.end_date = None
        self.venue = form.getvalue('venue')                 # str
        self.requester = form.getvalue('requester')         # email_addr str
        self.invitees_list                                  # list
        """
        
        self.db_connection = eamm.backend.database.MyDatabase(autocommit="off")
        fluff = randint(100,999)
        self.requester = requester
        self.start_date = start_date
        self.title = "%s: this is a test meeting by %s on %s" % (fluff, 
                                                                 requester, 
                                                                 start_date)
        self.purpose = "%s: this is a test meeting by %s on %s" %(fluff, 
                                                                  requester, 
                                                                  start_date)
        self.justification = "test"
        self.id_template = 2
        self.agenda = "test %s" % fluff
        self.start_date = start_date
        self.start_time = "09:00"
        self.duration = "45"
        self.recurring = "none"
        self.end_date = self.start_date
        self.venue = "test"
        self.invitees_list = ['a@a.com', 'b@b.com']

        
    def __get_invitees(self):
        sql = """
        SELECT invitee_email_addr 
        FROM Invitee 
        WHERE idInvite=%s 
        ORDER BY invitee_email_addr
        """
        sql_vars = [self.id_invite]
    
        my_db_conn = eamm.backend.database.MyDatabase()
        my_query_results = my_db_conn.select2(sql, sql_vars)
            
        if not my_query_results:
            self.is_valid = False
            self.error = my_db_conn.error
            logging.info("__get_invitees: db connection failed")
        elif len(my_query_results) == 0:
            self.is_valid = False
            self.error = "id_invite %s does not exist"
            logging.info(self.error)
        else:
            # looks like were good.
            invitees_list = list()
            for item in my_query_results:
                invitees_list.append(item[0])
        
        #invitees_list = ['a@a.com', 'b@b.com']    
        return invitees_list  
    
    
    # return a list of dates (in datetime format) that recur every m months
    # betwen the datetime inputs of d1 and d2
    def __recurr_every_X_months(self, d1, d2, m):
        dlist = list()     
        d_temp = d1
        n = 4       # skipping forward 4 weeks at a time.
        count = 0   # running counter
    
        while d_temp <= d2:
            if count % m == 0:
                dlist.append(d_temp)
            count += 1
            d_temp =  self.__next_month(d_temp, n)

        return dlist

    # the next relative day of the month is either 4 or 5 weeks into
    # the future
    def __next_month(self, d, n):
        d_next = d + timedelta(weeks=n)
        if self.__weekday_index(d_next) < self.__weekday_index(d):
            d_next += timedelta(weeks=1)
        return d_next

    # d is a datetime.date object.
    def __weekday_index(self,d):
        return (d.day + 6) // 7  
    
    def __recurr_daily(self, d1, d2):
        dlist = list(rrule(DAILY, 
                           byweekday=(MO,TU,WE,TH,FR),
                           dtstart=d1,
                           until=d2))
        return dlist