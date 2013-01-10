"""A one line summary of the module or script, terminated by a period.

Leave one blank line. The rest of this __doc__ string should contain an
overall description of the module or script.  Optionally, it may also
contain a brief description of exported classes and functions.

    ClassFoo: One line summary.
    functionBar(): One line summary.

Source:http://github/richardarchbold/eamm.git
Created: 7 Jan 2013
"""
__authors__ = [
  # alphabetical order by last name, please
  '"Richard  Archbold" <richardarchbold@gmail.com>',
]

import eamm.base_webpage 
import eamm.meeting_template

# Import modules for CGI handling , the cgitb modules gives descriptive debug errors to the browser.
import cgi
import cgitb; cgitb.enable(display=1)
import logging

# setup basic logging config.
logging.basicConfig(filename='/var/log/eamm.log',level=logging.INFO)
logging.info("-----------------------")

class AddMeetingWebPage(eamm.base_webpage.WebPage):
    """Summary of class here.

    Longer class information....
    Longer class information....

    Public Attributes:
        likes_spam: A boolean indicating if we like SPAM or not.
        eggs: An integer count of the eggs we have laid.
     Public Methods:
         name:  1 line summary
     """
    pass
    
    def __init__(self):
        """A one line summary of the function/method, eg: Fetch rows from a table.

        Public Args:
            Arg1: description
            Arg2: description row to fetch.

        Returns:
            A dict mapping keys to the corresponding table row data
            fetched. Each row is represented as a tuple of strings. For
        
        Raises:
            IOError: An error occurred accessing the table.Table object.
        """
        super(AddMeetingWebPage, self).__init__()
            
    def display_add_meeting_initial_form(self, template=""):
        """A one line summary of the function/method, eg: Fetch rows from a table.

        Args:
            Arg1: description
            Arg2: description row to fetch.

        Returns:
            A dict mapping keys to the corresponding table row data
            fetched. Each row is represented as a tuple of strings. For
        
        Raises:
            IOError: An error occurred accessing the table.Table object.
        """
        
        self.set_title("Create a GREAT new Meeting!")
        logging.info("set the title")
        
        # Set up the start of the form, based on the teachings of "death by meeting", also get requester to state
        # the purpose and goal of the meeting.
        my_initial_meeting_form = """
        <form name="add_meeting" method="POST" action="/eamm/add_meeting.py">  
        <TABLE WIDTH=100% CELLPADDING=4 CELLSPACING=0>
        <COL WIDTH=39*>
        <COL WIDTH=217*>
        <TR>
            <TD COLSPAN=2 WIDTH=100% VALIGN=TOP STYLE="border: 1px solid #000000; padding: 0.1cm">
                <P ALIGN=LEFT>For a meeting to be effective and efficient, it must have a clear PURPOSE & CONTEXT. This must be set by the meeting organizer in advance.</p>
                <UL>
                    <LI><P ALIGN=LEFT>It should be clear to everyone why the meeting is taking in place, what
                    should be accomplished during the meeting, and what is expected of everyone.</P>
                    <LI><P ALIGN=LEFT>Tactical &amp; Strategic topics should not be mixed into the same meeting.</P>
                    <LI><P ALIGN=LEFT>Agendas &amp; Meeting Structure, where appropriate, should be published in
                    advance.</P>
                </UL>
                <P ALIGN=LEFT>To help you create an effective, engaging meeting, please think
                about and write out the purpose of your meeting and then choose
                the most appropriate meeting template to create your meeting.</P>
                <P Align=LEFT>The purpose of this meeting is to: <textarea rows="3" cols="100" name="purpose1"> ...state your meeting purpose here ...</textarea>
                <br>
                <P Align=LEFT>Such that the following can be achieved: <textarea rows="3" cols="100" name="purpose2"> ...state your higher level goal and value proposition ... </textarea>
                <BR>
            </TD>
        </TR>
        <TR>
            <TH COLSPAN=2 WIDTH=100% VALIGN=TOP STYLE="border-top: none; border-bottom: 1px solid #000000; border-left: 1px solid #000000; 
            border-right: 1px solid #000000; padding-top: 0cm; padding-bottom: 0.1cm; padding-left: 0.1cm; padding-right: 0.1cm">
            The meeting I need to schedule most closely resembles the following template:<br>
            </TH>
        </TR>
        """

        self.add_to_body(my_initial_meeting_form)
        
        # the rest of the initial form is to get the requester to chose which template to base their meeting off.
        # we pull all the templates from the DB and show them to the user with radio buttons.
        my_meeting_template = eamm.meeting_template.MeetingTemplate() 
        all_templates = my_meeting_template.get_all()
        
        for count in range(len(all_templates)):
            # print ("key: %s, value type: %s, value: %s" % (count, new_type, all_templates[count]))
            # 0=id, 1= title, 2=description, 3=purpose, 5=agenda
            id = all_templates[count][0]
            title = all_templates[count][1]
            description = all_templates[count][2]
            purpose = all_templates[count][3]
            
            # <input type="radio" name="group1" value="Milk"> Milk<br>
            my_tr = """
                  <TR VALIGN=TOP>
                    <TD WIDTH=15% 
                        STYLE="border-top: none; 
                               border-bottom: 1px solid #000000; 
                               border-left: 1px solid #000000; 
                               border-right: none; 
                               padding-top: 0cm; 
                               padding-bottom: 0.1cm; 
                               padding-left: 0.1cm; 
                               padding-right: 0cm">
                        <P><input type="radio" name="template" value="{0}"> {1}
                        </TD>
                        <TD WIDTH=85% 
                        STYLE="border-top: none; 
                        border-bottom: 1px solid #000000; 
                        border-left: 1px solid #000000; 
                        border-right: 1px solid #000000; 
                        padding-top: 0cm; 
                        padding-bottom: 0.1cm; 
                        padding-left: 0.1cm; 
                        padding-right: 0.1cm">
                        <P>
                            Description: {2} <br><br>
                            Purpose: {3} <br>
                        </TD>
                        </TR>""".format(id, title, description, purpose)
            
            self.add_to_body(my_tr)
            
        # close out the form.
        my_form_end = """
        <tr>
            <td COLSPAN=2 width="100%"><input type="submit" value="Submit"/><td>
        </tr></table>
        """
        self.add_to_body(my_form_end)
        self.render()
    
    def process_add_meeting_initial_form(self):
        """A one line summary of the function/method, eg: Fetch rows from a table.

        Args:
            Arg1: description
            Arg2: description row to fetch.

        Returns:
            A dict mapping keys to the corresponding table row data
            fetched. Each row is represented as a tuple of strings. For
        
        Raises:
            IOError: An error occurred accessing the table.Table object.
        """
        self.set_title("Add Meeting :: Step 2")
                       
        form = cgi.FieldStorage()
        
        if form.getvalue('purpose1'):
            purpose1 = form.getvalue('purpose1')
        if form.getvalue('purpose2'):
            purpose2 = form.getvalue('purpose2')
        if form.getvalue('template'):
            template = form.getvalue('template')
        
        if not any((purpose1, purpose2, template)):
            self.add_to_body(self.error_table("ERROR: all forms fields must be filled in!"))
        
        self.render()    