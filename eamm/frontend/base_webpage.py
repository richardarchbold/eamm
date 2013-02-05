import logging



# setup basic logging config
logging.basicConfig(filename="/var/log/eamm.log",level=logging.INFO)

class WebPage(object):
      
    def __init__(self):
        self.css = "/eamm/css/eamm.css"
        self.title = "EAMM ::"
        self.js = '<script type="text/javascript"' \
                + 'src="http://127.0.0.1/eamm/js/eamm.js"></script>'
        self.body = ""
        
    def set_title(self, title):
        self.title = self.title + ' ' + title
        if not self.body:
            self.body = """
            <div align="center">
            <table>
            <tr>
              <td class="header"><img src="/eamm/images/dilbert-meeting.jpg" 
                                  width="187" height="176"/></td>
              <td class="header">Efficient Automated Meeting Manager :: %s</td>
            </tr>
            </table>
            <br><br>
            </div>
            """ % title
            
    def simple_table(self, message):
        html = """
        <table>
          <tr><td class="txt_area">%s</td></tr>
        </table>
        """ % message
        return html
        
    def error_table(self, message):
        html = """
        <table>
          <tr><td class="error">%s</td></tr>
        </table>
        """ % message
        return html

    def add_to_body(self, body):
        self.body = self.body + ' ' + body
    
    def error_exit(self, error):
        self.title = "ERROR"
        self.add_to_body(self.error_table(error))
        self.render()
        
    def render(self):
        print "Content-type:text/html\r\n\r\n"
        print "<!DOCTYPE html>"
        print "<html>"
        print "<head>"
        print "<meta http-equiv=\"Content-Type\" content=\"text/html; \
              charset=utf-8\" />"
        print "<link rel=stylesheet type=text/css href=\"%s\">" % self.css
        if self.js:
            print "%s" % self.js
        print "<title> %s </title>" % self.title
        print "</head>"
        print "<body>"
        print "<div align=\"center\">"
        print self.body
        print "</div>"
        print "</body>"
        print "</html>\r\n\r\n"
        
    def hide_past_form_contents(self, form):
        html = "\n"
        
        for key in form.keys():
            logging.info("form key: %s" % key)
            
            if key != 'step':
                html += '        <input type="hidden" name="%s" value="%s" \
                />\n' % (key, form.getvalue(key))

        return html
    
    def display_meeting_invite_table(self):
    
        invitees_list = ', '.join(self.invitees)
        
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
            <td class="col2_top">%s mins</td>
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
        """ % (self.requester, invitees_list, self.title, self.start_date, 
               self.start_time, self.duration, self.recurring, self.end_date, 
               self.venue, self.template_title, self.purpose, self.agenda,
               self.button)
        
        return html