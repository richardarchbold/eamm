import sys
sys.path.append("/home/richard/workspace/eamm/")

# using this to determine GET or POST.
import logging
import eamm.frontend.base_webpage
import eamm.backend.database
import eamm.backend.meeting_invite

# setup basic logging config
logging.basicConfig(filename="/var/log/eamm.log",level=logging.INFO)

class MeetingWebPage(eamm.frontend.base_webpage.WebPage):
    def __init__(self):
        super(MeetingWebPage, self).__init__()
        self.user = ""
    
    def display(self, user):
        self.user = user
        
        try:
            user_meetings = self.__get_recent_meetings()
        except Exception as e:
            err = self.error_table("Could not load initial meetings - %s" % e)
            self.add_to_body(err)
            return
        
        rowspan = len(user_meetings) + 1
        
        self.set_title("View Meetings for %s" % self.user)
    
        html = """
        <TABLE>
          <TR>
            <TD colspan="6" class="aqua"> Quick View - My Meetings +/- 7 days 
            </TD>
          </TR>

          <TR>
            <TD rowspan="%s" class="col1n"> </TD>
            <TD class="col2_top" style="width: 65px;">Date</TD>
            <TD class="col2_top" style="width: 65px;">Venue</TD>
            <TD class="col2_top" style="width: 60px;">Requester</TD>
            <TD colspan="2" class="col2_top">Title</TD>
          </TR>
        """ % rowspan
        
        for row in user_meetings:
            url = "http://127.0.0.1/eamm/private/view_meeting.py"
            link = """
            <a href="%s?var1=%s">%s</a>
            """ % (url, row[5], row[4])
            html += """
            <TR>
              <TD>%s</TD>
              <TD>%s</TD>
              <TD>%s</TD>
              <TD colspan="2">%s</TD>
            </TR>
            """ % (row[0], row[2], row[3], link)

        html += """</table>
        <br>
        <form name="search_meetings" method="post"
         action="/eamm/private/view_meetings.py"> 
        <table>

          <TR>
            <TD colspan="4" class="aqua">Advanced Search</TD>
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
              <input type="text" id="text_search" name="text_search"/>
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
        """
        
        self.add_to_body(html)
        return
    
    
    def __get_recent_meetings(self):
        db_conn = eamm.backend.database.MyDatabase()
        sql = """
        select m.start_time, i.duration, i.venue, 
               i.requester_email_addr, i.title, m.idMeeting
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
        order by m.start_time desc
        """
            
        sql_vars = [self.user, self.user]
        rows = db_conn.select2(sql, sql_vars)
           
        return rows        
    
    def display_this_meeting(self, id_meeting):
        this_meeting = eamm.backend.meeting.Meeting(id_meeting)
        id_invite = this_meeting.id_invite
        this_invite  = eamm.backend.meeting_invite.MeetingInvite(id_invite)
        
        self.set_title("View Meeting Titled: \"%s\"" % this_invite.title)
        
        # self.requester, self.invitees, self.title, self.start_date, 
        # self.start_time, self.duration, self.recurring, self.end_date, 
        # self.venue, self.template_title, self.purpose, self.agenda,
        # self.button
        
        self.requester      = this_invite.requester
        self.invitees       = this_invite.invitees_list
        self.title          = this_invite.title
        self.start_date     = this_meeting.start_datetime
        self.start_time     = "FIXME"
        self.duration       = this_invite.duration
        self.recurring      = this_invite.recurring
        self.end_date       = this_meeting.end_datetime
        self.venue          = this_invite.venue
        self.template_title = "FIXME"
        self.purpose        = this_invite.purpose
        self.agenda         = this_invite.agenda
        self.button         = "OK"
         
        html = self.display_meeting_invite_table()
        
        self.add_to_body(html)
        
        return
    