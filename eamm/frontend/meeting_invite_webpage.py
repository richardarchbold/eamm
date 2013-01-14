
# import necessary eamm modules.
import eamm.frontend.base_webpage 
import eamm.backend.meeting_template

# Import modules for CGI handling , the cgitb modules gives descriptive debug errors to the browser.
import cgitb; cgitb.enable(display=1)

import logging

# setup basic logging config.
logging.basicConfig(filename='/var/log/eamm.log',level=logging.INFO)

class MeetingInviteWebPage(eamm.frontend.base_webpage.WebPage):

    def __init__(self):
        super(MeetingInviteWebPage, self).__init__()
        self.js = """
            <script type="text/javascript" src="/eamm/tinymce/jscripts/tiny_mce/tiny_mce.js"></script>
            <script type="text/javascript">
                tinyMCE.init({
                mode : "textareas"
                });
            </script>
            """
    
    def add_meeting_invite_step_1(self):
        self.set_title("Create a new meeting invite :: Step 1")   
      
        html = """
        <form name="add_user" method="post" action="/eamm/add_meeting_invite.py"> 
        <input type="hidden" name="step" value="step1" />
        
        <table>
          <tr>
            <td rowspan="2" class="col1">Purpose</td>
            <td colspan="2" class="col2_top">It is critically important that your meeting has a clear
            purpose. It should be clear to everyone why the meeting is taking in place, what should
            be accomplished during the meeting, and what is expected of everyone. </td>
          </tr>

          <tr>
            <td colspan="2" class="col2_bottom"><textarea name="purpose" cols="80" rows="3" class="txt_area">
            The purpose of this meeting is to XXX such that YYY can be achieved</textarea></td>
          </tr>
        
          <tr>
            <td rowspan="2" class="col1">Justification</td>
            <td colspan="2" class="col2_top">Not every goal or task requires a meeting to be accomplished.
            Why do you need to call a meeting in this instance?</td>
          </tr>

          <tr>
            <td colspan="2" class="col2_bottom"><textarea name="justification" cols="80" rows="3" class="txt_area">$justification</textarea></td>
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
        
        purpose = form.getvalue('purpose')
        justification = form.getvalue('justification')
        id_template = form.getvalue('template')
        
        my_template = eamm.backend.meeting_template.MeetingTemplate()
        my_template.get(id_template)
        
        html = """
        <form name="add_user" method="post" action="/eamm/add_meeting_invite.py"> 
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
        
        purpose = form.getvalue('purpose')
        justification = form.getvalue('justification')
        id_template = form.getvalue('template')
        agenda = form.getvalue('agenda')
        title = form.getvalue('title')
        
        my_template = eamm.backend.meeting_template.MeetingTemplate()
        my_template.get(id_template)
        
        html = """
        <form name="add_user" method="post" action="/eamm/add_meeting_invite.py"> 
        <input type="hidden" name="step" value="step3" />
        """
        
        html += self.hide_past_form_contents(form)
        
        html += """
        
        <table>
          <tr>
            <td class="col1">Title</td>
            <td colspan="2" class="col2_top">%s</td>
          </tr>
          
          <tr>
            <td class="col1">Purpose</td>
            <td colspan="2" class="col2_top">%s</td>
          </tr>
            
          <tr>
            <td class="col1">Justification</td>
            <td colspan="2" class="col2_top">%s</td>
          </tr>

          <tr>
            <td class="col1">Agenda</td>
            <td colspan="2" class="col2_top">%s</td>
          </tr>
        
        """ % (title, purpose, justification, agenda)
    
        html += """
          <tr>
            <td rowspan="7" class="col1">Logistics</td>
            <td class="sub_col_1">Start Date</td>
            <td class="sub_col_2"><input type="text" name="start_date"></td>
          </tr>
                    
          <tr>
            <td class="sub_col_1">Start Time</td>
            <td class="sub_col_2"><input type="text" name="start_time"></td>
          </tr>
                    
          <tr>
            <td class="sub_col_1">Duration</td>
            <td class="sub_col_2"><input type="text" name="duration"></td>
          </tr>
                   
          <tr>
            <td class="sub_col_1">Recurring</td>
            <td class="sub_col_2"><input type="text" name="recurring"></td>
          </tr>

          <tr>
            <td class="sub_col_1">Venue</td>
            <td class="sub_col_2"><input type="text" name="venue"></td>
          </tr>
                    
          <tr>
            <td class="sub_col_1">Requestor</td>
            <td class="sub_col_2"><input type="text" name="requestor"></td>
          </tr>
                        
          <tr>
            <td class="sub_col_1">Invitees</td>
            <td class="sub_col_2"><textarea class="txt_area" cols="80" rows="10" name="invitees">each invitee email address should be on a new line</textarea></td>
          </tr>
        
        """
    
        html += """
          <tr>
            <td colspan="3" class="header"><input type="submit" value="submit" /></td>
          </tr>
          
        </table>

        </form>
        """
            
        self.add_to_body(html)
        
        