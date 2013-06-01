# import necessary eamm modules.
import eamm.frontend.base_webpage 
import eamm.backend.survey
import eamm.backend.meeting
import eamm.backend.meeting_invite

# Import modules for CGI handling , the cgitb modules gives descriptive debug 
# errors to the browser.
import cgi
import cgitb; cgitb.enable(display=1)

# Import these for query string parsing.
from urlparse import parse_qs
import re

# setup basic logging config
import logging
logging.basicConfig(filename="/var/log/eamm.log",level=logging.INFO)

class SurveyWebpage(eamm.frontend.base_webpage.WebPage):
    #############
    #
    def __init__(self):
        super(SurveyWebpage, self).__init__()
        self.js = '<script type="text/javascript" \
                    src="http://127.0.0.1/eamm/js/eamm.js"></script>'
        self.is_valid     = True
        self.error        = False
        self.query_string = False
        self.error_base   = "Class: SurveyWebPage, Method: %s, Error: %s"
    #
    ############

    #############
    # 
    def show_outstanding_surveys(self, user):
        title = "Meetings requiring Survey Completion for %s" % user
        self.set_title(title)
        
        try:
            uncompleted_surveys = self.__get_uncompleted_surveys(user)
        except Exception as e:
            err = self.error_table("Could not get surveys - %s" % e)
            self.add_to_body(err)
            return
        
        # because the headings are also a row
        rowspan = len(uncompleted_surveys) + 1
        
        html = """
        <TABLE>
          <TR>
            <TD colspan="6" class="aqua"> %s </TD>
          </TR>

          <TR>
            <TD rowspan="%s" class="col1n"> </TD>
            <TD class="col2_top" style="width: 70px;">Date</TD>
            <TD class="col2_top" style="width: 65px;">Venue</TD>
            <TD class="col2_top" style="width: 60px;">Requester</TD>
            <TD class="col2_top">Title</TD>
            <TD class="col2_top">Action</TD>
          </TR>
        """ % (title, rowspan)
        
        for row in uncompleted_surveys:
            html += self.__add_survey_row(row)
            pass
        
        html += """</table>
        <br>
        """
        
        self.add_to_body(html)
        return   
    #
    ############ 
    
    #############
    # 
    def __add_survey_row(self, row):
        url1 = "http://127.0.0.1/eamm/private/view_meeting.py"
        url2 = "http://127.0.0.1/eamm/private/complete_survey.py"
        
        # http://127.0.0.1/eamm/complete_survey.py?var1=117&var2=c@c.com
        
        # row[0] = m.start_time,      # row[1] = i.duration, 
        # row[2] = i.venue            # row[3] = i.requester_email_addr,
        # row[4] = i.title            # row[5] = m.idMeeting
        
        link1 = """
        <a href="%s?var1=%s">View Meeting</a>
        """ % (url1, row[5])
        
        link2 = """
        <a href="%s?var1=%s&var2=%s">Complete Survey</a>
        """ % (url2, row[5], row[3])
        
        link = "%s<br>%s" % (link1, link2)
        
        tmp = """
            <TR>
              <TD>%s</TD>
              <TD>%s</TD>
              <TD>%s</TD>
              <TD>%s</TD>
              <TD>%s</TD>
            </TR>
        """ % (row[0], row[2], row[3], row[4], link)

        return tmp
    #
    ############ 
    
    #############
    #     
    def __get_uncompleted_surveys(self, user):
        sql = """
        select m.start_time, i.duration, i.venue, i.requester_email_addr, 
               i.title, m.idMeeting
        from EAMM.Meeting as m 
          INNER JOIN EAMM.Invite as i 
          INNER JOIN EAMM.Invitee as v
            ON (m.idInvite = i.idInvite and m.idInvite = v.idInvite)
        where m.meeting_status='SCHEDULED' 
          and m.end_time<=date_add(now(), interval -15 minute)
          and v.invitee_email_addr=%s
	  and i.requester_email_addr!=%s
          and m.idMeeting not in (
            select idMeeting 
            from EAMM.Survey
            where responder_email_addr=%s
           )
        """
        sql_vars = [user, self.remote_user, self.remote_user]
        db_conn = eamm.backend.database.MyDatabase()
        rows = db_conn.select2(sql, sql_vars)
            
        return rows
    #
    ############
  
    #############
    #    
    def show_survey(self, query_string):
        # Flow of this method ...
        # 
        # 1. parse & validate query_string, populating self.id_meeting and 
        #    self.email_addr the query string should be something like:
        #    1234&me%40amazon%2Ecom    (%40 = @ , %2E = .)
        #    
        # 2. instantiate the relevant meeting and invite objects, well 
        #    need them to print the top part of the page.
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
            return
        
        # need to write a method to load a meeting object if it's passed an 
        # id_meeting  on instantiation 
        self.meeting_obj = eamm.backend.meeting.Meeting(self.id_meeting)
        if not self.meeting_obj.is_valid:
            self.error_table(self.meeting_obj.error)
            return
        
        # need to write a method to load a meeting invite object if it's passed 
        # an id_invite on instantiation (partially stubbed out at the __init__ 
        # level
        self.invite_obj = eamm.backend.meeting_invite.MeetingInvite(self.meeting_obj.id_invite)
        if not self.invite_obj.is_valid:
            self.error_table(self.invite_obj.error)
            return
        
        # need to write the function to get_questions based on id_template.
        self.survey_questions = eamm.backend.survey.get_questions(self.invite_obj.id_template)
        if not self.survey_questions:
            self.error_table("could not get survey questions for %s" \
                             % self.id_template)
            return
        
        self.__show_survey()
    #
    ############
    
    #############
    #
    def process_survey(self):
        self.set_title("THANK YOU, the survey is complete!")
        form = cgi.FieldStorage()
        
        for i in form.keys():
            logging.info("survey key:%s, val:%s<br>\n" % (i, form.getvalue(i)))
            #self.add_to_body("survey key: %s, value: %s<br>\n" % (i, form.getvalue(i)))
        
        my_survey = eamm.backend.survey.SurveyResponse(form)
        try:
            my_survey.add()
            self.add_to_body(self.simple_table("Thanks, Survey Stored \
                                                Successfully"))
        except Exception as e:
            self.add_to_body(self.error_table("Unfortunately, the Survey \
                                               could not be stored: %s")
                             % str(e))
            
        return
    #
    ############

    #############
    #    
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
            tmp = "SurveyWebpage().__parse_query_string()"
            self.error = "%s: %s not an int" % (tmp, qs['var1'])
            logging.info(self.error)
            self.is_valid = False
            return False

        # re.match('^[\w\-\.]+@[\w\.\-]+\.\w+$', line):
        logging.info("qs var2 = \"%s\"" % qs['var2'][0])
        if re.match('^[\w\-\.]+@[\w\.\-]+\.\w+$',qs['var2'][0]):
            self.email_addr = qs['var2'][0]
        else:
            tmp = "Class: survey_webpage, Method: __parse_query_string"
            self.error = "%s, var2 not an email_addr: %s" % (tmp, qs['var2'])
            logging.info(self.error)
            self.is_valid = False
            return False
    
        return True
    #
    ############ 
 
    #############
    #    
    def __show_survey(self):
        # this just prints out the HTML
        self.set_title("Meeting Effectiveness Survey")
        
        self.js = """
        <script type="text/javascript" src="http://127.0.0.1/eamm/js/eamm.js"></script>
        """
        
        html = """
        
        <form action="/eamm/private/complete_survey.py" id="survey" method="post" onsubmit="return(validateSurvey());">
        <input type="hidden" name="id_invite" value="%s" />
        <input type="hidden" name="id_meeting" value="%s" />
        <input type="hidden" name="email_addr" value="%s" />
        <input type="hidden" name="responder_email_addr" value="%s" />
        <table>
          
          <TR>
            <TD rowspan="6" class="col1">For which meeting?</TD>
            <TD class="sub_col_1">Date & Time</TD>
            <TD>%s</TD>
          </TR>
            
          <TR>
            <TD class="sub_col_1">Subject</TD>
            <TD>%s</TD>
          </TR>
            
          <TR>
            <TD class="sub_col_1">Purpose</TD>
            <TD>%s</TD>
          </TR>

          <TR>
            <td class="sub_col_1">Justification</td>
            <td>%s</td>
          </TR>

          <TR>
            <td class="sub_col_1">Agenda</td>
            <td>%s</td>
          </TR>
        """ % (self.invite_obj.id_invite, self.meeting_obj.id_meeting, 
               self.email_addr, self.remote_user, 
               self.meeting_obj.start_datetime, 
               self.invite_obj.title, self.invite_obj.purpose, 
               self.invite_obj.justification, self.invite_obj.agenda)
        
        html += """
            <TR>
              <td class="sub_col_1">Invitees</td>
              <td>%s</td>
            </TR> 
        """ % " ".join(self.invite_obj.invitees_list)
        
        html += """
            <TR>
              <TD colspan="3" class="aqua">To what extent do you agree or disagree with the following
              questions?</TD>
            </TR>
        """
    
        count = 0
        for row in self.survey_questions:
            # tmpArray[i] = tmpArray[i].replace(/<.*>/g,"");
            temp = re.sub("John Doe", self.invite_obj.requester, row[1])
            html_question = """
            <!-- beginning HTML block for a single question -->
            <TR>
              <TD rowspan="2" class="col1">Question %s</td>
              <td colspan="2" class="col2_top">%s</td>
            </tr>
            
            <tr>
              <td colspan="2" class="col2_bottom">
                <input type="radio" name="%s" value="0">Strongly Disagree
                <input type="radio" name="%s" value="25">Disagree
                <input type="radio" name="%s" value="50">Neutral
                <input type="radio" name="%s" value="75">Agree
                <input type="radio" name="%s" value="100">Strongly Agree
              </td>
            </tr>
            <!-- ending HTML block for a single question -->
            """ % (count+1, temp, row[0], row[0], row[0], row[0], row[0])
            
            count += 1
            html += html_question
        
        html += """
            <tr>
              <td colspan="3" class="header"><input type="submit" value="Submit"/></td>
            </tr>
          </table>
          </form>
        
        """
        
        self.add_to_body(html)
    #
    ############ 
