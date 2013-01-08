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
import eamm.user

# Import modules for CGI handling , the cgitb modules gives descriptive debug errors to the browser.
import cgi
import cgitb; cgitb.enable(display=1)
import logging

# setup basic logging config.
logging.basicConfig(filename='/var/log/eamm.log',level=logging.INFO)

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
        
        self.template_chooser_form = """
        """
            
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
        
        my_inital_meeting_form = '''
        <TABLE WIDTH=100% CELLPADDING=4 CELLSPACING=0>
        <COL WIDTH=39*>
        <COL WIDTH=217*>
        <THEAD>
        <TR>
            <TH COLSPAN=2 WIDTH=100% VALIGN=TOP STYLE="border: 1px solid #000000; padding: 0.1cm">
                <P ALIGN=LEFT>In the book, “Death By Meeting”, it is stated that to have an effective, engaging 
                meeting, the meeting leader must provide:</P>
                <BR>
                <P ALIGN=LEFT><U>Clear Purpose &amp; Context</U></P>
                <UL>
                    <LI><P ALIGN=LEFT>It should be clear to everyone why the meeting is taking in place, what
                    should be accomplished during the meeting, and what is expected of everyone.</P>
                    <LI><P ALIGN=LEFT>Tactical &amp; Strategic topics should not be mixed into the same meeting.</P>
                    <LI><P ALIGN=LEFT>Agendas &amp; Meeting Structure, where appropriate, should be published in
                    advance.</P>
                </UL>
                <BR>
                <P ALIGN=LEFT>To help you create an effective, engaging meeting, please think
                about and write out the purpose of your meeting and then choose
                the most appropriate meeting template to create    your meeting.</P>
                <BR>
            </TH>
        </TR>
        </THEAD>
        <TBODY>
        '''
        
        
    
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
    
    def get_template_chooser