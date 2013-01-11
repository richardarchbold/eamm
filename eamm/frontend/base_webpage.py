"""This module provides webpage/html functionality common to all eamm webpages.

  Class:
      WebPage: The main class this module provides.
      
Source: https://github.com/richardarchbold/eamm
Created: 3 Jan 2013
"""

import logging

# setup basic logging config
logging.basicConfig(filename="/var/log/eamm.log",level=logging.INFO)

class WebPage(object):

    """This class provides website/html functionality common to all eamm webpages.

    Public Attributes:
        none.
    Public Methods:
        display_add_user_form()
        process_add_user_form()
    """
       
    def __init__(self):
        self.title = "EAMM ::"
        self.body = ""
        self.bgcolor = "#E6E6FA"
        
    def set_title(self, title):
        self.title = self.title + ' ' + title
        if not self.body:
            self.body = """
            <table>
            <tr><td><img src="images/dilbert-meeting.jpg" width="234" height="211"/></td>
            <td><h1>Efficient Automated Meeting Manager :: %s</h1></td></tr>
            </table><br/><br/>
            """ % title
            
    def simple_table(self, message):
        html = """
        <table width="400" border="border" align="center" bgcolor="#1E90FF">
          <tr><td>%s</td></tr>
        </table>
        """ % message
        return html
        
    def error_table(self, message):
        html = """
        <table width="400" border="border" align="center" bgcolor="#FF0040">
          <tr><td>%s</td></tr>
        </table>
        """ % message
        return html

    def add_to_body(self, body):
        self.body = self.body + ' ' + body
        
    def render(self):
        print "Content-type:text/html\r\n\r\n"
        print "<html>"
        print "<head>"
        print "<title> %s </title>" % self.title
        print "</head>"
        print "<body bgcolor=\"%s\">" % self.bgcolor
        print self.body
        print "</body>"
        print "</html>\r\n\r\n"
        