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
#        my_inital_meeting_form = """
#        <form name="add_meeting" method="POST" action="/eamm/add_meeting.py">  
#        <TABLE WIDTH=100% CELLPADDING=4 CELLSPACING=0>
#        <COL WIDTH=39*>
#        <COL WIDTH=217*>
#        <THEAD>
#        <TR>
#            <TH COLSPAN=2 WIDTH=100% VALIGN=TOP STYLE="border: 1px solid #000000; padding: 0.1cm">
#                <P>In the book, Death By Meeting, it is stated that to have an effective, engaging meeting, the meeting 
#                leader must provide:
#                <BR>
#                <P ALIGN=LEFT><U>Clear Purpose &amp; Context</U></P>
#                <UL>
#                    <LI><P ALIGN=LEFT>It should be clear to everyone why the meeting is taking in place, what
#                    should be accomplished during the meeting, and what is expected of everyone.</P>
#                    <LI><P ALIGN=LEFT>Tactical &amp; Strategic topics should not be mixed into the same meeting.</P>
#                    <LI><P ALIGN=LEFT>Agendas &amp; Meeting Structure, where appropriate, should be published in
#                    advance.</P>
#                </UL>
#                <BR>
#                <P ALIGN=LEFT>To help you create an effective, engaging meeting, please think
#                about and write out the purpose of your meeting and then choose
#                the most appropriate meeting template to create your meeting.</P>
#                <P Align=LEFT>The purpose of this meeting is to: <textarea rows="3" cols="100" name="purpose1"> ...state your meeting 
#                purpose here ...</textarea>
#                <br>
#                <P Align=LEFT>Such that the following can be achieved: <textarea rows="3" cols="100" name="purpose2"> ...state insert 
#                your higher level goal and value proposition ... </textarea>
#                <BR>
#            </TH>
#        </TR>
#        </THEAD>
#        
#        <TBODY>
#        <TR>
#            <TH COLSPAN=2 WIDTH=100% VALIGN=TOP STYLE="border-top: none; border-bottom: 1px solid #000000; border-left: 1px solid #000000; 
#            border-right: 1px solid #000000; padding-top: 0cm; padding-bottom: 0.1cm; padding-left: 0.1cm; padding-right: 0.1cm">
#                <BR>
#                <P ALIGN=LEFT STYLE="font-weight: normal">
#                The meeting I need to schedule most closely resembles the following template: </p><br>
#            </TH>
#        </TR>
#        <TR VALIGN=TOP>
#            <TH WIDTH=15% STYLE="border-top: none; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: none; 
#            padding-top: 0cm; padding-bottom: 0.1cm; padding-left: 0.1cm; padding-right: 0cm">
#            <P ALIGN=LEFT>Name</P>
#            </TH>
#            <TH WIDTH=85% STYLE="border-top: none; border-bottom: 1px solid #000000; border-left: 1px solid #000000; border-right: 1px 
#            solid #000000; padding-top: 0cm; padding-bottom: 0.1cm; padding-left: 0.1cm; padding-right: 0.1cm">
#            <P ALIGN=LEFT>Description</P>
#            </TH>
#        </TR>
#        """
        my_initial_meeting_form = "<table>"
        self.add_to_body(my_initial_meeting_form)
        
        # the rest of the initial form is to get the requester to chose which template to base their meeting off.
        # we pull all the templates from the DB and show them to the user with radio buttons.
        my_meeting_template = eamm.meeting_template.MeetingTemplate() 
        all_templates = my_meeting_template.get_all()
        
        for count in range(len(all_templates)):
            # print ("key: %s, value type: %s, value: %s" % (count, new_type, all_templates[count]))
            # 0=title, 1=description, 2=purpose, 3=agenda
            title = all_templates[count][0]
            description = all_templates[count][1]
            purpose = all_templates[count][2]
            
            #logging.info("title: ", all_templates[count][0])
            
#           my_tr = """
#                  <TR VALIGN=TOP>
#                    <TD WIDTH=15% 
#                        STYLE="border-top: none; 
#                               border-bottom: 1px solid #000000; 
#                               border-left: 1px solid #000000; 
#                               border-right: none; 
#                               padding-top: 0cm; 
#                               padding-bottom: 0.1cm; 
#                               padding-left: 0.1cm; 
#                               padding-right: 0cm">
#                        <P>{0}
#                        </TD>
#                        <TD WIDTH=85% 
#                        STYLE="border-top: none; 
#                        border-bottom: 1px solid #000000; 
#                        border-left: 1px solid #000000; 
#                        border-right: 1px solid #000000; 
#                        padding-top: 0cm; 
#                        padding-bottom: 0.1cm; 
#                        padding-left: 0.1cm; 
#                        padding-right: 0.1cm">
#                        <P>
#                            Description: {1} <br>
#                            Purpose: {2} <br>
#                        </TD>
#                        </TR>"""
            #my_tr.format(title, description, purpose)
            my_tr = "<tr><td>a</td><tr>"
            self.add_to_body(my_tr)
            
        # close out the form.
        self.add_to_body("</tbody></table>")
    
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
        pass