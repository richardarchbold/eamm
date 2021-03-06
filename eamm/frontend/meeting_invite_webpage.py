
# import necessary eamm modules.
import eamm.frontend.base_webpage 
import eamm.backend.meeting_template
import eamm.backend.meeting_invite
import eamm.backend.database

# Import modules for CGI handling , the cgitb modules gives descriptive debug errors to the browser.
import cgitb; cgitb.enable(display=1)

import logging

# setup basic logging config.
logging.basicConfig(filename='/var/log/eamm.log',level=logging.INFO)

class MeetingInviteWebPage(eamm.frontend.base_webpage.WebPage):

    def __init__(self):
        super(MeetingInviteWebPage, self).__init__()
        self.tinymce_js = """

<!-- START JS :: WYSIWYG TEXTAREA --> 

<script type="text/javascript" src="/eamm/tinymce/jscripts/tiny_mce/tiny_mce.js"></script>

<script type="text/javascript">
                tinyMCE.init({
                    mode : "textareas",
                    theme : "advanced",
                    theme_advanced_buttons1 : "mybutton,bold,italic,underline,separator,strikethrough,justifyleft,justifycenter,justifyright, justifyfull,bullist,numlist,undo,redo,link,unlink",
                    theme_advanced_buttons2 : "",
                    theme_advanced_buttons3 : "",
                    theme_advanced_toolbar_location : "top",
                    theme_advanced_toolbar_align : "left",
                    theme_advanced_statusbar_location : "bottom",            
                });
                
</script>

<!-- END JS :: WYSIWYG TEXTAREA --> 
            """
    
    def add_meeting_invite_step_1(self):
        self.set_title("Create a new meeting invite :: Step 1")   
      
        html = """
        <form id="add_meeting_invite" name="add_meeting_invite" method="post" action="/eamm/private/add_meeting_invite.py"> 
        <input type="hidden" name="step" value="step1" />
        
        <table>
          <tr>
            <td rowspan="2" class="col1">Purpose</td>
            <td colspan="2" class="col2_top">It is critically important that your meeting has a clear
            purpose. It should be clear to everyone why the meeting is taking in place, what should
            be accomplished during the meeting, and what is expected of everyone. </td>
          </tr>

          <tr>
            <td colspan="2" class="col2_bottom"><textarea id="purpose" name="purpose" cols="80" rows="3" class="txt_area">The purpose of this meeting is to XXX such that YYY can be achieved.</textarea></td>
          </tr>
        
          <tr>
            <td rowspan="2" class="col1">Justification</td>
            <td colspan="2" class="col2_top">Not every goal or task requires a meeting to be accomplished.
            Why do you need to call a meeting in this instance?</td>
          </tr>

          <tr>
            <td colspan="2" class="col2_bottom"><textarea id="justification" name="justification" cols="80" rows="3" class="txt_area">A meeting is the best way to achieve my purpose because ...</textarea></td>
          </tr>
        
        """
        
        my_templates = eamm.backend.meeting_template.MeetingTemplate()
        all_templates = my_templates.get_all()
        colspan = len(all_templates) + 1
        
        html += """
          <tr>
            <td rowspan="%s" class="col1">Template</td>
            <td colspan="2" class="col2_top">Please choose from one of the templates below to help set
            your meetings agenda, structure and help set your post-meeting satisfaction survey
            questions.</td>
          </tr>
          
        """ % colspan
        
        for template in all_templates:
            # idMeetingTemplate, title, description, purpose, agenda
            id_meeting_template = template[0]
            title = template[1]
            description = template[2]
            purpose = template[3]
            
            html += """
              <tr>
                <td class="sub_col_1"><input type="radio" name="template" value="%s">%s</td>
                <td class="sub_col_2"><b>Description:</b> %s<br><b>Purpose: </b>%s</td>
              </tr>
              
            """ % (id_meeting_template, title, description, purpose)
            
        html += """
          <tr>
            <td colspan="3" class="header"><input type="submit" value="submit" /></td>
          </tr>
          
        </table>

        </form>

        """
      
        self.add_to_body(html)
        

    def add_meeting_invite_step_2(self, form):
        self.set_title("Create a new meeting invite :: Step 2")
        
        self.js += self.tinymce_js
        
        purpose = form.getvalue('purpose')
        justification = form.getvalue('justification')
        id_template = form.getvalue('template')
        
        my_template = eamm.backend.meeting_template.MeetingTemplate()
        my_template.get(id_template)
        
        html = """
        <form id="add_meeting_invite" name="add_meeting_invite" method="post" action="/eamm/private/add_meeting_invite.py"> 
        <input type="hidden" name="step" value="step2" />
        """
        html += self.hide_past_form_contents(form)
        
        html += """
        
        <table>
          <tr>
            <td class="col1">Purpose</td>
            <td class="col2_top">%s</td>
          </tr>
        
          <tr>
            <td class="col1">Justification</td>
            <td class="col2_top">%s</td>
          </tr>

          <tr>
            <td class="col1">Template</td>
            <td class="col2_top"><b>Name:</b> %s<p><b>Description:</b> %s<p><b>Purpose: </b>%s</td>
          </tr>
        
        """ % (purpose, justification, my_template.title, my_template.description, my_template.purpose )
        
        html += """
          <tr>
            <td rowspan="2" class="col1">Agenda</td>
            <td colspan="2" class="col2_top">Effective Meetings are those that have drama and constructive
            conflict. To help achieve this, the meeting leader should create an agenda that:
            <ul>
              <li>Ensures that the most important, engaging and controversial issues are discussed first.
              <li>Constructive conflict is surfaced, encouraged and discussed until a resolution is found.
            </ul></td>
          </tr>

          <tr>
            <td colspan="2" class="col2_bottom"><textarea class="txt_area" name="agenda" cols="80">%s
            </textarea></td>
          </tr>
        
        """ % my_template.agenda
        
        html += """
           <tr>
            <td rowspan="2" class="col1">Subject</td>
            <td colspan="2" class="col2_top">Please provide a short one-line title for your meeting. This
             will be used as the Subject line in the meeting invite email.</td>
          </tr>

          <tr>
            <td colspan="2" class="col2_bottom"><input type="text" name="title" size="80"></td>
          </tr>   
              
          <tr>
            <td colspan="2" class="header"><input type="submit" value="submit" /></td>
          </tr>
          
        </table>

        </form>

        """
            
        self.add_to_body(html)
        
        
    def add_meeting_invite_step_3(self, form):
        self.set_title("Create a new meeting invite :: Step 3")
        self.js += self.tinymce_js
        self.js += self.datepicker_js
        if not self.remote_user:
            self.remote_user = "you@example.com"
        
        purpose = form.getvalue('purpose')
        justification = form.getvalue('justification')
        id_template = form.getvalue('template')
        agenda = form.getvalue('agenda')
        title = form.getvalue('title')
        
        my_template = eamm.backend.meeting_template.MeetingTemplate()
        my_template.get(id_template)
        
        html = """
        <form name="add_meeting_invite" id="add_meeting_invite" 
            onsubmit="return validateStep3Form()" method="post" 
            action="/eamm/private/add_meeting_invite.py"> 
        <input type="hidden" name="step" value="step3" /> 
        """
        
        html += self.hide_past_form_contents(form)
        
        html += """
        
        <table>
          <tr>
            <td class="col1">Title</td>
            <td colspan="4" class="col2_top">%s</td>
          </tr>
          
          <tr>
            <td class="col1">Purpose</td>
            <td colspan="4" class="col2_top">%s</td>
          </tr>
            
          <tr>
            <td class="col1">Justification</td>
            <td colspan="4" class="col2_top">%s</td>
          </tr>

          <tr>
            <td class="col1">Agenda</td>
            <td colspan="4" class="col2_top">%s</td>
          </tr>
        """ % (title, purpose, justification, agenda)
    
        html += """
          <tr>
            <td rowspan="7" class="col1">Logistics</td>
            <td class="sub_col_1">Start Date</td>
            <td class="sub_col_2" colspan="3">
                <input type="text" id="start_date" name="start_date"/></td>
          </tr>
        
          <tr>
            <td class="sub_col_1">Start Time (24 hr format)</td>
            <td class="sub_col_2" colspan="3"><input type="text" id="start_time" name="start_time" value="hh:mm"/></td>
          </tr>
          
          <tr>
            <td class="sub_col_1">Duration</td>
            <td class="sub_col_2" colspan="3"><input type="text" id="duration" name="duration" value="mm"/></td>
          </tr>
                   
          <tr>
            <td class="sub_col_1">Repeats</td>
            <td class="sub_col_2">
              <select name="recurring" id="recurring" onChange="setEndDateStatus()">
                <option value="none">none</option>
                <option value="daily">daily</option>
                <option value="weekly">weekly</option>
                <option value="monthly">monthly</option>
                <option value="quarterly">quarterly</option>
              </select>
            </td>
            <td class="sub_col_1">End Date</td>
            <td class="sub_col_2"><input type="text" id="end_date" name="end_date" value="yyyy-mm-dd"/></td>
          </tr>

          <tr>
            <td class="sub_col_1">Venue</td>
            <td class="sub_col_2" colspan="3"><input type="text" name="venue" size="50"></td>
          </tr>
                    
          <tr>
            <td class="sub_col_1">Requester</td>
            <td class="sub_col_2" colspan="3">
              <input type="text" id="requester" name="requester" value="%s" 
               size="50"/>
            </td>
          </tr>
                        
          <tr>
            <td class="sub_col_1">Invitees</td>
            <td class="sub_col_2" colspan="3"><textarea class="txt_area" cols="80" rows="10" name="invitees">each invitee email address should be on a new line</textarea></td>
          </tr>
        """ % self.remote_user
    
        html += """
          <tr>
            <td colspan="5" class="header"><input type="submit" value="Next" /></td>
          </tr>
          
        </table>

        </form>
        """
            
        self.add_to_body(html)

    def add_meeting_invite_step_4(self, form):
        self.set_title("Create a new meeting invite :: Step 4 (last one!")
        
        self.purpose = form.getvalue('purpose')
        #justification = form.getvalue('justification')
        self.id_template = form.getvalue('template')
        self.agenda = form.getvalue('agenda')
        self.title = form.getvalue('title')
        self.start_date = form.getvalue('start_date')
        self.start_time = form.getvalue('start_time')
        self.duration = form.getvalue('duration')
        self.recurring = form.getvalue('recurring')
        self.end_date = form.getvalue('end_date')
        self.venue = form.getvalue('venue')
        self.requester = form.getvalue('requester')
        self.invitees = form.getvalue('invitees')
        self.button = "Save & Send"
        
        my_template = eamm.backend.meeting_template.MeetingTemplate()
        my_template.get(self.id_template)
        self.template_title = my_template.title
        
        html = """
        <form id="add_meeting_invite" name="add_meeting_invite" method="post" action="/eamm/private/add_meeting_invite.py"> 
        <input type="hidden" name="step" value="step4" />
        """
        
        html += self.hide_past_form_contents(form)
        
        html += self.display_meeting_invite_table()
        
        self.add_to_body(html)
        
    
    def display_meeting_invite_table(self):
        html = """
        <table>
        
          <tr>
            <td class="col1">From:</td>
            <td colspan="2" class="col2_top">%s</td>
          </tr>
        
          <tr>
            <td class="col1">To:</td>
            <td colspan="2" class="col2_top">%s</td>
          </tr>  
          
          <tr>
            <td class="col1">Subject:</td>
            <td colspan="2" class="col2_top">%s</td>
          </tr>
          
          <tr>
            <td rowspan="7" class="col1">Logistics:</td>
            <td class="col1">Start Date:</td>
            <td class="col2_top">%s</td>
          </tr>
          
          <tr>
            <td class="col1">Start Time:</td>
            <td class="col2_top">%s</td>
          </tr>
          
          <tr>
            <td class="col1">Duration:</td>
            <td class="col2_top">%s</td>
          </tr>
          
          <tr>
            <td class="col1">Repeating:</td>
            <td class="col2_top">%s</td>
          </tr>
          
          <tr>
            <td class="col1">Until:</td>
            <td class="col2_top">%s</td>
          </tr>
          
          <tr>
            <td class="col1">Venue:</td>
            <td class="col2_top">%s</td>
          </tr>
          
          <tr>
            <td class="col1">From Template:</td>
            <td class="col2_top">%s</td>
          </tr>
          
           <tr>
            <td class="col1">Purpose:</td>
            <td colspan="2" class="col2_top">%s</td>
          </tr>
          
          <tr>
            <td class="col1">Agenda:</td>
            <td colspan="2" class="col2_top">%s</td>
          </tr>
          
          <tr>
            <td class="header" colspan="3"><input type="submit" value="%s"/>
            </td>
          </tr>
        </table>
        """ % (self.requester, self.invitees, self.title, self.start_date, 
               self.start_time, self.duration, self.recurring, self.end_date, 
               self.venue, self.template_title, self.purpose, self.agenda,
               self.button)
        
        return html

    def add_meeting_invite_step_5(self, form):
        self.set_title("Create a new meeting invite :: DONE !")
           
        # presuming that passing a "form" variable to the class will try and create/save
        # a new invite.
        logging.info("blah: %s" % form.getvalue("invitees"))
        
        new_invite = eamm.backend.meeting_invite.MeetingInvite(form)
        
        if new_invite.is_valid:
            # create a new DB connection instance, with autocommit off.
            db_transaction_con = eamm.backend.database.MyDatabase(autocommit="off")
            # reach in and set a new DB attribute.
            new_invite.db_connection = db_transaction_con 
            if new_invite.add():
                html = """
        
                <table>
                  <tr>
                    <td class="col1">Your meeting invite has been saved on the system and emailed to 
                                     your invitees</td>
                  </tr>
                  <tr>
                    <td class="header"> Return to <a href="/eamm/public/index.html">Main Menu</a></td>
                  </tr>
                </table>
                """
            else:
                html = self.error_table("ERROR: eamm.backend.meeting_invite.MeetingInvite.add() failed \
                                         with message <b>%s</b>" % new_invite.error)
        else:
            html = self.error_table("ERROR: eamm.backend.meeting_invite.MeetingInvite(form) \
                                         failed with message <b>%s</b>" % new_invite.error)
            
        self.add_to_body(html)
        