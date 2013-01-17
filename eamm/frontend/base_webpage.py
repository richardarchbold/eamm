import logging


# setup basic logging config
logging.basicConfig(filename="/var/log/eamm.log",level=logging.INFO)

class WebPage(object):
      
    def __init__(self):
        self.css = "css/eamm.css"
        self.title = "EAMM ::"
        self.js = ""
        self.body = ""
        
    def set_title(self, title):
        self.title = self.title + ' ' + title
        if not self.body:
            self.body = """
            <div align="center">
            <table>
            <tr>
                <td class="header"><img src="images/dilbert-meeting.jpg" width="187" height="176"/></td>
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
        print "<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" />"
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
                html += '        <input type="hidden" name="%s" value="%s" />\n' % (key, form.getvalue(key))

        return html
    