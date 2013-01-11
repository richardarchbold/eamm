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
import eamm.meeting_invite

# Import modules for CGI handling , the cgitb modules gives descriptive debug errors to the browser.
import cgi
import cgitb; cgitb.enable(display=1)

import re
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
            
    def display_add_meeting_initial_form(self):
        """A one line summary of the function/method, eg: Fetch rows from a table.

        Args:
            Arg1: description
            Arg2: description row to fetch.

        Returns:
            A dict mapping keys to the corresponding table row data
            fetched. Each row is represented as a tuple of strings. For
        
        Raises:
            IOError: An error occurred accessing the table.Tablea object.
        """
        
        self.set_title("Create a GREAT new Meeting !")
        logging.info("set the title")
        
        # Set up the start of the form, based on the teachings of "death by meeting", also get requester to state
        # the purpose and goal of the meeting.
        my_initial_meeting_form = """
        <form name="add_meeting" method="POST" action="/eamm/add_meeting.py">  
        <input type="hidden" name="method" value="display_add_meeting_initial_form">
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
            <td COLSPAN=2 width="100%"><input type="submit" value="Submit"/></form><td>
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
        
        purpose1 = form.getvalue('purpose1')
        purpose2 = form.getvalue('purpose2')
        self.purpose = "The purpose of this meeting is to <b>" + purpose1 + "</b> such that the following can be achieved: <b>" + purpose2 + "</b>."
        self.template = form.getvalue('template')
        
        # Make sure something new was entered into each field.
        if (re.match(r'.*\.\.\.state your.*', purpose1) or re.match(r'.*\.\.\.state your.*', purpose2) or not self.template):
            self.add_to_body(self.error_table("ERROR: all forms fields must be filled in!"))
            self.render()
        else:
            #self.add_to_body(self.simple_table("%s, %s, %s" % (purpose1, purpose2, template)))
            self.display_meeting_main_form(0, "rw")
            self.render()
            
    def display_meeting_main_form(self, idInvite, perms):
        """Display the main meeting invite form.

        Args:
            idInvite: an INTEGER, set to 0 (zero) if a new meeting, set to the idInvite of an existing meeting
                  which will be attempted to be loaded from the DB. 
            perms: a string, r = prints a read-only table, rw = prints writable table, so the user update the invite.

        Returns:
            none.
        
        Raises:
            IOError: An error occurred accessing the table.Table object.
        """
        
        if idInvite == 0:
            # this is a new meeting, always rw.
            my_meeting_invite = eamm.meeting_invite.MeetingInvite()
            my_meeting_invite.purpose = self.purpose
            my_meeting_invite.template = self.template
    
            self.title = "Create a new meeting invite!"
        elif idInvite > 0:
            # this is an existing meeting, check perms.
            my_meeting_invite = eamm.meeting_invite.MeetingInvite(idInvite)
            if perms == 'rw':
                # print the form writable.
                my_meeting_invite._writable = True
                self.title = "Update a meeting invite!"
            elif perms == 'r':
                # print the form read-only.
                my_meeting_invite._writable = False
                self.title = "View a meeting invite!"
            else:
                # TO-DO: this is dodgy perms, barf.
                pass
        else:
            # this is a dodgy idInvite value, barf. 
            pass
        
        my_invite_form = """
        <form name="manage_meeting" method="POST" action="/eamm/manage_meeting_invite.py"> 
        <input type="hidden" name="method" value="display_meeting_main_form">
        
        <TABLE WIDTH=762 CELLPADDING=4 CELLSPACING=0>
        <COL WIDTH=241>
        <COL WIDTH=503>
        <TR VALIGN=TOP>
            <TD WIDTH=241 STYLE="border-top: 1px double #808080; border-bottom: 1px double #808080; border-left: 1px double #808080; border-right: none; padding-top: 0.1cm; padding-bottom: 0.1cm; padding-left: 0.1cm; padding-right: 0cm">
                <P ALIGN=LEFT>Meeting Title</P>
            </TD>
            <TD WIDTH=503 STYLE="border: 1px double #808080; padding: 0.1cm">   
                <P ALIGN=LEFT>%s</P>
            </TD>
        </TR>
        <TR VALIGN=TOP>
            <TD WIDTH=241 STYLE="border-top: none; border-bottom: 1px double #808080; border-left: 1px double #808080; border-right: none; padding-top: 0cm; padding-bottom: 0.1cm; padding-left: 0.1cm; padding-right: 0cm">
                <P ALIGN=LEFT>Meeting Purpose</P>
            </TD>
            <TD WIDTH=503 STYLE="border-top: none; border-bottom: 1px double #808080; border-left: 1px double #808080; border-right: 1px double #808080; padding-top: 0cm; padding-bottom: 0.1cm; padding-left: 0.1cm; padding-right: 0.1cm">
                <P ALIGN=LEFT>&lt;writeable Meeting Purpose from form&gt;</P>
            </TD>
        </TR>
        <TR VALIGN=TOP>
            <TD WIDTH=241 STYLE="border-top: none; border-bottom: 1px double #808080; border-left: 1px double #808080; border-right: none; padding-top: 0cm; padding-bottom: 0.1cm; padding-left: 0.1cm; padding-right: 0cm">
                <P ALIGN=LEFT>Meeting Description</P>
            </TD>
            <TD WIDTH=503 STYLE="border-top: none; border-bottom: 1px double #808080; border-left: 1px double #808080; border-right: 1px double #808080; padding-top: 0cm; padding-bottom: 0.1cm; padding-left: 0.1cm; padding-right: 0.1cm">
                <P ALIGN=LEFT>&lt;insert longer Meeting Description&gt;</P>
            </TD>
        </TR>
        <TR VALIGN=TOP>
            <TD WIDTH=241 STYLE="border-top: none; border-bottom: 1px double #808080; border-left: 1px double #808080; border-right: none; padding-top: 0cm; padding-bottom: 0.1cm; padding-left: 0.1cm; padding-right: 0cm">
                <P ALIGN=LEFT>Meeting Background Reading</P>
            </TD>
            <TD WIDTH=503 STYLE="border-top: none; border-bottom: 1px double #808080; border-left: 1px double #808080; border-right: 1px double #808080; padding-top: 0cm; padding-bottom: 0.1cm; padding-left: 0.1cm; padding-right: 0.1cm">
                <P ALIGN=LEFT>&lt;insert links to any appropriate background
                reading&gt;</P>
            </TD>
        </TR>
        <TR VALIGN=TOP>
            <TD WIDTH=241 STYLE="border-top: none; border-bottom: 1px double #808080; border-left: 1px double #808080; border-right: none; padding-top: 0cm; padding-bottom: 0.1cm; padding-left: 0.1cm; padding-right: 0cm">
                <P ALIGN=LEFT>Meeting Agenda 
                </P>
            </TD>
            <TD WIDTH=503 STYLE="border-top: none; border-bottom: 1px double #808080; border-left: 1px double #808080; border-right: 1px double #808080; padding-top: 0cm; padding-bottom: 0.1cm; padding-left: 0.1cm; padding-right: 0.1cm">
                <P ALIGN=LEFT>&lt;writeable agenda, default is from template if
                one exists&gt;</P>
            </TD>
        </TR>
        <TR VALIGN=TOP>
            <TD WIDTH=241 STYLE="border-top: none; border-bottom: 1px double #808080; border-left: 1px double #808080; border-right: none; padding-top: 0cm; padding-bottom: 0.1cm; padding-left: 0.1cm; padding-right: 0cm">
                <P ALIGN=LEFT STYLE="font-style: normal">Requester Email Address</P>
            </TD>
            <TD WIDTH=503 STYLE="border-top: none; border-bottom: 1px double #808080; border-left: 1px double #808080; border-right: 1px double #808080; padding-top: 0cm; padding-bottom: 0.1cm; padding-left: 0.1cm; padding-right: 0.1cm">
                <P ALIGN=LEFT>&lt;insert email_addr&gt;</P>
            </TD>
        </TR>
        <TR VALIGN=TOP>
            <TD WIDTH=241 STYLE="border-top: none; border-bottom: 1px double #808080; border-left: 1px double #808080; border-right: none; padding-top: 0cm; padding-bottom: 0.1cm; padding-left: 0.1cm; padding-right: 0cm">
                <P ALIGN=LEFT STYLE="font-style: normal">Start Date</P>
            </TD>
            <TD WIDTH=503 STYLE="border-top: none; border-bottom: 1px double #808080; border-left: 1px double #808080; border-right: 1px double #808080; padding-top: 0cm; padding-bottom: 0.1cm; padding-left: 0.1cm; padding-right: 0.1cm">
                <P ALIGN=LEFT><BR>
                </P>
            </TD>
        </TR>
        <TR VALIGN=TOP>
            <TD WIDTH=241 STYLE="border-top: none; border-bottom: 1px double #808080; border-left: 1px double #808080; border-right: none; padding-top: 0cm; padding-bottom: 0.1cm; padding-left: 0.1cm; padding-right: 0cm">
                <P ALIGN=LEFT STYLE="font-style: normal">Start Time</P>
            </TD>
            <TD WIDTH=503 STYLE="border-top: none; border-bottom: 1px double #808080; border-left: 1px double #808080; border-right: 1px double #808080; padding-top: 0cm; padding-bottom: 0.1cm; padding-left: 0.1cm; padding-right: 0.1cm">
                <P ALIGN=LEFT><BR>
                </P>
            </TD>
        </TR>
        <TR VALIGN=TOP>
            <TD WIDTH=241 STYLE="border-top: none; border-bottom: 1px double #808080; border-left: 1px double #808080; border-right: none; padding-top: 0cm; padding-bottom: 0.1cm; padding-left: 0.1cm; padding-right: 0cm">
                <P ALIGN=LEFT STYLE="font-style: normal">Duration</P>
            </TD>
            <TD WIDTH=503 STYLE="border-top: none; border-bottom: 1px double #808080; border-left: 1px double #808080; border-right: 1px double #808080; padding-top: 0cm; padding-bottom: 0.1cm; padding-left: 0.1cm; padding-right: 0.1cm">
                <P ALIGN=LEFT><BR>
                </P>
            </TD>
        </TR>
        <TR VALIGN=TOP>
            <TD WIDTH=241 STYLE="border-top: none; border-bottom: 1px double #808080; border-left: 1px double #808080; border-right: none; padding-top: 0cm; padding-bottom: 0.1cm; padding-left: 0.1cm; padding-right: 0cm">
                <P ALIGN=LEFT STYLE="font-style: normal">Recurring</P>
            </TD>
            <TD WIDTH=503 STYLE="border-top: none; border-bottom: 1px double #808080; border-left: 1px double #808080; border-right: 1px double #808080; padding-top: 0cm; padding-bottom: 0.1cm; padding-left: 0.1cm; padding-right: 0.1cm">
                <P ALIGN=LEFT> [Drop Down Box of NONE, Daily, Weekly, Monthly,
                Quarterly]</P>
            </TD>
        </TR>
        <TR VALIGN=TOP>
            <TD WIDTH=241 STYLE="border-top: none; border-bottom: 1px double #808080; border-left: 1px double #808080; border-right: none; padding-top: 0cm; padding-bottom: 0.1cm; padding-left: 0.1cm; padding-right: 0cm">
                <P ALIGN=LEFT STYLE="font-style: normal">Venue</P>
            </TD>
            <TD WIDTH=503 STYLE="border-top: none; border-bottom: 1px double #808080; border-left: 1px double #808080; border-right: 1px double #808080; padding-top: 0cm; padding-bottom: 0.1cm; padding-left: 0.1cm; padding-right: 0.1cm">
                <P ALIGN=LEFT>&lt;insert venue.</P>
            </TD>
        </TR>
        <TR VALIGN=TOP>
            <TD WIDTH=241 STYLE="border-top: none; border-bottom: 1px double #808080; border-left: 1px double #808080; border-right: none; padding-top: 0cm; padding-bottom: 0.1cm; padding-left: 0.1cm; padding-right: 0cm">
                <P ALIGN=LEFT STYLE="font-style: normal">Meeting Invitees</P>
            </TD>
            <TD WIDTH=503 STYLE="border-top: none; border-bottom: 1px double #808080; border-left: 1px double #808080; border-right: 1px double #808080; padding-top: 0cm; padding-bottom: 0.1cm; padding-left: 0.1cm; padding-right: 0.1cm">
                <P ALIGN=LEFT>[[text area box, one email address per line]]</P>
            </TD>
        </TR>
        <TR>
            <TD COLSPAN=2 WIDTH=752 VALIGN=TOP STYLE="border-top: none; border-bottom: 1px double #808080; border-left: 1px double #808080; border-right: 1px double #808080; padding-top: 0cm; padding-bottom: 0.1cm; padding-left: 0.1cm; padding-right: 0.1cm">
                <P ALIGN=CENTER STYLE="font-style: normal">[Submit Button]</P>
            </TD>
        </TR>
    </TABLE>
        """
        
        