import sys
sys.path.append("/home/richard/workspace/eamm/")

# using this to determine GET or POST.
import logging
import eamm.frontend.base_webpage
import eamm.backend.database
import eamm.backend.meeting_invite
import eamm.backend.meeting_template
import re

# setup basic logging config
logging.basicConfig(filename="/var/log/eamm.log",level=logging.INFO)

class MeetingWebPage(eamm.frontend.base_webpage.WebPage):
    #############
    # 
    def __init__(self):
        super(MeetingWebPage, self).__init__()
        self.user = None
        self.form = None
        self.table_top = """
        <TABLE>
          <TR>
            <TD colspan="6" class="aqua"> %s </TD>
          </TR>

          <TR>
            <TD rowspan="%s" class="col1n"> </TD>
            <TD class="col2_top" style="width: 65px;">Date</TD>
            <TD class="col2_top" style="width: 65px;">Venue</TD>
            <TD class="col2_top" style="width: 60px;">Requester</TD>
            <TD colspan="2" class="col2_top">Title</TD>
          </TR>
        """
    #
    ############
    
    #############
    # 
    def display(self, user):
        self.user = user
        
        try:
            user_meetings = self.__get_recent_meetings()
        except Exception as e:
            err = self.error_table("Could not load initial meetings - %s" % e)
            self.add_to_body(err)
            return
        
        rowspan = len(user_meetings) + 1
        
        # add datepicker JS
        self.js += self.datepicker_js
        
        self.set_title("View Meetings for %s" % self.user)
    
        html = """
        <form name="search_meetings" method="post"
         action="/eamm/private/view_meetings.py"> 
        <table>

          <TR>
            <TD colspan="4" class="aqua">Advanced Search<br>Search for meetings
              in which you are the requester or an invitee</TD>
          </TR>

          <TR>
            
            <TD rowspan="2" class="col1n"> </TD>
            
            <TD class="col2_top" style="width: 60px;">Start Date:<br>
              <input type="text" id="start_date" name="start_date" 
                value="yyyy-mm-dd" size=10/>
            </TD>
            
            <TD class="col2_top" style="width: 60px;">End Date:<br>
              <input type="text" id="end_date" name="end_date" 
                value="yyyy-mm-dd" size="10"/>
            </TD>
            
            <TD class="col2_top">Title Text:<br>
              <input type="text" id="text_search" name="text_search" size="60"/>
            </TD>
            
          </TR>

          <TR>
            <TD colspan="3">
              <div align="center">
                <input type="submit" value="Search"/>
              </div>
            </TD>
          </TR>

        </TABLE>
        </form>
        <br><br>
        """
    
        table_title = "Quick View - My Meetings +/- 7 days"
        html += self.table_top % (table_title, rowspan)
        
        for row in user_meetings:
            html += self.__add_meeting_row(row)
        
        html += """</table>
        <br>
        """
        
        self.add_to_body(html)
        return
    #
    ############
    
    #############
    #    
    def display_search_results(self, user, form): 
        self.user = user
        self.form = form
        
        table_title = "Search Results"
        self.set_title(table_title)
        
        try:
            search_results = self.__search()
        except Exception as e:
            err = self.error_table("Could not search for  meetings - %s" % e)
            self.add_to_body(err)
            return
        
        # because the headings are also a row
        rowspan = len(search_results) + 1
        
        html = self.table_top % (table_title, rowspan)

        for row in search_results:
            html += self.__add_meeting_row(row)
        
        html += """</table>
        <br>
        """
        
        self.add_to_body(html)
        return   
    #
    ############
    
    #############
    # 
    def __add_meeting_row(self, row):
        url = "http://127.0.0.1/eamm/private/view_meeting.py"
        
        # row[0] = m.start_time,      # row[1] = i.duration, 
        # row[2] = i.venue            # row[3] = i.requester_email_addr,
        # row[4] = i.title            # row[5] = m.idMeeting
        
        link = """
        <a href="%s?var1=%s">%s</a>
        """ % (url, row[5], row[4])
        
        tmp = """
            <TR>
              <TD>%s</TD>
              <TD>%s</TD>
              <TD>%s</TD>
              <TD colspan="2">%s</TD>
            </TR>
        """ % (row[0], row[2], row[3], link)

        return tmp
    #
    ############
    
    #############
    # 
    def display_this_meeting(self, id_meeting):
        this_meeting  = eamm.backend.meeting.Meeting(id_meeting)
        id_invite     = this_meeting.id_invite
        this_invite   = eamm.backend.meeting_invite.MeetingInvite(id_invite)
        this_template = eamm.backend.meeting_template.MeetingTemplate()
        this_template.get(this_invite.id_template)
        
        m = re.search('^(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):\d+$', 
                      str(this_meeting.start_datetime))
        
        logging.info(str(this_meeting.start_datetime))
        YYYY = m.group(1)
        MM   = m.group(2)
        DD   = m.group(3)
        hh   = m.group(4)
        mm   = m.group(5) 
    
        start_date = "%s-%s-%s" % (YYYY, MM, DD)
        start_time = "%s:%s" % (hh, mm)
        
        self.set_title("View Meeting Titled: \"%s\"" % this_invite.title)
        
        # self.requester, self.invitees, self.title, self.start_date, 
        # self.start_time, self.duration, self.recurring, self.end_date, 
        # self.venue, self.template_title, self.purpose, self.agenda,
        # self.button
        
        self.requester      = this_invite.requester
        self.invitees       = this_invite.invitees_list
        self.title          = this_invite.title
        self.start_date     = start_date
        self.start_time     = start_time
        self.duration       = this_invite.duration
        self.recurring      = this_invite.recurring
        self.end_date       = this_meeting.end_datetime
        self.venue          = this_invite.venue
        self.template_title = this_template.title
        self.purpose        = this_invite.purpose
        self.agenda         = this_invite.agenda
         
        html = self.display_meeting_invite_table()
        
        self.add_to_body(html)
        
        return
    #
    ############
    
    #############
    #    
    def __search(self): 
        sql = """
        select  m.start_time, i.duration, i.venue, i.requester_email_addr,
                i.title, m.idMeeting
        from EAMM.Meeting as m, 
          EAMM.Invite as i, 
          EAMM.Invitee as v
        where m.idInvite=i.idInvite
          and m.idInvite=v.idInvite
          and m.idInvite=v.idInvite
          and (
               v.invitee_email_addr=%s
               OR
               i.requester_email_addr=%s
              )
        """ 
        sql_vars = [self.user, self.user]
        
        if self.form.getvalue('start_date') != 'yyyy-mm-dd':
            sql += """
               and m.start_time > %s
            """
            sql_vars.append(self.form.getvalue('start_date'))
           
        if self.form.getvalue('end_date') != 'yyyy-mm-dd':
            sql += """
               and m.end_time > %s
            """
            sql_vars.append(self.form.getvalue('end_date'))
            
        if self.form.getvalue('text_search'):
            text_search = self.form.getvalue('text_search')
            escaped_text_search = "%%%s%%" % text_search
            
            sql += """
               and (
                    i.title like %s
                    or
                    i.purpose like %s
                    )
            """
            sql_vars.append(escaped_text_search)
            sql_vars.append(escaped_text_search)
        
        sql += """
	group by m.idMeeting
        order by m.start_time
        """
        
        logging.info("meetingwebpage__search sql: %s" % sql) 
        db_conn = eamm.backend.database.MyDatabase()
        rows = db_conn.select2(sql, sql_vars)
            
        return rows
    #
    ############ 
    
    #############
    # 
    def __get_recent_meetings(self):
        db_conn = eamm.backend.database.MyDatabase()
        sql = """
        select m.start_time, i.duration, i.venue, i.requester_email_addr, 
               i.title, m.idMeeting
        from EAMM.Meeting as m, 
          EAMM.Invite as i,
          EAMM.Invitee as v
        where m.idInvite=i.idInvite 
          and m.idInvite=v.idInvite
          and m.start_time <= date_add(now(), interval 7 day)
          and m.start_time >= date_add(now(), interval -7 day)
          and (
            v.invitee_email_addr=%s
            OR
            i.requester_email_addr=%s
          )
        group by m.idMeeting
        order by m.start_time desc
        """
            
        sql_vars = [self.user, self.user]
        rows = db_conn.select2(sql, sql_vars)
           
        return rows        
    #
    ############
        
